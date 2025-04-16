import os
from datetime import datetime
import configparser

config = configparser.ConfigParser()
config.read("settings.ini")
BOOKS_DIR = config.get("server", "book_dir", fallback="books")

def list_books(query, sort_by, sort_order):
    files = []
    for name in os.listdir(BOOKS_DIR):
        if not name.endswith(".epub"):
            continue
        if query and query.lower() not in name.lower():
            continue
        path = os.path.join(BOOKS_DIR, name)
        stat = os.stat(path)
        files.append({
            "name": name,
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime)
        })
    reverse = sort_order == "desc"
    files.sort(key=lambda x: x[sort_by], reverse=reverse)
    return files
