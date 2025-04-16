from flask import session, redirect, url_for
from functools import wraps
import bcrypt
import configparser

config = configparser.ConfigParser()
config.read("settings.ini")

ENABLE_AUTH = config.getboolean("auth", "enable", fallback=False)
PASSWORD_HASH = config.get("auth", "password_hash", fallback="")

def check_password(password):
    return bcrypt.checkpw(password.encode("utf-8"), PASSWORD_HASH.encode("utf-8"))

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if ENABLE_AUTH and not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

def inject_globals():
    return dict(auth_enabled=ENABLE_AUTH, logged_in=session.get("logged_in", False))
