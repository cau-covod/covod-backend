from flask import Blueprint
from flask_restful import Api

from covod.resources.foo import Foo

bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(bp)

api.add_resource(Foo, "/foo", "/foo/<string:id>")
