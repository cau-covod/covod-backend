from flask import Blueprint

from covod.oauth2 import authorization, require_oauth

bp = Blueprint("auth", __name__, url_prefix="/oauth2")


@bp.route("/token", methods=["POST"])
def issue_token():
    return authorization.create_token_response()


@bp.route("/revoke", methods=["POST"])
def revoke_token():
    return authorization.create_endpoint_response("revocation")


@bp.route("/check_token", methods=["POST"])
@require_oauth("upload")
def check_token():
    return "Working! \o/"
