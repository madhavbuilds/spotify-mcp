from functools import lru_cache

import spotipy

from spotify_mcp.auth import run_oauth_flow


@lru_cache(maxsize=1)
def get_spotify() -> spotipy.Spotify:
    return run_oauth_flow()
