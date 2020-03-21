from flask import Blueprint
from flask_restful import Api

from covod.resources.foo import Foo
from covod.resources.lecture import LectureMedia, LecturePDF, LectureTimestamps, LectureAPI

bp = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(bp)

api.add_resource(Foo, "/foo", "/foo/<string:id>")

api.add_resource(LectureAPI, "/lecture")
api.add_resource(LectureMedia, "/lecture/<int:id>/media")
api.add_resource(LecturePDF, "/lecture/<int:id>/pdf")
api.add_resource(LectureTimestamps, "/lecture/<int:id>/timestamps")