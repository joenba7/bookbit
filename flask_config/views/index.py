from flask import Blueprint, render_template, request
from flask_config.logic.auth import login_required
from flask_config.logic.fileops import list_books
import configparser

bp_index = Blueprint("index", __name__)

config = configparser.ConfigParser()
config.read("settings.ini")

@bp_index.route("/")
@login_required
def index():
    sort_by = request.args.get("sort_by", config.get("display", "sort_by"))
    sort_order = request.args.get("sort_order", config.get("display", "sort_order"))
    query = request.args.get("q", "")
    files = list_books(query, sort_by, sort_order)
    return render_template("body.html", files=files, search_query=query,
                           sort_by=sort_by, sort_order=sort_order,
                           show_size=config.getboolean("display", "show_size"),
                           show_modified=config.getboolean("display", "show_modified"),
                           hide_ext=config.getboolean("display", "hide_extensions"))
