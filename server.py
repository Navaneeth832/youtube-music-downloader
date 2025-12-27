import os
import subprocess
import zipfile
from flask import Flask, request, jsonify, send_from_directory, send_file, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

DEST_FOLDER = os.path.expanduser("~/projects/yt-downloader/temp_audio")
UPLOAD_FOLDER = os.path.join(DEST_FOLDER, "uploads")
ZIP_PATH = os.path.join(DEST_FOLDER, "all_downloads.zip")

os.makedirs(DEST_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- CORE DOWNLOAD ----------------
def run_yt_dlp(urls, media_type, quality, is_channel=False):
    base_cmd = [
        "yt-dlp",
        "--force-overwrites",
        "-o", f"{DEST_FOLDER}/%(title)s.%(ext)s"
    ]

    if media_type == "audio":
        q = quality.replace("k", "")
        base_cmd += [
            "-x",
            "--audio-format", "mp3",
            "--audio-quality", q
        ]
    else:
        base_cmd += [
            "-f", f"bestvideo[height<={quality}]+bestaudio/best",
            "--merge-output-format", "mp4"
        ]

    if not is_channel:
        base_cmd.append("--no-playlist")

    base_cmd.extend(urls)

    subprocess.run(base_cmd)

# ---------------- SINGLE / MULTI / CHANNEL ----------------
@app.route("/download", methods=["POST"])
def download():
    data = request.json
    mode = data.get("mode")  # single | multi | channel
    media_type = data.get("type")
    quality = data.get("quality")

    if mode == "single":
        urls = [data.get("url")]
    elif mode == "multi":
        urls = data.get("urls", [])
    elif mode == "channel":
        urls = [data.get("url")]
    else:
        return jsonify({"error": "Invalid mode"}), 400

    run_yt_dlp(urls, media_type, quality, is_channel=(mode == "channel"))

    return jsonify({"status": "started"})

# ---------------- FILE UPLOAD ----------------
@app.route("/download-file", methods=["POST"])
def download_file():
    file = request.files.get("file")
    media_type = request.form.get("type")
    quality = request.form.get("quality")

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    with open(path) as f:
        urls = [line.strip() for line in f if line.strip()]

    run_yt_dlp(urls, media_type, quality)

    return jsonify({"status": "started"})

# ---------------- LIBRARY ----------------
@app.route("/files")
def files():
    out = []
    for f in os.listdir(DEST_FOLDER):
        if f.endswith((".mp3", ".mp4", ".m4a")):
            p = os.path.join(DEST_FOLDER, f)
            out.append({
                "name": f,
                "size": f"{os.path.getsize(p)/(1024*1024):.2f} MB"
            })
    return jsonify(out)

@app.route("/files/<filename>")
def get_file(filename):
    return send_from_directory(DEST_FOLDER, filename, as_attachment=True)

# ---------------- ZIP ALL ----------------
@app.route("/zip")
def zip_all():
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zipf:
        for f in os.listdir(DEST_FOLDER):
            if f.endswith((".mp3", ".mp4", ".m4a")):
                zipf.write(os.path.join(DEST_FOLDER, f), f)
    return send_file(ZIP_PATH, as_attachment=True)

# ---------------- RUN ----------------
if __name__ == "__main__":
    print("🚀 Server running on http://0.0.0.0:8000")
    app.run(host="0.0.0.0", port=8000, debug=True)
