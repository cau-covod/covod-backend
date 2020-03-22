from authlib.integrations.flask_oauth2 import current_token
from flask_restful import Resource, fields, marshal_with, reqparse
from sqlalchemy import func

from covod.models.models import User, Lecture, db, Comment

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


class CommentsAPI(Resource):
    @marshal_with(comment_fields_recursive, envelope="comments")
    def get(self, lecture_id):
        return Comment.query.filter_by(lecture_id=lecture_id).filter(
            func.length(Comment.path) == Comment.get_n()).all()

    @marshal_with(comment_fields_recursive, envelope="comments")
    def put(self, lecture_id):
        lecture = Lecture.query.filter_by(id=lecture_id).first_or_404()
        user = User.query.filter_by(id=1).first()

        parser = reqparse.RequestParser()
        parser.add_argument("text", required=True, help="No comment text provided")
        parser.add_argument("parent", type=int)
        parser.add_argument("timestamp", type=int)
        args = parser.parse_args()

        comment = Comment(user=user, text=args.text, parent=args.parent,
                          timestamp=args.timestamp, lecture_id=lecture_id
                          )

        # Use comment.save()to generate path
        comment.save()

        lecture.add_comment(comment)
        db.session.commit()
        return comment


class CommentsFlatAPI(Resource):
    @marshal_with(comment_fields, envelope="comments")
    def get(self, lecture_id):
        return Comment.query.filter_by(lecture_id=lecture_id).all()
