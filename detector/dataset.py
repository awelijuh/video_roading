import time

import cv2
import numpy as np

from Yolov5_DeepSort_Pytorch.yolov5.utils.augmentations import letterbox


class LoadMedia:
    # YOLOv5 image/video dataloader, i.e. `python detect.py --source image.jpg/vid.mp4`
    def __init__(self, path, redis, img_size=640, stride=32, auto=True):
        self.path = path
        self.redis = redis
        # self.path = '../images'
        self.img_size = img_size
        self.stride = stride
        self.auto = auto
        self.cap = None
        self.last_image = None

        self.mask = cv2.imread('mask.png', 0)
        contours, hierarchy = cv2.findContours(self.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnt = contours[0]
        self.x, self.y, self.w, self.h = cv2.boundingRect(cnt)

    def __iter__(self):
        self.count = 0
        return self

    def get_filename(self):
        result = self.redis.get('last_image')
        if result is None:
            return None
        return result.decode('utf-8')
        # files = os.listdir(self.path)
        # if files is None or len(files) == 0:
        #     return None
        # return max(files)

    def __next__(self):
        while True:
            filename = self.get_filename()
            while filename is None or filename == self.last_image:
                time.sleep(0.1)
                filename = self.get_filename()

            path = self.path + '/' + filename

            # Read image
            self.count += 1
            img0 = cv2.imread(path)  # BGR
            # img0 = numpy.fromstring(self.redis.get('last_img'))
            img0 = cv2.bitwise_and(img0, img0, mask=self.mask)
            img0 = img0[self.y:self.y + self.h, self.x:self.x + self.w]
            if img0 is None:
                continue
            s = filename

            # Padded resize
            img = letterbox(img0, self.img_size, stride=self.stride, auto=self.auto)[0]

            # Convert
            img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
            img = np.ascontiguousarray(img)

            return path, img, img0, self.cap, s

    def new_video(self, path):
        self.frame = 0
        self.cap = cv2.VideoCapture(path)
        self.frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def __len__(self):
        return self.nf  # number of files
