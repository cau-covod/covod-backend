from authlib.integrations.flask_oauth2 import current_token
from flask_restful import Resource, fields, marshal_with

from covod.models.models import User, Lecture, Course, Media
from covod.oauth2 import require_oauth

media_fields = {
    "length": fields.Integer,
    "thumbnail": fields.String
}

lecture_fields = {
    "id": fields.Integer,
    "number": fields.Integer,
    "created_at": fields.DateTime(dt_format="iso8601"),
    "description": fields.String,
    "comment_count": fields.Integer,
    "media": fields.Nested(media_fields)
}

course_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "lectures": fields.List(fields.Nested(lecture_fields))
}

feed_fields = {
    "courses": fields.List(fields.Nested(course_fields))
}


class UserFeed(Resource):
    @require_oauth("view")
    @marshal_with(feed_fields, envelope="feed")
    def get(self):
        user = User.query.filter_by(id=current_token.user_id).first_or_404()
        feed = user.query.join(Course, User.courses).join(Lecture).all()
        return feed
