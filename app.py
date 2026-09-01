#!/usr/bin/env python3
"""Alpha-X — Interface web pour le téléchargement vidéo/audio.

Flask app permettant de télécharger des vidéos/audio depuis
YouTube, TikTok, Instagram, Twitter/X, et 100+ plateformes
via une interface web moderne et responsive.
"""

import os
import re
import uuid
import threading
from pathlib import Path

from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp

app = Flask(__name__)

DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)

tasks = {}


def sanitize_filename(name: str) -> str:
    """Nettoie un nom de fichier."""
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    return name[:200]


def progress_hook(task_id: str):
    """Retourne un hook de progression pour yt-dlp."""
    def hook(d):
        if task_id not in tasks:
            return
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            done = d.get("downloaded_bytes", 0)
            speed = d.get("speed")
            eta = d.get("eta")
            tasks[task_id].update({
                "state": "downloading",
                "progress": round(done / total * 100, 1) if total else 0,
                "downloaded": done,
                "total": total,
                "speed": speed,
                "eta": eta,
            })
        elif d["status"] == "finished":
            tasks[task_id].update({
                "state": "processing",
                "progress": 100,
            })
    return hook


def download_task(task_id: str, url: str, fmt: str, quality: str) -> None:
    """Exécute le téléchargement en arrière-plan."""
    if fmt == "mp4":
        selector = "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]/bv*+ba/b"
        if quality == "worst":
            selector = "wv*[ext=mp4]+wa[ext=m4a]/w[ext=mp4]/wv*+wa/w"
        opts = {
            "format": selector,
            "merge_output_format": "mp4",
            "outtmpl": str(DOWNLOAD_DIR / "%(title)s.%(ext)s"),
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
            "progress_hooks": [progress_hook(task_id)],
        }
    else:
        opts = {
            "format": "ba/wa" if quality == "worst" else "ba",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "outtmpl": str(DOWNLOAD_DIR / "%(title)s.%(ext)s"),
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
            "progress_hooks": [progress_hook(task_id)],
        }

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "video")

        files = list(DOWNLOAD_DIR.glob("*"))
        if files:
            filepath = files[0]
            tasks[task_id].update({
                "state": "done",
                "progress": 100,
                "filename": filepath.name,
                "filepath": str(filepath),
                "title": title,
            })
        else:
            tasks[task_id].update({
                "state": "error",
                "error": "Aucun fichier généré",
            })
    except Exception as e:
        tasks[task_id].update({
            "state": "error",
            "error": str(e),
        })


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/download", methods=["POST"])
def api_download():
    data = request.get_json()
    url = data.get("url", "").strip()
    fmt = data.get("format", "mp4")
    quality = data.get("quality", "best")

    if not url:
        return jsonify({"error": "URL requise"}), 400

    if not url.startswith("http"):
        return jsonify({"error": "Lien invalide (commence par http/https)"}), 400

    task_id = uuid.uuid4().hex[:12]
    tasks[task_id] = {"state": "starting", "progress": 0}

    thread = threading.Thread(target=download_task, args=(task_id, url, fmt, quality))
    thread.daemon = True
    thread.start()

    return jsonify({"task_id": task_id})


@app.route("/api/status/<task_id>")
def api_status(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": "Tâche introuvable"}), 404
    return jsonify(task)


@app.route("/api/file/<task_id>")
def api_file(task_id):
    task = tasks.get(task_id)
    if not task or task.get("state") != "done":
        return jsonify({"error": "Fichier non disponible"}), 404
    filepath = task.get("filepath")
    if not filepath or not os.path.exists(filepath):
        return jsonify({"error": "Fichier introuvable"}), 404
    return send_file(filepath, as_attachment=True, download_name=task["filename"])


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
