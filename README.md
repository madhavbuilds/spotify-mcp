# Spotify MCP Server

Control Spotify with natural language from **Claude Desktop** or **Cursor** — one Python file, no clone required.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![MCP](https://img.shields.io/badge/MCP-Compatible-orange?style=flat-square)](https://modelcontextprotocol.io/)
[![Spotify](https://img.shields.io/badge/Spotify-Web%20API-1DB954?style=flat-square&logo=spotify&logoColor=white)](https://developer.spotify.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

**Created by [Madhav Panchal](https://github.com/madhavbuilds)** · [X @maddytechspace](https://x.com/maddytechspace) · [Report an issue](https://github.com/madhavbuilds/spotify-mcp/issues) · [Download the file](https://github.com/madhavbuilds/spotify-mcp/raw/main/spotify_mcp_server.py)

---

## Table of contents

- [Features](#features)
- [Quick start](#-quick-start)
- [Daily use](#-daily-use)
- [Available tools](#-available-tools)
- [Troubleshooting](#-troubleshooting)
- [Requirements](#-requirements)
- [Security](#-security)
- [Author](#-author)
- [Contributing](#-contributing)
- [Disclaimer](#-disclaimer)
- [License](#-license)

---

## Features

- **Single file** — download `spotify_mcp_server.py` and go
- **Natural language** — ask Claude or Cursor to play, pause, search, queue, and more
- **11 MCP tools** — playback, queue, search, playlists, and listening stats
- **One-time Spotify login** — OAuth token saved locally
- **Works on Mac & Windows** — clear setup steps for each platform

---

## Quick start

### Step 1 — Download one file

Download **[`spotify_mcp_server.py`](https://github.com/madhavbuilds/spotify-mcp/raw/main/spotify_mcp_server.py)** (right-click → Save as).

Save it anywhere, for example:

| Platform | Example location |
|----------|------------------|
| Mac | `~/spotify-mcp/spotify_mcp_server.py` |
| Windows | `C:\Tools\spotify_mcp_server.py` |

No `git clone` needed — only this file.

---

### Step 2 — Install dependencies

**Mac**

```bash
pip3 install mcp spotipy
```

**Windows**

```bash
pip install mcp spotipy
```

---

### Step 3 — Spotify API credentials

1. Open the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Click **Create App** and fill in the details
3. Under **Redirect URIs**, add: `http://127.0.0.1:8888/callback`
4. Open **Settings** and copy your **Client ID** and **Client Secret**
5. Open `spotify_mcp_server.py` in any text editor and paste them at the top:

```python
SPOTIFY_CLIENT_ID     = "your_client_id"
SPOTIFY_CLIENT_SECRET = "your_client_secret"
```

---

### Step 4 — Authorize Spotify (one time)

Run this from the folder where you saved the file:

**Mac**

```bash
python3 spotify_mcp_server.py --login
```

**Windows**

```bash
python spotify_mcp_server.py --login
```

Your browser opens → log in to Spotify → allow access. A token is saved to `~/.spotify_mcp_token` (Mac) or `%USERPROFILE%\.spotify_mcp_token` (Windows). You only do this once.

---

### Step 5 — Connect Claude or Cursor

Replace the path in `args` with the **full absolute path** to your downloaded file, then restart the app.

> Use **either** Claude Desktop **or** Cursor with this server — not both at the same time.

#### Claude Desktop

| Platform | Config file location |
|----------|----------------------|
| Mac | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |

**Mac**

```json
{
  "mcpServers": {
    "spotify": {
      "command": "python3",
      "args": ["/full/path/to/spotify_mcp_server.py"]
    }
  }
}
```

**Windows**

```json
{
  "mcpServers": {
    "spotify": {
      "command": "python",
      "args": ["C:\\full\\path\\to\\spotify_mcp_server.py"]
    }
  }
}
```

#### Cursor

| Platform | Config file location |
|----------|----------------------|
| Mac | `~/.cursor/mcp.json` |
| Windows | `%USERPROFILE%\.cursor\mcp.json` |

**Mac**

```json
{
  "mcpServers": {
    "spotify": {
      "command": "python3",
      "args": ["/full/path/to/spotify_mcp_server.py"]
    }
  }
}
```

**Windows**

```json
{
  "mcpServers": {
    "spotify": {
      "command": "python",
      "args": ["C:\\full\\path\\to\\spotify_mcp_server.py"]
    }
  }
}
```

**Tip (Mac):** Drag the file into Terminal to copy its full path.

---

## Daily use

1. Open **Spotify** on your phone or computer (start playback once if the device is inactive).
2. Open **Claude Desktop** or **Cursor**.
3. Ask in plain language, for example:

   - *"What's playing right now?"*
   - *"Play Blinding Lights"*
   - *"Pause"*
   - *"Add Drake to the queue"*
   - *"Set volume to 40"*

No terminal commands needed after setup.

---

## Available tools

| Tool | Description |
|------|-------------|
| `now_playing` | Show the current track |
| `play` | Resume playback |
| `pause` | Pause playback |
| `skip_next` | Skip to the next track |
| `skip_previous` | Go to the previous track |
| `set_volume` | Set volume (0–100) |
| `search_and_play` | Search and play a track immediately |
| `add_to_queue` | Search and add a track to the queue |
| `get_queue` | View upcoming tracks |
| `my_top_tracks` | Your most played tracks |
| `recently_played` | Recently played tracks |
| `my_playlists` | List your playlists |
| `play_playlist` | Play a playlist by name |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `invalid_client` | Double-check Client ID and Secret in `spotify_mcp_server.py` — no extra spaces |
| `NO_ACTIVE_DEVICE` | Open Spotify on a device and play any song once, then retry |
| MCP server not listed | Use the **full absolute path** in `args`; restart Claude/Cursor |
| `python` / `python3` not found | Install [Python 3.10+](https://www.python.org/downloads/) and ensure it is on your PATH |

**Re-authorize Spotify**

**Mac**

```bash
rm -f ~/.spotify_mcp_token
python3 spotify_mcp_server.py --login
```

**Windows**

```powershell
Remove-Item "$env:USERPROFILE\.spotify_mcp_token" -ErrorAction SilentlyContinue
python spotify_mcp_server.py --login
```

Still stuck? [Open an issue](https://github.com/madhavbuilds/spotify-mcp/issues).

---

## Requirements

| Requirement | Notes |
|-------------|--------|
| Python 3.10+ | [Download Python](https://www.python.org/downloads/) |
| `mcp`, `spotipy` | Installed via pip (see Step 2) |
| Spotify account | Free or Premium |
| Spotify Developer app | Free at [developer.spotify.com](https://developer.spotify.com/dashboard) |
| Claude Desktop or Cursor | MCP-enabled client |

> **Premium note:** Playback control (play, pause, skip, volume) requires **Spotify Premium**. Search, queue, and listening stats work on free accounts.

---

## Security

- API credentials live **only in your local copy** of `spotify_mcp_server.py` — never commit real keys to GitHub.
- OAuth tokens are stored locally in `~/.spotify_mcp_token` (Mac) or `%USERPROFILE%\.spotify_mcp_token` (Windows).
- This project runs on your machine; no data is sent to any third-party server besides Spotify's API.

---

## Author

**Madhav Panchal** — builder, open-source enthusiast

- GitHub: [@madhavbuilds](https://github.com/madhavbuilds)
- X: [@maddytechspace](https://x.com/maddytechspace)
- Project: [spotify-mcp](https://github.com/madhavbuilds/spotify-mcp)

If this project helped you, consider starring the repo — it helps others discover it.

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

For bugs or ideas, [open an issue](https://github.com/madhavbuilds/spotify-mcp/issues) first.

---

## Disclaimer

This is a **third-party integration** and is **not** made by, affiliated with, or endorsed by **Spotify**, **Anthropic** (Claude), or **Cursor**.

Made by **Madhav Panchal** ([@madhavbuilds](https://github.com/madhavbuilds) · [@maddytechspace](https://x.com/maddytechspace) on X).

Use at your own discretion. You are responsible for complying with Spotify's [Terms of Use](https://www.spotify.com/legal/end-user-agreement/) and [Developer Policy](https://developer.spotify.com/policy).

---

## License

This project is licensed under the [MIT License](LICENSE).

Copyright © 2026 Madhav Panchal
