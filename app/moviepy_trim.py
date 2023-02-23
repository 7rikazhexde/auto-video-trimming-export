from moviepy.editor import *
from log import LogProccess
import toml

class ExeMovieyPy:
    def __init__(self,logger):
        """
        ExeMovieyPy class constructor

        Parameters
        ----------
        logger : LogProccess
            Instance variable of LogProccess class
            Used for log output
        """
        self.__logger = logger

    def trim_video(self, file_path, export_file, start, end, fps):
        """
        Video trimming process

        Parameters
        ----------
        file_path
            Path of video file to be trimmed (.mov or .mp4)
        export_file
            Path to output video after trimming process
        start
            Trimming start position
        end
            Trimming end position
        fps
            Frame rate

        Raises:
        -------
            check_output method, and errors in AppleScript execution are handled as built-in exceptions in Exception

        See Also
        -------
        moviepy.video.VideoClip.VideoClip
        """
        self.__logger.info(f'Start MovieyPy Execution')
        try:
            video_clip = VideoFileClip(file_path).subclip(start, end)
        except Exception as e:
            self.__logger.error(e)
            sys.exit()

        try:
            vide_clip_resized = video_clip.resize(height=360) 
        except Exception as e:
            self.__logger.error(e)
            sys.exit()

        try:
            vide_clip_resized.write_videofile(export_file,fps,codec='libx264',audio_codec='aac',threads=4)
        except Exception as e:
            self.__logger.error(e)
            sys.exit()

        self.__logger.info(f'Execution MovieyPy Complete')

if __name__ == '__main__':
    file_path = './media/test.mp4'
    export_file = './media/test_trim.mp4'
    start = 50
    end = 100
    fps = 30

    with open('./setting.toml') as f:
        toml_obj = toml.load(f)

    log_process = LogProccess()
    log_process.logging_info = toml_obj
    logger = log_process.logging_info

    exe_moviepy = ExeMovieyPy(logger)
    exe_moviepy.trim_video(file_path, export_file, start, end, fps)