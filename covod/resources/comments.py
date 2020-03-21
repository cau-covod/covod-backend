from flask_restful import Resource, fields, marshal_with
from sqlalchemy import and_, or_, func

from covod.models.models import User, Lecture, db, Course, Comment

user_fields = {
    "id": fields.Integer,
    "username": fields.String,
    "full_name": fields.String
}

comment_fields = {
    "id": fields.Integer,
    "created_at": fields.DateTime(dt_format="iso8601"),
    "modified_at": fields.DateTime(dt_format="iso8601"),
    "timestamp": fields.Integer,
    "text": fields.String,
    "path": fields.String,
    "user": fields.Nested(user_fields)
}

comment_fields_recursive = comment_fields.copy()
comment_fields_recursive["replies"] = fields.List(fields.Nested(comment_fields_recursive))


class Comments(Resource):
    @marshal_with(comment_fields_recursive, envelope="comments")
    def get(self, lecture_id):
        return Comment.query.filter_by(lecture_id=lecture_id).filter(
            func.length(Comment.path) == Comment.get_n()).all()


class CommentsFlat(Resource):
    @marshal_with(comment_fields, envelope="comments")
    def get(self, lecture_id):
        return Comment.query.filter_by(lecture_id=lecture_id).all()
