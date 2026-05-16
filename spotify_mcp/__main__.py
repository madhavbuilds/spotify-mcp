import argparse
import asyncio

from spotify_mcp.auth import run_oauth_flow
from spotify_mcp.config import check_credentials
from spotify_mcp.server import run_mcp_server


def main() -> None:
    check_credentials()
    parser = argparse.ArgumentParser(description="Spotify MCP server")
    parser.add_argument(
        "--login",
        action="store_true",
        help="Run Spotify OAuth in the terminal (do this once before using in Claude)",
    )
    args = parser.parse_args()

    if args.login:
        run_oauth_flow()
        return

    asyncio.run(run_mcp_server())


if __name__ == "__main__":
    main()
