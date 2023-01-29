from moviepy.editor import *

def trim_video(file_path,export_file,start,end,fps):
    # ビデオのカット開始
    video_clip = VideoFileClip(file_path).subclip(start, end)
    vide_clip_resized = video_clip.resize(height=360) 
    vide_clip_resized.write_videofile(export_file,fps,codec='libx264',audio_codec='aac',threads=4)

if __name__ == '__main__':
    # 編集したい動画のパス
    file_path = './media/test.mp4'
    # 編集後のファイル保存先のパス
    export_file = './media/test_trim.mp4'
    # 切り出し開始時刻。秒で表現
    start = 50
    # 切り出し終了時刻。同じく秒で表現
    end = 250
    fps = 30
    trim_video(file_path, export_file, start, end, fps)