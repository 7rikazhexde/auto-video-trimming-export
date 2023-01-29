import cv2, platform, toml
from os.path import dirname, basename, splitext
from analyze import analyze_frame
from moviepy.editor import *
from moviepy_trim import trim_video
from exe_applescript import execute_applescript

class VideoEdit:
    def __init__(self,file_path):
        self.__file_path = file_path
        self.__dname = dirname(self.__file_path )
        self.__fname = basename(self.__file_path )
        self.__file_name = splitext(self.__fname)[0]
        self.__extension = splitext(self.__fname)[1]
        print(f'VideoEdit - media_dir: {self.__dname}, input_file_name: {self.__fname}')
        self.__capture = cv2.VideoCapture(self.__file_path )
        self.__fps = self.__capture.get(cv2.CAP_PROP_FPS)
        self.__timestamp_list = []
        print(f'VideoEdit - fps: {self.__fps}\n')
        self.__pf = platform.system()
    
    def parse_video(self):
        # Counter for frame
        count = 0
        # Create an empty list of time information to be saved after analysis
        analyzed_frame_list = []

        #print('-------- Analyze Start --------')
        while True:
            # Get Frame
            ret, frame = self.__capture.read()
            # If not readable, exit the loop.
            if not ret:
                break
            # Processes a frame every second.
            if int(count % self.__fps) == 0:
                frame_num = int(count / self.__fps)
                # Analyze frames (image data)
                mean = int(analyze_frame(frame))
                #print(f'parse_video - Frame: {frame_num} mean: {mean}')
                # Create time information from specific frames from analysis results
                if(mean == 0):
                    # Exporting frames
                    # cv2.imwrite(f"./media/images/{frame_num:02}.png", frame)
                    # Get the current elapsed time (milliseconds) of the video
                    # timestamp = self.__capture.get(cv2.CAP_PROP_POS_MSEC)
                    # Convert milliseconds to seconds
                    # timestamp = str(timestamp / 1000)
                    # print(f'parse_video - Frame: {frame_num} mean: {mean}')
                    # print(f'parse_video - timestamp: {timestamp}sec')
                    analyzed_frame_list.append(frame_num)
            count += 1
        print('VideoEdit.parse_video - analyzed_frame_list:',analyzed_frame_list)
        # Last frame
        last_frame_num = frame_num
        print('VideoEdit.parse_video - last_frame_num:',last_frame_num)

        # Create a list of start and end times to be specified in trim processing from analysis results (frames)
        for i in range(len(analyzed_frame_list)):
            if i == 0:
                # the first time list
                # Start time is set to 0
                self.__timestamp_list.append([0, analyzed_frame_list[i]])
            else:
                # After the first time list
                # Shift the start time by 1 second.
                self.__timestamp_list.append([analyzed_frame_list[i-1]+1, analyzed_frame_list[i]])
            # Last start time is created from the last frame information that has already been analyzed.
            unique_last_frame_num = analyzed_frame_list[i]
        # Create last time list for trim process
        self.__timestamp_list.append([unique_last_frame_num, last_frame_num])
        print('VideoEdit.parse_video - timestamp_list:',self.__timestamp_list)
        print('VideoEdit.parse_video - Analyze End & Trim Data Created\n')
        return self.__timestamp_list

    # Trim Process
    def save_cut_video(self,time_list):
        num = 0
        cwd = os.getcwd()
        input_file = f' {cwd}/media/{self.__file_name}{self.__extension}'
        # If you want to use MoviePy on a Mac, change self.__pf to something other than Darwin.
        #self.__pf = ''
        for i in range(len(time_list)):
            for j in range(2):
                if(j == 0):
                    start = time_list[i][j]
                else:
                    end = time_list[i][j]
            if(start != end):
                num = num + 1
                print(f'VideoEdit.save_cut_video - Data{num}: Trim Process Start')
                if self.__pf == 'Darwin':
                    # For Mac
                    # Trim processing with AppleScript(trim-quicktime.applescript)
                    # Create configuration information for Trim processing
                    scpt = ' ./trim-quicktime.applescript'
                    export_file = f' {cwd}/media/{self.__file_name}_trim-quicktime_trim{num}{self.__extension}'
                    start_time = f' {start}'
                    end_time = f' {end}'
                    print(f'VideoEdit.save_cut_video - Input File:{input_file}')
                    print(f'VideoEdit.save_cut_video - Export File:{export_file}\n')
                    # スクリプト実行
                    execute_applescript(scpt, input_file, export_file, start_time, end_time)
                else:
                    # For Windows / Linux
                    # Trim processing with MoviePy
                    export_file = f'{cwd}/media/{self.__file_name}_MoviePy_trim{num}{self.__extension}'
                    trim_video(self.__file_path, export_file, start, end, self.__fps)
                print(f'VideoEdit.save_cut_video - Data{num}: Trim Process End\n')

if __name__ == '__main__':
    with open('./media_info.toml') as f:
        obj = toml.load(f)
    file_path = obj['media']['path']
    time_list = obj['trim_info']['time_list']
    video_edit = VideoEdit(file_path)
    # If time information is empty, parse and process to create time information
    if len(time_list) == 0:
        time_list = video_edit.parse_video()
    video_edit.save_cut_video(time_list)
