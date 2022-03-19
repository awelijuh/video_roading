import logging
import os
import shutil
from threading import Thread

from moviepy.editor import VideoFileClip, concatenate_videoclips

TMP_DIR = '/video_tmp'

logger = logging.getLogger('video_saver')


def chek_tmp():
    if not os.path.exists(TMP_DIR):
        os.mkdir(TMP_DIR)


def clear_tmp():
    files = os.listdir(TMP_DIR)
    for f in files:
        os.remove(os.path.join(TMP_DIR, f))


class VideoSaver:
    def __init__(self, redis, video_path, save_dir):
        super().__init__()
        self.is_save = False
        self.redis = redis
        self.video_path = video_path
        self.save_dir = save_dir
        self.thread = None

    def save_video(self):
        if self.is_save:
            return
        self.thread = Thread(target=self.run, daemon=True)
        self.thread.start()

    def run(self) -> None:
        self.is_save = True
        logger.info('begin video saver')
        if self.redis is not None:
            self.redis.set('is_saving', 1)
        save_accident_video(self.video_path, self.save_dir)
        logger.info('end video saver')
        if self.redis is not None:
            self.redis.set('is_saving', 0)
        self.is_save = False


def save_accident_video(video_path, save_dir):
    try:
        chek_tmp()
        clear_tmp()
        files = os.listdir(video_path)
        files = files[(len(files) // 2):-1]
        files.sort()
        videos_files = []
        for f in files:
            if not f.endswith('.avi'):
                continue
            shutil.copyfile(os.path.join(video_path, f), os.path.join(TMP_DIR, f))
            videos_files.append(os.path.join(TMP_DIR, f))

        videos = []
        for f in videos_files:
            try:
                videos.append(VideoFileClip(f))
            except Exception as e:
                # logger.error('error open video, ' + str(e))
                logger.error('video read error, file=' + f + ', error=' + str(e))
        if len(videos) == 0:
            logger.info('videos 0')
            return
        out = concatenate_videoclips(videos)
        out.write_videofile(save_dir + '/' + files[0].replace('avi', 'mkv'), codec='libx264')
    except Exception as e:
        logger.error('save_accident_video error, ' + str(e))
