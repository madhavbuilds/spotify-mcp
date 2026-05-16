import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from spotify_mcp.config import (
    SCOPE,
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    SPOTIFY_REDIRECT_URI,
    TOKEN_PATH,
    check_credentials,
    log,
    redirect_host_port,
)


def build_auth_manager() -> SpotifyOAuth:
    check_credentials()
    return SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SCOPE,
        cache_path=TOKEN_PATH,
        open_browser=False,
    )


def run_oauth_flow(auth_manager: SpotifyOAuth | None = None) -> spotipy.Spotify:
    auth_manager = auth_manager or build_auth_manager()
    host, port = redirect_host_port(SPOTIFY_REDIRECT_URI)

    if auth_manager.get_cached_token():
        log("Spotify already authorized (cached token found).")
        return spotipy.Spotify(auth_manager=auth_manager)

    auth_url = auth_manager.get_authorize_url()
    log(f"\nOpen this URL to authorize Spotify:\n\n{auth_url}\n")
    try:
        webbrowser.open(auth_url)
    except Exception:
        pass

    callback_code: list[str | None] = [None]
    callback_error: list[str | None] = [None]

    class CallbackHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            params = parse_qs(urlparse(self.path).query)
            if "code" in params:
                callback_code[0] = params["code"][0]
                body = b"<h1>Spotify connected. You can close this tab.</h1>"
            elif "error" in params:
                callback_error[0] = params.get("error_description", params["error"])[0]
                body = b"<h1>Authorization failed. Check the terminal.</h1>"
            else:
                body = b"<h1>Waiting for Spotify...</h1>"
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format, *args):
            pass

    log(f"Waiting for callback on {host}:{port} ...")
    httpd = HTTPServer((host, port), CallbackHandler)
    httpd.handle_request()

    if callback_error[0]:
        log(f"Authorization failed: {callback_error[0]}")
        sys.exit(1)
    if not callback_code[0]:
        log("No authorization code received. Try again.")
        sys.exit(1)

    auth_manager.get_access_token(callback_code[0], as_dict=False)
    log("Spotify authorized successfully.")
    return spotipy.Spotify(auth_manager=auth_manager)
