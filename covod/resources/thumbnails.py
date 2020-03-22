import json, cv2, os
from threading import Thread
from flask import Response
from flask_restful import Resource
from covod.oauth2 import require_oauth
from covod.models.models import Lecture

class LectureThumbnail(Resource):
    @require_oauth("view")
    def get(self, id, tid):
        lecture = Lecture.query.filter_by(id=id).first_or_404()
        thumbnail_path = "media/" + str(lecture.course.uuid) + "/" + str(lecture.media.uuid) + "/" + str(tid) + ".jpg"
        try:
            file = open(thumbnail_path, "rb")
        except (OSError, IOError) as e:
            return "Not Found", 404, {}
        response = Response(file.read())
        response.headers['content-type'] = 'image/jpeg'
        return response

class LectureThumbnails(Resource):
    @require_oauth("view")
    def get(self, id):
        lecture = Lecture.query.filter_by(id=id).first_or_404()
        thumbnail_path = "media/" + str(lecture.course.uuid) + "/" + str(lecture.media.uuid)
        tids = []
        try:
            for f in os.listdir(thumbnail_path):
                tid = int(f.split('.')[0])
                tids.append(tid)
            tids.sort()
            return tids
        except (OSError, IOError) as e:
            return "Not Found", 404, {}

# Thumbnails for timestamps aren't generated if a timestamp is less than TIME_THRESHOLD seconds from the previous timestamp
TIME_THRESHOLD = 3 

def _generateThumbnails(course_uuid, media_uuid, media_extension, timestamps_json):
    print("GENERATING THUMBNAILS")
    filename = "media/" + str(course_uuid) + "/" + str(media_uuid) + "." + media_extension
    timestamps = json.loads(timestamps_json)
    print("filename: ", filename)
    print("timestamps: ", timestamps)

    thumbnail_path = "media/" + str(course_uuid) + "/" + str(media_uuid)
    try: 
        if not os.path.exists(thumbnail_path): 
            os.makedirs(thumbnail_path)
    except OSError: 
        print ('Error: Creating directory of data') 

    vid = cv2.VideoCapture(filename)
    fps = vid.get(cv2.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
    frame_count = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count/fps

    print('fps = ' + str(fps))
    print('number of frames = ' + str(frame_count))
    print('duration (S) = ' + str(duration))
    minutes = int(duration/60)
    seconds = duration%60
    print('duration (M:S) = ' + str(minutes) + ':' + str(seconds))

    prev_time = -float("Inf")
    for timestamp in [{"time": 0}] + timestamps:
        # print(timestamp)
        time = timestamp['time']
        if (time - prev_time) >= TIME_THRESHOLD:
            # if time in timestamps_finished:
            #     continue
            vid.set(cv2.CAP_PROP_POS_MSEC, time * 1000)
            succ, img = vid.read()
            if succ:
                cv2.imwrite(thumbnail_path + "/"+ str(time) + ".jpg", img)
            else:
                print("Couldn't generate thumbnail!")
            # timestamps_finished.append(time)
            print("finished thumbnail for second "+str(time))
        prev_time = time

    vid.release()

    # TODO save in database

    return


def generateThumbnails(lecture):
    Thread(target=_generateThumbnails, args=(lecture.course.uuid, lecture.media.uuid, lecture.media.extension, lecture.timestamps.json, )).start()