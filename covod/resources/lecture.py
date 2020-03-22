import uuid, fnmatch, json

from flask import request, Response
from flask_restful import Resource, reqparse, fields, marshal_with
from flask_restful.reqparse import RequestParser
from flask_cloudy import Storage

from authlib.integrations.flask_oauth2 import current_token

from covod.models.models import Timestamps, PDF, Lecture, Course, MediaType, Media, db
from covod.oauth2 import require_oauth
from covod.resources.thumbnails import generateThumbnails

storage = Storage()

lecture = {
        "id":fields.Integer,
        "number":fields.Integer,
        "pub_time":fields.DateTime(dt_format="iso8601"),
        "name":fields.String,
        "course_id":fields.Integer
}

class LectureAPI(Resource):
    @require_oauth("upload")
    @marshal_with(lecture)
    def put(self, id=0):
        parser = reqparse.RequestParser()
        parser.add_argument('course_id', type=int)
        parser.add_argument('number', type=int)
        parser.add_argument('name', type=str)
        args = parser.parse_args()

        course = Course.query.filter_by(id=args['course_id']).first_or_404()
        if not (current_token.user_id == course.user_id):
            return "Unauthorized", 401, {}
        
        lecture = Lecture(number=args['number'], name=args['name'], course=course)
        db.session.add(lecture)
        db.session.commit()
        
        return lecture, 201, {}

    @require_oauth("view")
    @marshal_with(lecture)
    def get(self, id):
        return Lecture.query.filter_by(id=id).first_or_404();



class LectureMedia(Resource):
    @require_oauth("view")
    def get(self, id):
        # TODO: use cloudy storage with S3
        # obj = storage.get(str(id)+".mp3")
        # print(obj)
        # url = file.download_url()
        # print(url)

        lecture = Lecture.query.filter_by(id=id).first_or_404()
        
        filename = "media/" + str(lecture.course.uuid) + "/" + str(lecture.media.uuid) + "." + lecture.media.extension
        
        file = open(filename, "rb")
        response = Response(file.read())
        if lecture.media.extension == "mp3":
            response.headers['content-type'] = 'audio/mp3'
        elif lecture.media.extension == "mp4":
            response.headers['content-type'] = 'video/mp4'
        else:
            raise ValueError("[GET lecture media]: File has unsupported extension")
        return response

    # If you get {"message": null} the oauth authentication failed
    # TODO: Better oauth errors
    @require_oauth("upload")
    def post(self, id):
        lecture = Lecture.query.filter_by(id=id).first_or_404()
        print(lecture)

        if not (current_token.user_id == lecture.course.user_id):
            return "Unauthorized", 401, {}

        media_uuid = uuid.uuid4()
        file = request.files['file']
        upload = storage.upload(file, name=str(media_uuid), prefix=f"{lecture.course.uuid}/", extensions=["mp3", "mp4"])

        media_type = None
        if (file.mimetype.split('/')[0] == "audio"):
            media_type = MediaType.AUDIO_ONLY
        elif (file.mimetype.split('/')[0] == "video"):
            media_type = MediaType.AUDIO_VIDEO
        else:
            return "Unsupported mimetype", 400, {}

        media = Media(uuid=media_uuid, type=media_type, lecture=lecture, extension=upload.extension)
        db.session.add(media)
        db.session.commit()

        print("lecture.timestamps:", lecture.timestamps)
        if lecture.timestamps:
            generateThumbnails(lecture)

        return {'name': upload.name, 'extension': upload.extension, 'size': upload.size, 'url': upload.url}, 201, {}


class LecturePDF(Resource):
    @require_oauth("view")
    def get(self, id):
        # TODO: use cloudy storage with S3
        # obj = storage.get(str(id)+".mp3")
        # print(obj)
        # url = file.download_url()
        # print(url)

        lecture = Lecture.query.filter_by(id=id).first_or_404()
        
        filename = "media/" + str(lecture.course.uuid) + "/" + str(lecture.pdf.uuid) + ".pdf"
        
        file = open(filename, "rb")
        response = Response(file.read())
        response.headers['content-type'] = 'application/pdf'
        return response
    
    @require_oauth("upload")
    def post(self, id):
        lecture = Lecture.query.filter_by(id=id).first_or_404()
        print(lecture)

        if not (current_token.user_id == lecture.course.user_id):
            return "Unauthorized", 401, {}

        pdf_uuid = uuid.uuid4()
        file = request.files['file']
        upload = storage.upload(file, name=str(pdf_uuid), prefix=f"{lecture.course.uuid}/", extensions=["pdf"])

        pdf = PDF(uuid=pdf_uuid, lecture=lecture)
        db.session.add(pdf)
        db.session.commit()

        return {'name': upload.name, 'extension': upload.extension, 'size': upload.size, 'url': upload.url}, 201, {}


class LectureTimestamps(Resource):
    @require_oauth("view")
    def get(self, id):
        lecture = Lecture.query.filter_by(id=id).first_or_404()
        if not lecture.timestamps:
            return []
        else:
            return json.loads(lecture.timestamps.json)

    @require_oauth("upload")
    def post(self, id):
        lecture = Lecture.query.filter_by(id=id).first_or_404()
        
        if not (current_token.user_id == lecture.course.user_id):
            return "Unauthorized", 401, {}
        
        timestamp_uuid = uuid.uuid4()
        print(request.data)
        timestamps_json = request.data.decode("utf-8")

        # TODO validate json before saving

        timestamp = Timestamps(uuid=timestamp_uuid, json=timestamps_json, lecture=lecture)
        db.session.add(timestamp)
        db.session.commit()

        print("lecture.media:", lecture.media)
        if lecture.media:
            generateThumbnails(lecture)

        return "Created", 201, {}