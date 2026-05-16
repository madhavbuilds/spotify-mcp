import asyncio

import spotipy
from mcp import types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from spotify_mcp.client import get_spotify
from spotify_mcp.config import log

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
    log("Spotify MCP server running (waiting for Claude on stdin).")
    async with stdio_server() as streams:
        await server.run(streams[0], streams[1], server.create_initialization_options())
