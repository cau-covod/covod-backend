import uuid, fnmatch

from flask import request, Response
from flask_restful import Resource
from flask_cloudy import Storage

from covod.models.models import PDF, Lecture, MediaType, Media, db
from covod.oauth2 import require_oauth

storage = Storage()

class LectureMedia(Resource):
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
        file = request.files['file']
        # TODO test if lecture belongs to user
        lecture = Lecture.query.filter_by(id=id).first_or_404()
        print(lecture)
        media_uuid = uuid.uuid4()

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

        return {'name': upload.name, 'extension': upload.extension, 'size': upload.size, 'url': upload.url}


class LecturePDF(Resource):
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

    def post(self, id):
        file = request.files['file']
        # TODO test if lecture belongs to user
        lecture = Lecture.query.filter_by(id=id).first_or_404()
        print(lecture)
        pdf_uuid = uuid.uuid4()

        upload = storage.upload(file, name=str(pdf_uuid), prefix=f"{lecture.course.uuid}/", extensions=["pdf"])

        pdf = PDF(uuid=pdf_uuid, lecture=lecture, extension=upload.extension)
        db.session.add(pdf)
        db.session.commit()

        return {'name': upload.name, 'extension': upload.extension, 'size': upload.size, 'url': upload.url}


class LectureTimestamps(Resource):
    def get(self):
        pass

    def post(self):
        pass
