import os
import sys
from urllib.parse import urlparse

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
    """MCP uses stdout for JSON-RPC; diagnostics must go to stderr."""
    print(msg, file=sys.stderr, flush=True)


def check_credentials() -> None:
    if not SPOTIFY_CLIENT_ID.strip() or not SPOTIFY_CLIENT_SECRET.strip():
        log(
            "Missing Spotify credentials.\n"
            "  Edit spotify_mcp/config.py and set SPOTIFY_CLIENT_ID / SPOTIFY_CLIENT_SECRET\n"
            "  Get keys at https://developer.spotify.com/dashboard"
        )
        sys.exit(1)
    if SPOTIFY_CLIENT_ID.startswith("YOUR_") or SPOTIFY_CLIENT_SECRET.startswith("YOUR_"):
        log("Replace YOUR_CLIENT_ID and YOUR_CLIENT_SECRET in spotify_mcp/config.py")
        sys.exit(1)


def redirect_host_port(redirect_uri: str) -> tuple[str, int]:
    parsed = urlparse(redirect_uri)
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    return host, port
