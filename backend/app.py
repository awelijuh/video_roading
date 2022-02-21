import os
from datetime import date, datetime

import cv2
import dotenv
from flask import Flask, jsonify, Response, request
from flask.json import JSONEncoder
from flask_cors import cross_origin
from redis import Redis

app = Flask(__name__, static_url_path='/', static_folder='./static')

dotenv.load_dotenv()

ACCIDENT_PATH = os.environ.get('BACKEND_ACCIDENTS_PATH')
ACCIDENT_PREFIX_URL = os.environ.get('BACKEND_ACCIDENT_PREFIX_URL')
IMAGES_PATH = os.environ.get('BACKEND_IMAGES_PATH')
DETECTED_PATH = os.environ.get('BACKEND_DETECTED_PATH')
DETECTED_PREFIX_URL = os.environ.get('BACKEND_DETECTED_PREFIX_URL')
REDIS_HOST = os.environ.get('REDIS_HOST')
IMAGE_FORMAT = os.environ.get('IMAGE_FORMAT')
redis = Redis(host=REDIS_HOST, port=6379, db=0)


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.astimezone().isoformat()
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


@app.route('/api//accidents')
@cross_origin()
def video_list():
    lst = os.listdir(ACCIDENT_PATH)
    lst = [{'name': fl.rstrip('.mkv'), 'url': ACCIDENT_PREFIX_URL + fl} for fl in lst]
    return jsonify(lst)


def resize_to_height(img, height):
    height = int(height)
    width = img.shape[1]  # keep original width
    old_height = img.shape[0]
    width = int(width * height / old_height)
    return cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)


def gen_stream(path=DETECTED_PATH, redis_key='last_detect', size=None):
    while True:
        # lst = os.listdir(path)
        # filename = max(lst)
        filename = redis.get(redis_key).decode('utf-8')
        frame = cv2.imread(f'{path}/{filename}')
        if size is not None:
            frame = resize_to_height(frame, size)
        (flag, encodedImage) = cv2.imencode(f".{IMAGE_FORMAT}", frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/' + IMAGE_FORMAT.encode('utf-8') + b'\r\n\r\n' + bytearray(encodedImage) + b'\r\n')


@app.route('/api/detected-stream')
@cross_origin()
def detected_stream():
    return Response(gen_stream(DETECTED_PATH, redis_key='last_detect', size=request.args.get('size', None)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/api/raw-stream')
@cross_origin()
def raw_stream():
    return Response(gen_stream(IMAGES_PATH, 'last_image', size=request.args.get('size', None)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/api/stream')
@cross_origin()
def stream():
    stream_type = request.args.get('type')
    type_to_path = {
        'raw': IMAGES_PATH,
        'detected': DETECTED_PATH
    }
    type_to_redis_key = {
        'raw': 'last_image',
        'detected': 'last_detect',
    }
    return Response(gen_stream(type_to_path.get(stream_type), type_to_redis_key.get(stream_type),
                               size=request.args.get('size', None)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def cast_or_none(m_type, value):
    try:
        return m_type(value)
    except Exception:
        return None


@app.route('/api/params')
@cross_origin()
def get_params():
    d = {
        'read_fps': cast_or_none(float, redis.get('read_fps').decode("utf-8")),
        'yolo_time': cast_or_none(float, redis.get('yolo_time').decode("utf-8")),
        'deep_sort_time': cast_or_none(float, redis.get('deep_sort_time').decode("utf-8")),
        'detect_fps': cast_or_none(float, redis.get('detect_fps').decode("utf-8")),
    }
    return jsonify(d)


app.json_encoder = CustomJSONEncoder


def run():
    app.run('0.0.0.0', threaded=True)


if __name__ == '__main__':
    run()
