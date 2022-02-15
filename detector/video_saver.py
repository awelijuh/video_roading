import os

from moviepy.editor import VideoFileClip, concatenate_videoclips


def save_accident_video(video_path, save_dir):
    try:
        files = os.listdir(video_path)
        files = files[(len(files) // 2):-1]
        files.sort()
        videos = []
        for f in files:
            if not f.endswith('.mkv'):
                continue
            videos.append(VideoFileClip(video_path + '/' + f))
        out = concatenate_videoclips(videos)
        out.write_videofile(save_dir + '/' + files[0], codec='libx264')
    except Exception as e:
        print(e)
