from flask import Flask
from flask-config.logic.auth import inject_globals
from flask-config.views.index import bp_index
from flask-config.views.files import bp_files

def create_app():
    app = Flask(__name__)
    app.secret_key = b'supersecret'
    app.context_processor(inject_globals)
    app.register_blueprint(bp_index)
    app.register_blueprint(bp_files)
    return app
