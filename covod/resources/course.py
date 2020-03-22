import uuid, fnmatch, json

# from flask import request, Response
from flask_restful import Resource, fields, marshal_with
# from flask_restful.reqparse import RequestParser
# from flask_cloudy import Storage

from authlib.integrations.flask_oauth2 import current_token

from covod.models.models import Course, User, Lecture # Timestamps, PDF, Lecture, Course, MediaType, Media, db
from covod.oauth2 import require_oauth

course = {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.String,
    "user_id": fields.Integer
}

class CourseAPI(Resource):
    @require_oauth("view")
    @marshal_with(course)
    def get(self):
        courses = Course.query.filter_by(user_id=current_token.user_id).all()
        return courses
