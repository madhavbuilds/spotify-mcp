#!/usr/bin/env python3
"""
Spotify MCP Server — single file, no clone needed.
==================================================
1. pip install mcp spotipy
2. Fill in SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET below
3. python spotify_mcp_server.py --login
4. Point Claude/Cursor MCP config at this file (full path)
"""

import argparse
import asyncio
import os
import sys
import webbrowser
from functools import lru_cache
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

import spotipy
from mcp import types
from mcp.server import Server
from mcp.server.stdio import stdio_server
from spotipy.oauth2 import SpotifyOAuth

# ============================================================
#   FILL IN YOUR CREDENTIALS HERE
#   https://developer.spotify.com/dashboard
# ============================================================
SPOTIFY_CLIENT_ID = "YOUR_CLIENT_ID"
SPOTIFY_CLIENT_SECRET = "YOUR_CLIENT_SECRET"
SPOTIFY_REDIRECT_URI = "http://127.0.0.1:8888/callback"
# ============================================================

TOKEN_PATH = os.path.expanduser("~/.spotify_mcp_token")

SCOPE = (
    "user-read-playback-state "
    "user-modify-playback-state "
    "user-read-currently-playing "
    "playlist-read-private "
    "playlist-read-collaborative "
    "user-top-read "
    "user-read-recently-played "
    "streaming"
)


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def check_credentials() -> None:
    if not SPOTIFY_CLIENT_ID.strip() or not SPOTIFY_CLIENT_SECRET.strip():
        log(
            "Missing Spotify credentials.\n"
            "  Edit spotify_mcp_server.py and set SPOTIFY_CLIENT_ID / SPOTIFY_CLIENT_SECRET\n"
            "  Get keys at https://developer.spotify.com/dashboard"
        )
        sys.exit(1)
    if SPOTIFY_CLIENT_ID.startswith("YOUR_") or SPOTIFY_CLIENT_SECRET.startswith("YOUR_"):
        log("Replace YOUR_CLIENT_ID and YOUR_CLIENT_SECRET in spotify_mcp_server.py")
        sys.exit(1)


def redirect_host_port(redirect_uri: str) -> tuple[str, int]:
    parsed = urlparse(redirect_uri)
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    return host, port


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


@lru_cache(maxsize=1)
def get_spotify() -> spotipy.Spotify:
    return run_oauth_flow()


server = Server("spotify-mcp")


