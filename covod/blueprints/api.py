from flask import Blueprint
from flask_restful import Api

from covod.resources.foo import Foo
from covod.resources.lecture import LectureMedia
from covod.resources.user_feed import UserFeed

bp = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(bp)

api.add_resource(Foo, "/foo", "/foo/<string:id>")
api.add_resource(LectureMedia, "/lecture/<int:id>/media")
api.add_resource(UserFeed, "/user/<int:user_id>/feed")
