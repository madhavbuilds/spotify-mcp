# 🎵 Spotify MCP Server

> One Python file. Control Spotify with natural language from Claude Desktop.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)
![MCP](https://img.shields.io/badge/MCP-Compatible-orange?style=flat-square)
![Spotify](https://img.shields.io/badge/Spotify-Web%20API-1DB954?style=flat-square&logo=spotify&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 📺 Demo

> 🎬 **[Watch Demo Video](#)** — Claude controlling Spotify in real time

<!-- Replace # with your actual LinkedIn/YouTube video link -->

---

## ✨ What You Can Do

Just talk to Claude naturally:

- *"What am I listening to right now?"*
- *"Play something for a late night coding session"*
- *"Add 3 songs by The Weeknd to the queue"*
- *"Lower the volume to 30"*
- *"What's my most played song?"*
- *"Play some Coldplay"*

---

## 🚀 Setup

### 1. Install dependencies

```bash
pip install mcp spotipy
```

---

### 2. Get Spotify API credentials

1. Go to [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
2. Click **Create App**
3. Fill in any name and description
4. Add redirect URI: `http://127.0.0.1:8888/callback`
5. Select **Web API** and save
6. Go to **Settings** → copy your **Client ID** and **Client Secret**

---

### 3. Add your credentials

Open `spotify_mcp_server.py` and fill in at the top:

```python
SPOTIFY_CLIENT_ID     = "your_client_id"
SPOTIFY_CLIENT_SECRET = "your_client_secret"
```

---

### 4. Authorize Spotify (one time only)

Run the file once manually to complete the browser login:

```bash
python3 spotify_mcp_server.py
```

A browser window will open → Log in → Allow access → Done. Token is saved automatically, you won't need to do this again.

---

### 5. Configure Claude Desktop

#### 🍎 macOS
Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

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

#### 🪟 Windows
Edit `%APPDATA%\Claude\claude_desktop_config.json`:

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

#### 🐧 Linux
Edit `~/.config/Claude/claude_desktop_config.json`:

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

> 💡 **Tip:** To find the exact path on Mac, drag the file into Terminal — the path will appear automatically.

Restart Claude Desktop after saving.

---

## 🛠️ Tools

| Tool | What it does |
|------|-------------|
| `now_playing` | Show currently playing track |
| `play` / `pause` | Playback control |
| `skip_next` / `skip_previous` | Skip tracks |
| `set_volume` | Set volume 0–100 |
| `search_and_play` | Search and instantly play any track |
| `add_to_queue` | Add a track to the queue |
| `get_queue` | See what's coming up next |
| `my_top_tracks` | Your most played songs |
| `recently_played` | Your listening history |
| `my_playlists` | List all your playlists |
| `play_playlist` | Play a playlist by name |

---

## ❗ Troubleshooting

**`invalid_client` error**
→ Double check your Client ID and Secret — make sure nothing was copied twice or has extra spaces.

**`NO_ACTIVE_DEVICE` error**
→ Open Spotify on your phone or computer first and play any song, then try again.

**Spotify not showing in Claude**
→ Make sure the path in config is the full absolute path. Restart Claude Desktop after any changes.

**Browser opens and closes instantly**
→ Delete the cached token and run the file manually again:
```bash
rm -f ~/.spotify_mcp_token
python3 spotify_mcp_server.py
```

---

## 📋 Requirements

- Python 3.8+
- Claude Desktop
- Spotify account (Free or Premium)
- Spotify Developer account (free)

> ⚠️ **Note:** Playback control (play, pause, skip, volume) requires **Spotify Premium**. Search and stats work with free accounts.

---

## 📄 License

MIT — do whatever you want with it!# spotify-mcp
