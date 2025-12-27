# 🎵 Navan YT Downloader

A Linux-first, Flask-based YouTube downloader powered by yt-dlp. Provides a modern web UI to download audio/video, manage a local library, and perform batch downloads efficiently.

This project is designed for personal use, learning, and local LAN access — not for public hosting.

---

## ✨ Features

- 🎧 Audio download (MP3) with selectable quality  
- 🎥 Video download (MP4) with resolution control  
- 🔗 Single YouTube link download  
- 📋 Multiple link download (paste list)  
- 📁 Upload `.txt` file containing multiple links  
- 📺 Full YouTube channel download  
- 📚 Live download library (browser-accessible)  
- 🗜️ Download entire library as a ZIP  
- ⚡ Powered by native Linux `yt-dlp`  
- 🌐 Flask backend + modern Tailwind frontend

---

## 📁 Project Structure

```
yt-downloader/
├── server.py               # Flask backend
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html          # Frontend UI
├── temp_audio/             # Download destination (NOT tracked)
│   ├── uploads/            # Uploaded .txt files
│   └── *.mp3 / *.mp4       # Downloaded media
├── cookies.txt             # YouTube cookies (NOT tracked)
└── README.md
```

> ⚠️ `cookies.txt` and `temp_audio/` are intentionally NOT committed for privacy and storage reasons.

---

## 🔐 About cookies.txt (NOT included)

YouTube may restrict:
- age-restricted videos  
- region-locked content  
- private / member content

To handle these cases, `yt-dlp` can use your own browser cookies.

How to generate `cookies.txt`:
1. Install a cookies exporter extension (Chrome/Firefox) — e.g., "Get cookies.txt".  
2. Log in to YouTube in your browser.  
3. Export cookies as `cookies.txt`.  
4. Place it at either:
   - `yt-downloader/cookies.txt`  
   - or `yt-downloader/temp_audio/cookies.txt`

Never upload `cookies.txt` to GitHub — it contains session data linked to your account.

---

## 🔒 Why temp_audio/ is NOT included

- Contains large media files  
- Machine-specific storage  
- Would bloat the repository

---

## 🧩 Setup

Recommended: create a Python virtual environment.

```bash
# create venv and activate
python3 -m venv yt-venv
source yt-venv/bin/activate

# install python deps
pip install -r requirements.txt

# create required folders
mkdir -p temp_audio/uploads
```

System packages (Ubuntu / Debian recommended):

```bash
sudo apt update
sudo apt install -y yt-dlp ffmpeg
```

Notes:
- `yt-dlp` should be installed system-wide or otherwise available in PATH.
- Python 3.10+ is recommended.

---

## 🚀 Running the Application

From the project root:

```bash
python server.py
```

You should see output similar to:

> 🚀 Server running on http://0.0.0.0:8000

Open in browser:
- Local: http://127.0.0.1:8000  
- LAN: http://<your-local-ip>:8000

---

## 🧠 Usage Guide

- 🔹 Single download  
  - Select "Single Link"  
  - Paste YouTube URL  
  - Choose audio/video + quality  
  - Click "Start Download"

- 🔹 Multiple downloads  
  - Select "Multiple Links"  
  - Paste one link per line  
  - Start download

- 🔹 File upload  
  - Upload a `.txt` file containing links (one per line)

- 🔹 Full channel  
  - Select "Full Channel"  
  - Paste channel URL to download all videos

- 🔹 Library  
  - View downloaded media in browser  
  - Download individual files or the entire library as a ZIP

---

## ⚠️ Disclaimer

This project is intended for:
- educational purposes  
- personal offline backups

Respect:
- YouTube’s Terms of Service  
- Copyright laws in your region

The author is not responsible for misuse.

---

## 👨‍💻 Author

Navaneeth (Mitu)  
B.Tech CSE – CET Trivandrum  
Linux • Backend • Systems • AI

---

## ⭐ Future Improvements

- Download progress tracking  
- Job queue & cancellation  
- Authentication  
- Mobile-first UI polish  
- Dockerized setup

---