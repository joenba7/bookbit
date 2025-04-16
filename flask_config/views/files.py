from flask import Blueprint, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import configparser
from flask_config.logic.auth import login_required

bp_files = Blueprint("files", __name__)

# Get absolute path to the books directory
config = configparser.ConfigParser()
config.read("settings.ini")

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
book_dir_rel = config.get("server", "book_dir", fallback="books")
BOOKS_DIR = os.path.join(base_dir, book_dir_rel)

@bp_files.route("/upload", methods=["POST"])
@login_required
def upload():
    files = request.files.getlist("files")
    os.makedirs(BOOKS_DIR, exist_ok=True)
    for f in files:
        if f.filename.endswith(".epub"):
            filename = secure_filename(f.filename)
            f.save(os.path.join(BOOKS_DIR, filename))
    return redirect(url_for("index.index"))

@bp_files.route("/<path:filename>")
@login_required
def serve_epub(filename):
    full_path = os.path.join(BOOKS_DIR, filename)
    print(f"📥 Serving file: {full_path}")
    if not os.path.isfile(full_path):
        print("❌ File not found!")
    return send_from_directory(BOOKS_DIR, filename, as_attachment=True)
