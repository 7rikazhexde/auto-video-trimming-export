from moviepy.editor import *

def trim_video(file_path,export_file,start,end,fps):
    # Start cutting video
    video_clip = VideoFileClip(file_path).subclip(start, end)
    vide_clip_resized = video_clip.resize(height=360) 
    vide_clip_resized.write_videofile(export_file,fps,codec='libx264',audio_codec='aac',threads=4)

if __name__ == '__main__':
    # Media path
    file_path = './media/test.mp4'
    # Export path
    export_file = './media/test_trim.mp4'
    # Cutout start time (sec)
    start = 50
    # Cutout end time (sec)
    end = 250
    fps = 30
    trim_video(file_path, export_file, start, end, fps)