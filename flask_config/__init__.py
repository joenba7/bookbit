import os
from flask import Flask
from flask_config.logic.auth import inject_globals
from flask_config.views.index import bp_index
from flask_config.views.files import bp_files

def create_app():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    template_dir = os.path.join(base_dir, "..", "layout")
    static_dir = os.path.join(base_dir, "..", "static")

    app = Flask(
        __name__,
        template_folder=template_dir,
        static_folder=static_dir
    )

    app.secret_key = b'supersecret'
    app.context_processor(inject_globals)

    app.register_blueprint(bp_index)
    app.register_blueprint(bp_files, url_prefix="/books")

    return app
