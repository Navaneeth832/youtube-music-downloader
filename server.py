import os
import subprocess
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask import Flask, render_template

app = Flask(__name__)
CORS(app)  # Allows your React frontend to talk to this server

# Change this to your actual laptop path
DEST_FOLDER = os.path.expanduser("~/projects/yt-downloader/temp_audio")
COOKIES_FILE = os.path.join(DEST_FOLDER, "cookies.txt")

# Ensure directory exists
if not os.path.exists(DEST_FOLDER):
    os.makedirs(DEST_FOLDER)

@app.route('/download', methods=['POST'])
def download_media():
    data = request.json
    print("RAW DATA:", request.json)

    url = (data or {}).get('url')
    if not url or not url.startswith("http"):
        return jsonify({"error": "Invalid or missing URL"}), 400

    media_type = data.get('type')  # 'audio' or 'video'
    quality = data.get('quality')   # e.g., '128k', '320k', '1080'
  
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    # Build the yt-dlp command based on your "secret.txt" vibe
    cmd = [
        "yt-dlp",
        "--no-playlist",
        "--cookies", COOKIES_FILE,
        "--force-overwrites",
        "-o", f"{DEST_FOLDER}/%(title)s.%(ext)s"
    ]

    if media_type == 'audio':
        audio_q = quality.replace('k', '') if quality else '192'
        cmd += [
            "-f", "ba",
            "-x",
            "--audio-format", "mp3",
            "--audio-quality", audio_q
        ]

    else:
        # For video quality, we use -f to specify resolution
        cmd += [
            "-f", f"bestvideo[height<={quality}]+bestaudio/best[height<={quality}]",
            "--merge-output-format", "mp4"
        ]
    print("CMD:", " ".join(cmd))
    url = url.split("&list=")[0]

    cmd.append(url)
    print("FINAL CMD:", cmd)

    try:
        # Run the command
        process = subprocess.run(cmd, text=True)

        
        if process.returncode == 0:
            return jsonify({
                "status": "success",
                "message": f"Downloaded to {DEST_FOLDER}",
                "output": process.stdout
            })
        else:
            return jsonify({
                "status": "error", 
                "message": "yt-dlp failed",
                "error": process.stderr
            }), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/files', methods=['GET'])
def list_files():
    # Return list of files in the destination folder
    files = []
    for filename in os.listdir(DEST_FOLDER):
        if filename.endswith(('.mp3', '.mp4', '.m4a')):
            path = os.path.join(DEST_FOLDER, filename)
            files.append({
                "name": filename,
                "size": f"{os.path.getsize(path) / (1024*1024):.2f} MB",
                "path": path
            })
    return jsonify(files)

@app.route('/files/<filename>', methods=['GET'])
def get_file(filename):
    # This allows the "Download to browser" option
    return send_from_directory(DEST_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    print(f"🚀 Navan YT Downloader Server running on http://localhost:5000")
    print(f"📂 Destination: {DEST_FOLDER}")
    app.run(
    host="0.0.0.0",
    port=8000,
    debug=True,
    use_reloader=True
    )

@app.route("/")
def home():
    return render_template("index.html")