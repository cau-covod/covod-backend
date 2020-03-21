from flask import Blueprint
from flask_restful import Api

from covod.resources.foo import Foo
from covod.resources.lecture import LectureMedia

bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(bp)

api.add_resource(Foo, "/foo", "/foo/<string:id>")
api.add_resource(LectureMedia, "/lecture/<int:id>/media")