from flask import Blueprint

from covod.oauth2 import authorization

bp = Blueprint("auth", __name__, url_prefix="/oauth2")


@bp.route("/token", methods=["POST"])
def issue_token():
    return authorization.create_token_response()


@bp.route("/revoke", methods=["POST"])
def revoke_token():
    return authorization.create_endpoint_response("revocation")
