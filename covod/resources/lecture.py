import uuid
from http.client import HTTPException

from flask import request
from flask_restful import Resource
from flask_cloudy import Storage

from covod.models.models import Lecture, MediaType, Media, db
from covod.oauth2 import require_oauth

storage = Storage()


class LectureMedia(Resource):
    def get(self, id):
        return "Got id " + str(id)

    # If youget {"message": null} the oauth authentication failed
    # TODO: Better oauth errors
    @require_oauth("upload")
    def post(self, id):
        file = request.files['file']

        lecture = Lecture.query.filter_by(id=id).first_or_404()
        print(lecture)
        media_uuid = uuid.uuid4()

        upload = storage.upload(file, name=str(media_uuid), prefix=f"{lecture.course.uuid}/")

        media = Media(uuid=media_uuid, type=MediaType.AUDIO_VIDEO, lecture=lecture, extension=upload.extension)
        db.session.add(media)
        db.session.commit()

        return {'name': upload.name, 'extension': upload.extension, 'size': upload.size, 'url': upload.url}


class LecturePDF(Resource):
    def get(self):
        pass

    def post(self):
        pass


class LectureTimestamps(Resource):
    def get(self):
        pass

    def post(self):
        pass
