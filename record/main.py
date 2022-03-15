import os
import queue
import time

import cv2
import numpy
import pafy
from dotenv import load_dotenv
from redis import Redis

load_dotenv()

url = os.environ.get('VIDEO_URL')

IMAGE_PATH = os.environ.get('IMAGE_RECORDING_DIR')
VIDEO_PATH = os.environ.get('VIDEO_RECORDING_DIR')
VIDEO_FPS = int(os.environ.get('VIDEO_FPS'))

MAX_IMAGES = int(os.environ.get('RECORDING_MAX_IMAGES'))
VIDEO_DURATION = int(os.environ.get('RECORDING_VIDEO_DURATION'))
MAX_VIDEOS = int(os.environ.get('RECORDING_MAX_VIDEOS'))
VIDEOS_SAVE_QUALITY = int(os.environ.get('RECORDING_VIDEOS_SAVE_QUALITY'))
REDIS_HOST = os.environ.get('REDIS_HOST')
IMAGE_FORMAT = os.environ.get('IMAGE_FORMAT')
YOUTUBE_QUALITY = os.environ.get('YOUTUBE_QUALITY')
redis = Redis(host=REDIS_HOST, port=6379, db=0)

import threading


class VideoCapture:

    def __init__(self, name):
        self.cap = cv2.VideoCapture(name)
        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    # read frames as soon as they are available, keeping only most recent one
    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()  # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            self.q.put(frame)

    def read(self):
        return self.q.get()


def resize_to_height(img, height):
    height = int(height)
    width = img.shape[1]  # keep original width
    old_height = img.shape[0]
    width = int(width * height / old_height)
    return cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)


class FrameSaver:
    def __init__(self, fps, width, height):
        if not os.path.exists(IMAGE_PATH):
            os.makedirs(IMAGE_PATH)
        if not os.path.exists(VIDEO_PATH):
            os.makedirs(VIDEO_PATH)

        self.fps = fps
        self.width = width
        self.height = height
        self.video_writer = None
        self.video_start = None

    def create_writer(self, tt):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_writer = cv2.VideoWriter(f'{VIDEO_PATH}/{tt}.mkv', fourcc, self.fps, (self.width, self.height))
        self.video_start = tt

    def next_frame(self, frame: numpy.ndarray):
        t = time.time()
        image_name = f'{t}.{IMAGE_FORMAT}'
        image_path = f'{IMAGE_PATH}/{image_name}'
        cv2.imwrite(image_path, frame)
        redis.set('last_image', image_name)
        # redis.set('last_img', frame.tostring())

        images = os.listdir(IMAGE_PATH)
        images.sort(reverse=True)
        for frame_to_remove in images[MAX_IMAGES:]:
            os.remove(f'{IMAGE_PATH}/{frame_to_remove}')

        if self.video_writer is None:
            self.create_writer(t)

        self.video_writer.write(resize_to_height(frame, VIDEOS_SAVE_QUALITY))

        if t - self.video_start >= VIDEO_DURATION:
            self.video_writer.release()
            self.video_writer = None
            print(f'release {self.video_start} - {t}, d: {t - self.video_start}')

            videos = os.listdir(VIDEO_PATH)
            videos.sort(reverse=True)
            for video_to_remove in videos[MAX_VIDEOS:]:
                os.remove(f'{VIDEO_PATH}/{video_to_remove}')


def get_stream():
    r_url = url
    if 'youtube.com' in r_url:
        video = pafy.new(r_url)
        streams = [v for v in video.streams if v.extension == 'mp4' and v.quality.endswith(YOUTUBE_QUALITY)]

        # best = video.getworst(preftype="mp4")
        r_url = streams[0].url

    return cv2.VideoCapture(r_url)


class Road:
    def __init__(self, fps=VIDEO_FPS):
        self.stream = get_stream()
        self.stream.set(cv2.CAP_PROP_BUFFERSIZE, 0)
        cap = self.stream
        self.fps = fps
        if self.fps is None:
            self.fps = float(cap.get(cv2.CAP_PROP_FPS))

        self.frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.frame_size = (self.frame_width, self.frame_height)

        print('FPS:', self.fps)
        print('FRAME_SIZE:', self.frame_size)
        self.wt = 1 / self.fps

        self.last_save_image_time = 0

        self.start_recording_time = time.time()
        self.frame_start_recording_time = self.start_recording_time

        self.none_frame_count = 0  # число пустых фреймов
        self.none_frame_to_restart_count = 10  # через сколько пустых фреймов перезапустить стрим
        self.restart_count = 0  # число сделаных перезапусков
        self.restart_none_frame_to_finish_count = 10000  # через сколько неудачных перезапусков завешить программу

        self.real_fps = 0
        self.is_road = None

        self.saver = FrameSaver(self.fps, self.frame_width, self.frame_height)

    def start_road(self):
        self.is_road = True
        while self.is_road:
            self.next_frame()

    def next_frame(self):
        start_time = time.time()

        ret, frame = self.stream.read()

        if frame is not None:

            t = time.time()

            self.saver.next_frame(frame)

            self.real_fps = (1 / (t - self.last_save_image_time))
            redis.set('read_fps', str(self.real_fps))
            self.last_save_image_time = t

            self.none_frame_count = 0
            self.restart_count = 0
            dt = time.time() - start_time
            if self.wt - dt > 0:
                time.sleep(self.wt - dt)
        else:
            print('frame None')
            self.none_frame_count += 1
            redis.set('read_fps', 0)

        if self.restart_count >= self.restart_none_frame_to_finish_count:
            self.is_road = False
            redis.set('read_fps', 0)
            return

        if self.none_frame_count >= self.none_frame_to_restart_count:
            self.stream = get_stream()
            self.none_frame_count = 0
            self.restart_count += 1
            redis.set('read_fps', 0)
            time.sleep(4)


if __name__ == '__main__':
    r = Road()
    r.start_road()
    print("Video stop")
