from flask import Blueprint
from flask_restful import Api

from covod.resources.comments import CommentsAPI, CommentsFlatAPI
from covod.resources.foo import Foo

from covod.resources.lecture import LectureMedia, LecturePDF, LectureTimestamps, LectureAPI
from covod.resources.user_feed import UserFeed

bp = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(bp)

api.add_resource(Foo, "/foo", "/foo/<string:id>")

api.add_resource(LectureAPI, "/lecture/<int:id>")
api.add_resource(LectureMedia, "/lecture/<int:id>/media")
api.add_resource(LecturePDF, "/lecture/<int:id>/pdf")
api.add_resource(LectureTimestamps, "/lecture/<int:id>/timestamps")
api.add_resource(CommentsAPI, "/lecture/<int:lecture_id>/comments")
api.add_resource(CommentsFlatAPI, "/lecture/<int:lecture_id>/comments-flat")
api.add_resource(UserFeed, "/user/<int:user_id>/feed")
