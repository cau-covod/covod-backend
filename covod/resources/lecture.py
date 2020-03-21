from flask import request
from flask_restful import Resource
from flask_cloudy import Storage

storage = Storage()

UPLOAD_DIRECTORY='media'

class LectureMedia(Resource):
    def get(self, id=-1):
        return "Got id " + str(id)
    def post(self, id=-1):
        file = request.files['file']
        print(file)
        upload = storage.upload(file, name=str(id))
        return {'name':upload.name, 'extension':upload.extension, 'size':upload.size, 'url': upload.url}

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