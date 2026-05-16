# 🎵 Spotify MCP Server

> **One file.** Download, add your keys, connect Claude or Cursor — no clone needed.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![MCP](https://img.shields.io/badge/MCP-Compatible-orange?style=flat-square)
![Spotify](https://img.shields.io/badge/Spotify-Web%20API-1DB954?style=flat-square&logo=spotify&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## ⚡ Quick start (3 minutes)

### 1. Download one file

Get **`spotify_mcp_server.py`** — pick any option:

- [Download from GitHub](https://github.com/madhavbuilds/spotify-mcp/raw/main/spotify_mcp_server.py) (right‑click → Save as)
- Or copy it to a folder like `C:\Tools\` or `~/spotify-mcp/`

You only need this **one file**. No git clone.

---

### 2. Install Python packages

```bash
pip install mcp spotipy
```

---

### 3. Spotify API keys

1. [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard) → **Create App**
2. Redirect URI: `http://127.0.0.1:8888/callback`
3. Copy **Client ID** and **Client Secret**
4. Open `spotify_mcp_server.py` in any editor and paste them at the top:

```python
SPOTIFY_CLIENT_ID     = "your_client_id"
SPOTIFY_CLIENT_SECRET = "your_client_secret"
```

---

### 4. Log in once

In the folder where you saved the file:

```bash
python spotify_mcp_server.py --login
```

Browser opens → log in to Spotify → allow access. Done. (Token saved; you won’t repeat this.)

---

### 5. Connect Claude or Cursor

Use the **full path** to your downloaded file.

**Claude Desktop** — `%APPDATA%\Claude\claude_desktop_config.json` (Windows) or `~/Library/Application Support/Claude/claude_desktop_config.json` (Mac):

```json
{
  "mcpServers": {
    "spotify": {
      "command": "python",
      "args": ["C:\\Tools\\spotify_mcp_server.py"]
    }
  }
}
```

**Cursor** — `%USERPROFILE%\.cursor\mcp.json` (Windows) or `~/.cursor/mcp.json` (Mac/Linux):

```json
{
  "mcpServers": {
    "spotify": {
      "command": "python3",
      "args": ["/Users/you/spotify_mcp_server.py"]
    }
  }
}
```

On Mac/Linux use `python3` in `command`. Restart the app after saving.

> Run **either** Claude **or** Cursor with this server — not both at once.

---

## 🎯 Daily use

1. Open Spotify on your phone or computer (play something once if needed).
2. Open Claude or Cursor.
3. Chat naturally:
   - *"What's playing?"*
   - *"Play Blinding Lights"*
   - *"Pause"*
   - *"Add Drake to the queue"*

No terminal commands needed after setup.

---

## 🛠️ Tools

| Tool | What it does |
|------|-------------|
| `now_playing` | Show currently playing track |
| `play` / `pause` | Playback control |
| `skip_next` / `skip_previous` | Skip tracks |
| `set_volume` | Set volume 0–100 |
| `search_and_play` | Search and play a track |
| `add_to_queue` | Add a track to the queue |
| `get_queue` | See what's up next |
| `my_top_tracks` | Your most played songs |
| `recently_played` | Listening history |
| `my_playlists` | List playlists |
| `play_playlist` | Play a playlist by name |

---

## ❗ Troubleshooting

**`invalid_client`** — Check Client ID/Secret; no extra spaces.

**`NO_ACTIVE_DEVICE`** — Open Spotify and start playback on one device, then retry.

**MCP not showing** — Use the **full absolute path** in `args`. Restart Claude/Cursor.

**Login again**

```bash
# Mac/Linux
rm -f ~/.spotify_mcp_token
python spotify_mcp_server.py --login
```

```powershell
# Windows
Remove-Item "$env:USERPROFILE\.spotify_mcp_token" -ErrorAction SilentlyContinue
python spotify_mcp_server.py --login
```

---

## 📋 Requirements

- Python 3.10+
- `pip install mcp spotipy`
- Spotify account + free [Developer](https://developer.spotify.com/dashboard) app
- Claude Desktop or Cursor

Playback control (play/pause/skip/volume) needs **Spotify Premium**. Search and stats work on free accounts.

---

## 📄 License

MIT
