import os

import cv2
from flask import Flask, jsonify
from flask_cors import cross_origin

app = Flask(__name__)


def is_preview(video_name: str):
    print(video_name)
    image_name = video_name.rstrip('.mp4') + ".jpg"
    if image_name in os.listdir('../media/preview/'):
        return True

    try:
        vidcap = cv2.VideoCapture(video_name)
        print('created')
        success, image = vidcap.read()
        print('read ok')
        if not success:
            return False

        cv2.imwrite(image_name, image)
        vidcap.release()
        return True
    except Exception as e:
        print(e)
        return False


@app.route('/list')
@cross_origin()
def video_list():
    lst = os.listdir('./media')
    lst = sorted(lst, key=lambda e: float(str(e).rstrip('.jpg')))

    # lst = [s for s in lst if s.endswith('.mp4') and (is_preview(s) or True)]

    return jsonify(lst)


if __name__ == '__main__':
    app.run('0.0.0.0', threaded=True)
