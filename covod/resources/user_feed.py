from flask_restful import Resource, fields, marshal_with

from covod.models.models import User, Lecture, db, Course

lecture_fields = {
    "id": fields.Integer,
    "number": fields.Integer,
    "pub_time": fields.DateTime(dt_format="iso8601"),
    "description": fields.String
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
    @marshal_with(feed_fields, envelope="feed")
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first_or_404()
        feed = user.query.join(Course, User.courses).join(Lecture).all()
        return feed