@server.list_tools()
async def list_tools():
    return [
        types.Tool(
            name="now_playing",
            description="Show the currently playing track",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="play",
            description="Play or resume music",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="pause",
            description="Pause the music",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="skip_next",
            description="Skip to the next track",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="skip_previous",
            description="Go back to the previous track",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="set_volume",
            description="Set the volume (0 to 100)",
            inputSchema={
                "type": "object",
                "properties": {
                    "volume": {
                        "type": "integer",
                        "description": "Volume level between 0 and 100",
                        "minimum": 0,
                        "maximum": 100,
                    }
                },
                "required": ["volume"],
            },
        ),
        types.Tool(
            name="search_and_play",
            description="Search for a track and play it immediately",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Track name, artist, or mood",
                    }
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="add_to_queue",
            description="Add a track to the queue",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Track name or artist to search and queue",
                    }
                },
                "required": ["query"],
            },
        ),
        types.Tool(
            name="get_queue",
            description="View the upcoming tracks in the queue",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="my_top_tracks",
            description="Get your most played tracks",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of tracks to return (default 10)",
                        "default": 10,
                    }
                },
            },
        ),
        types.Tool(
            name="recently_played",
            description="Get your recently played tracks",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of tracks to return (default 10)",
                        "default": 10,
                    }
                },
            },
        ),
        types.Tool(
            name="my_playlists",
            description="List all your playlists",
            inputSchema={"type": "object", "properties": {}},
        ),
        types.Tool(
            name="play_playlist",
            description="Play a playlist by name",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name of the playlist to play",
                    }
                },
                "required": ["name"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    sp = get_spotify()

    try:
        if name == "now_playing":
            current = sp.current_playback()
            if not current or not current.get("item"):
                return [types.TextContent(type="text", text="Nothing is currently playing.")]
            item = current["item"]
            artists = ", ".join(a["name"] for a in item["artists"])
            status = "Playing" if current["is_playing"] else "Paused"
            vol = current.get("device", {}).get("volume_percent", "?")
            result = (
                f"{status}\n"
                f"Track: {item['name']}\n"
                f"Artists: {artists}\n"
                f"Album: {item['album']['name']}\n"
                f"Volume: {vol}%"
            )
            return [types.TextContent(type="text", text=result)]

        if name == "play":
            sp.start_playback()
            return [types.TextContent(type="text", text="Music is playing.")]

        if name == "pause":
            sp.pause_playback()
            return [types.TextContent(type="text", text="Music paused.")]

        if name == "skip_next":
            sp.next_track()
            return [types.TextContent(type="text", text="Skipped to next track.")]

        if name == "skip_previous":
            sp.previous_track()
            return [types.TextContent(type="text", text="Went to previous track.")]

        if name == "set_volume":
            vol = arguments.get("volume", 50)
            sp.volume(vol)
            return [types.TextContent(type="text", text=f"Volume set to {vol}%.")]

        if name == "search_and_play":
            query = arguments["query"]
            results = sp.search(q=query, limit=1, type="track")
            tracks = results["tracks"]["items"]
            if not tracks:
                return [types.TextContent(type="text", text=f"No track found for '{query}'.")]
            track = tracks[0]
            sp.start_playback(uris=[track["uri"]])
            artists = ", ".join(a["name"] for a in track["artists"])
            return [
                types.TextContent(
                    type="text",
                    text=f"Now playing: {track['name']} — {artists}",
                )
            ]

        if name == "add_to_queue":
            query = arguments["query"]
            results = sp.search(q=query, limit=1, type="track")
            tracks = results["tracks"]["items"]
            if not tracks:
                return [types.TextContent(type="text", text=f"No track found for '{query}'.")]
            track = tracks[0]
            sp.add_to_queue(track["uri"])
            artists = ", ".join(a["name"] for a in track["artists"])
            return [
                types.TextContent(
                    type="text",
                    text=f"Added to queue: {track['name']} — {artists}",
                )
            ]

        if name == "get_queue":
            queue_data = sp.queue()
            if not queue_data or not queue_data.get("queue"):
                return [types.TextContent(type="text", text="The queue is empty.")]
            tracks = queue_data["queue"][:10]
            lines = ["Up next:"]
            for i, t in enumerate(tracks, 1):
                artists = ", ".join(a["name"] for a in t["artists"])
                lines.append(f"{i}. {t['name']} — {artists}")
            return [types.TextContent(type="text", text="\n".join(lines))]

        if name == "my_top_tracks":
            limit = arguments.get("limit", 10)
            results = sp.current_user_top_tracks(limit=limit, time_range="medium_term")
            lines = ["Your top tracks:"]
            for i, t in enumerate(results["items"], 1):
                artists = ", ".join(a["name"] for a in t["artists"])
                lines.append(f"{i}. {t['name']} — {artists}")
            return [types.TextContent(type="text", text="\n".join(lines))]

        if name == "recently_played":
            limit = arguments.get("limit", 10)
            results = sp.current_user_recently_played(limit=limit)
            lines = ["Recently played:"]
            for i, item in enumerate(results["items"], 1):
                t = item["track"]
                artists = ", ".join(a["name"] for a in t["artists"])
                lines.append(f"{i}. {t['name']} — {artists}")
            return [types.TextContent(type="text", text="\n".join(lines))]

        if name == "my_playlists":
            results = sp.current_user_playlists(limit=20)
            lines = ["Your playlists:"]
            for i, p in enumerate(results["items"], 1):
                lines.append(f"{i}. {p['name']} ({p['tracks']['total']} tracks)")
            return [types.TextContent(type="text", text="\n".join(lines))]

        if name == "play_playlist":
            name_query = arguments["name"].lower()
            results = sp.current_user_playlists(limit=50)
            matched = next(
                (p for p in results["items"] if name_query in p["name"].lower()),
                None,
            )
            if not matched:
                return [
                    types.TextContent(
                        type="text",
                        text=f"No playlist found matching '{arguments['name']}'.",
                    )
                ]
            sp.start_playback(context_uri=matched["uri"])
            return [
                types.TextContent(type="text", text=f"Now playing playlist: {matched['name']}")
            ]

        return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

    except spotipy.exceptions.SpotifyException as e:
        if "NO_ACTIVE_DEVICE" in str(e):
            return [
                types.TextContent(
                    type="text",
                    text=(
                        "No active Spotify device. Open Spotify on your phone or computer, "
                        "start playback once, then try again."
                    ),
                )
            ]
        return [types.TextContent(type="text", text=f"Spotify error: {e}")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {e}")]


async def run_mcp_server() -> None:
    log("Spotify MCP server running.")
    async with stdio_server() as streams:
        await server.run(streams[0], streams[1], server.create_initialization_options())


def main() -> None:
    check_credentials()
    parser = argparse.ArgumentParser(description="Spotify MCP server")
    parser.add_argument(
        "--login",
        action="store_true",
        help="Authorize Spotify once in the browser",
    )
    args = parser.parse_args()

    if args.login:
        run_oauth_flow()
        return

    asyncio.run(run_mcp_server())


if __name__ == "__main__":
    main()
