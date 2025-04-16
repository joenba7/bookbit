from flask import Blueprint, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
import configparser
from flask-config.logic.auth import login_required

bp_files = Blueprint("files", __name__)
config = configparser.ConfigParser()
config.read("settings.ini")
BOOKS_DIR = config.get("server", "book_dir", fallback="books")

@bp_files.route("/upload", methods=["POST"])
@login_required
def upload():
    files = request.files.getlist("files")
    for f in files:
        if f.filename.endswith(".epub"):
            f.save(os.path.join(BOOKS_DIR, secure_filename(f.filename)))
    return redirect(url_for("index.index"))

@bp_files.route("/books/<filename>")
@login_required
def download(filename):
    return send_from_directory(BOOKS_DIR, filename, as_attachment=True)
