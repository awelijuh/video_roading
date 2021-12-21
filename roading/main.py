import os
import time

import cv2

url = os.getenv('VIDEO_URL')
fps = float(os.getenv('FPS', 25))
recording_delay = float(os.getenv('RECORDING_DELAY', 60 * 60 * 24))

image_save_delay = float(os.getenv('IMAGE_SAVE_DELAY', 5))

# url = 'rtsp://cam.wikilink.by/kolesnika.1.(perekrestok)-98f02d9de3?token=2.ox1MUAPxAAEABcugQZmYezCJR_MpDO5CfKWOZXkrj5y2JN45'

stream = cv2.VideoCapture(url)

frame_width = int(stream.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_size = (frame_width, frame_height)

# fps = stream.get(cv2.CAP_PROP_FPS)
# print(fps)

# fps = 25
wt = 1 / fps

print('FPS:', fps)
print('FRAME_SIZE:', frame_size)

last_save_image_time = 0

start_recording_time = time.time()
frame_start_recording_time = start_recording_time

last_user_command = None
work = True

# def input_worker():
#     global last_user_command
#     while work:
#         last_user_command = input()
#
#
# input_thread = Thread(target=input_worker)
# input_thread.start()

while True:
    # Capture frame-by-frame
    start_time = time.time()

    ret, frame = stream.read()

    if frame is not None:
        if time.time() - start_recording_time >= recording_delay:
            break

        if time.time() - last_save_image_time >= image_save_delay:
            print('save image')
            cv2.imwrite('/media/{}.jpg'.format(time.time()), frame)
            last_save_image_time = time.time()

        # if time.time() - frame_start_recording_time >= fragment_size:
        #     print('release')
        #     frame_start_recording_time = time.time()
        #     out.release()
        #     out = get_out()

        dt = time.time() - start_time
        if wt - dt > 0:
            time.sleep(wt - dt)
    else:
        print("Frame is None")
        break

# When everything done, release the capture
work = False
stream.release()
# out.release()
cv2.destroyAllWindows()

print("Video stop")
