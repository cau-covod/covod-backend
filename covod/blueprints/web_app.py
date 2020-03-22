import os

from flask import Blueprint, send_from_directory

bp = Blueprint("web-app", __name__, url_prefix="/")


@bp.route("/", defaults={"path": ""})
@bp.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists("../web-app/" + path):
        return send_from_directory("../web-app", path)
    else:
        return send_from_directory("../web-app", "index.html")
