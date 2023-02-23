import cv2, platform, toml
from os.path import dirname, basename, splitext
import numpy as np
from analyze import AnalyzeProcess
from error import ErrorProcess
from moviepy.editor import *
from moviepy_trim import ExeMovieyPy
from exe_applescript import ExeAppleScript
from ocr import OcrProcess
from log import LogProccess

class VideoEdit:
    """
    VideoEdit is a class that handles video files.
    See Also
    --------
    reference: setting.toml
    """
    def __init__(self,logger,toml_obj):
        """
        VideoEdit class constructor

        Create instances of the LogProcess, AnalyzeProsess, and ErrorProcess classes as initialization processes, 
        obtain values from setting.toml, and set them to instance variables.

        If an abnormal value is read, the value is output to a log file and the program exit.

        Parameters
        ----------
        logger : LogProccess
            Instance variable of LogProccess class
            Used for log output
        toml_obj : dict
            Parsing result of the file specified as toml (dictionary)

        Returns
        -------
        none
        """

        self.__logger = logger
        self.__analyze_process = AnalyzeProcess(self.__logger)
        self.__error_process = ErrorProcess(self.__logger)

        # TOML file read and set instance variables
        self.__file_path = toml_obj['media']['input_file_path']
        self.__dname = dirname(self.__file_path )
        self.__fname = basename(self.__file_path )
        self.__file_name = splitext(self.__fname)[0]
        self.__extension = splitext(self.__fname)[1]
        self.__logger.info(f'media_dir: {self.__dname}, input_file_name: {self.__fname}')
        self.__capture = cv2.VideoCapture(self.__file_path )

        if not self.__capture.isOpened():
            sys.exit()
        
        self.__total_frame_count = int(self.__capture.get(cv2.CAP_PROP_FRAME_COUNT))

        self.__fps = self.__capture.get(cv2.CAP_PROP_FPS)
        self.__timestamp_list = []

        self.__parse_info = toml_obj['parse_info']

        if type(self.__parse_info[0]['ocr_enable']) == bool:
            self.__ocr_enable = self.__parse_info[0]['ocr_enable']
        else:
            error_value = f"{self.__parse_info[0]['ocr_enable']}({type(self.__parse_info[0]['ocr_enable'])})"
            self.__error_process.on_error(error_value,'ocr_enable')
             
        if type(self.__parse_info[0]['histogram_analysis_enable']) == bool:
            self.__histogram_analysis_enable  = self.__parse_info[0]['histogram_analysis_enable']
        else:
            error_value = f"{self.__parse_info[0]['histogram_analysis_enable']}({type(self.__parse_info[0]['histogram_analysis_enable'])})"
            self.__error_process.on_error(error_value,'histogram_analysis_enable')

        if type(self.__parse_info[0]['save_frames_enable']) == bool:
            self.__save_frames_enable  = self.__parse_info[0]['save_frames_enable']
        else:
            error_value = f"{self.__parse_info[0]['save_frames_enable']}({type(self.__parse_info[0]['save_frames_enable'])})"
            self.__error_process.on_error(error_value,'save_frames_enable')

        if type(self.__parse_info[0]['seane_detect_enable']) == bool:
            self.__seane_detect_enable = self.__parse_info[0]['seane_detect_enable']
            self.__seane_detect_id = 0
        else:
            error_value = f"{self.__parse_info[0]['seane_detect_enable']}({type(self.__parse_info[0]['seane_detect_enable'])})"
            self.__error_process.on_error(error_value,'seane_detect_enable')

        if self.__seane_detect_enable:
            self.__seane_detect_mean_val = self.__parse_info[0]['seane_detect_mean_val']
            if not (self.__seane_detect_mean_val >= 0 and self.__seane_detect_mean_val < 256):
                error_value = f"{self.__seane_detect_mean_val}"
                self.__error_process.on_error(error_value,'seane_detect_mean_val')

        self.__parse_info_image_path_list = []
        self.__parse_info_recognized_language_list = []
        self.__parse_info_hg_comp_correl_thresh_list = []
        self.__parse_info_skip_frame_list = []
        self.__parse_info_cropping_cordinate_point_list = []
        self.__parse_info_binarizing_thresh_list = []
        self.__parse_info_list_num = len(self.__parse_info) - 1

        for i in range(1,len(self.__parse_info)):
            self.__parse_info_image_path_list.append(self.__parse_info[i]['comparison_source_image_path'])

            self.__parse_info_recognized_language_list.append(self.__parse_info[i]['recognized_language'])
            
            if self.__parse_info[i]['hg_comp_correl_thresh'] >= 0:
                self.__parse_info_hg_comp_correl_thresh_list.append(self.__parse_info[i]['hg_comp_correl_thresh'])
            else:
                error_value = f"{self.__parse_info[i]['hg_comp_correl_thresh']}"
                self.__error_process.on_error(error_value,'hg_comp_correl_thresh')

            if self.__parse_info[i]['skip_frame'] >= 0 and self.__parse_info[i]['skip_frame'] < self.__total_frame_count:
                self.__parse_info_skip_frame_list.append(self.__parse_info[i]['skip_frame'])
            else:
                error_value = f"{self.__parse_info[i]['skip_frame']}"
                self.__error_process.on_error(error_value,'skip_frame')

            if len(self.__parse_info[i]['cropping_cordinate_point']) == 2:
                self.__parse_info_cropping_cordinate_point_list.append(self.__parse_info[i]['cropping_cordinate_point'])
            else:
                error_value = f"{self.__parse_info[i]['cropping_cordinate_point']}"
                self.__error_process.on_error(error_value,'cropping_cordinate_point')

            if self.__parse_info[i]['binarizing_thresh'] >= 0 and self.__parse_info[i]['binarizing_thresh'] < 255:
                self.__parse_info_binarizing_thresh_list.append(self.__parse_info[i]['binarizing_thresh'])
            else:
                error_value = f"{self.__parse_info[i]['binarizing_thresh']}"
                self.__error_process.on_error(error_value,'binarizing_thresh')

        self.__parse_info_crcp_dict_list = []
        for i in range(len(self.__parse_info_cropping_cordinate_point_list)):
            crcp_x1 = self.__parse_info_cropping_cordinate_point_list[i][0][0]
            crcp_y1 = self.__parse_info_cropping_cordinate_point_list[i][0][1]
            crcp_x2 = self.__parse_info_cropping_cordinate_point_list[i][1][0]
            crcp_y2 = self.__parse_info_cropping_cordinate_point_list[i][1][1]
            crcp_dict = {'crcp_x1': crcp_x1, 'crcp_y1':crcp_y1, 'crcp_x2':crcp_x2, 'crcp_y2':crcp_y2}
            self.__parse_info_crcp_dict_list.append(crcp_dict)

        self.__logger.info(f'fps: {self.__fps}')
        self.__pf = platform.system()
    
    def parse_video(self):
        """
        parse video frame by frame.

        This function parses the video according to the value of parse_info[0] in the TOML file.
        The parsing process uses the results analyzed according to the specification of 
        scene detection (mean), image comparison, and OCR processing.
        
        Image comparison, and OCR processing can be used together.

        Parameters
        ----------
        self
            set instance variables

        Returns
        -------
        list
            Returns the timestamp and id that match the conditions of the parsing process.
            analyzed_id_list,analyzed_ts_list
        """
        
        # Counter for frame
        count = 0
        # Create an empty list of time information and id to be saved after analysis
        analyzed_id_list = []
        analyzed_ts_list = []

        """
        Performs cropping and binarization (binary threshold: cv2.THRESH_BINARY) 
        on the pre-stored source images for comparison, 
        calculates the histogram, and stores the calculation results in a list
        """
        if self.__histogram_analysis_enable:
            self.__image_hist_list = []
            for i in range(self.__parse_info_list_num):
                image = cv2.imread(self.__parse_info_image_path_list[i])
                image = self.__analyze_process.cropping_img(image,self.__parse_info_crcp_dict_list[i])
                _, image = cv2.threshold(image, self.__parse_info_binarizing_thresh_list[i], 255, cv2.THRESH_BINARY)
                image_hist = cv2.calcHist([image], [0], None, [256], [0, 256])
                self.__image_hist_list.append(image_hist)

        # Flags that manage information on frames that correspond to the analysis result conditions.
        detect_seane_flag_list = [False] * self.__parse_info_list_num

        self.__total_frame_count = int(self.__capture.get(cv2.CAP_PROP_FRAME_COUNT))
        self.__logger.info(f'Total number of frames: {self.__total_frame_count}')

        self.__play_time = int(self.__total_frame_count / self.__fps)
        self.__logger.info(f'Total play time: {self.__play_time}')

        if not self.__capture.isOpened():
            sys.exit()

        while True:
            # Get Frame
            ret, frame = self.__capture.read()
            # If not readable, exit the loop.
            if not ret:
                break     
            if int(count % self.__fps) == 0:
                if self.__save_frames_enable:
                    cv2.imwrite(f"./media/save_frames/{self.__file_name}_{count:02}.png", frame)
                if (self.__histogram_analysis_enable and self.__ocr_enable):
                    ocr_process = OcrProcess(self.__logger,toml_obj)
                    for i in range(self.__parse_info_list_num):
                        frame = self.__analyze_process.cropping_img(frame,self.__parse_info_crcp_dict_list[i])
                        analyzed_scene_hist_data = self.__analyze_process.alalyzed_hist_data(
                            frame,
                            self.__parse_info_binarizing_thresh_list[i],
                            self.__image_hist_list[i]
                        )
                        if(analyzed_scene_hist_data >= self.__parse_info_hg_comp_correl_thresh_list[i]):
                            if detect_seane_flag_list[i] == False:
                                current_frame_count = self.__capture.get(cv2.CAP_PROP_POS_FRAMES)
                                if(ocr_process.ocr_frame(frame, self.__parse_info_recognized_language_list[i]) == f'seane{i+1}'):
                                    if(current_frame_count + self.__parse_info_skip_frame_list[i] < self.__total_frame_count):
                                        if len(analyzed_id_list) > 1:
                                            if analyzed_id_list[len(analyzed_id_list)-2] != analyzed_id_list[len(analyzed_id_list)-1]:
                                                if analyzed_id_list[len(analyzed_id_list)-1] != i+1:
                                                    analyzed_id_list.append(i+1)
                                                    timestamp = self.__capture.get(cv2.CAP_PROP_POS_MSEC)/1000
                                                    analyzed_ts_list.append(timestamp)
                                                self.__capture.set(cv2.CAP_PROP_POS_FRAMES, current_frame_count + self.__parse_info_skip_frame_list[i])
                                                detect_seane_flag_list = self.__analyze_process.change_flag(detect_seane_flag_list,i)
                                            else:
                                                self.__capture.set(cv2.CAP_PROP_POS_FRAMES, current_frame_count + self.__parse_info_skip_frame_list[i])
                                                detect_seane_flag_list = [False] * self.__parse_info_list_num
                                        else:
                                            analyzed_id_list.append(i+1)
                                            timestamp = self.__capture.get(cv2.CAP_PROP_POS_MSEC)/1000
                                            analyzed_ts_list.append(timestamp)
                                            detect_seane_flag_list = self.__analyze_process.change_flag(detect_seane_flag_list,i)
                                            self.__capture.set(cv2.CAP_PROP_POS_FRAMES, current_frame_count + self.__parse_info_skip_frame_list[i])
                                    else:
                                        if len(analyzed_id_list) > 1:
                                            if analyzed_id_list[len(analyzed_id_list)-2] != analyzed_id_list[len(analyzed_id_list)-1]:
                                                if analyzed_id_list[len(analyzed_id_list)-1] != i+1:
                                                    analyzed_id_list.append(i+1)
                                                    timestamp = self.__capture.get(cv2.CAP_PROP_POS_MSEC)/1000
                                                    analyzed_ts_list.append(timestamp)
                                                self.__capture.set(cv2.CAP_PROP_POS_FRAMES, current_frame_count + self.__parse_info_skip_frame_list[i])
                                                detect_seane_flag_list = self.__analyze_process.change_flag(detect_seane_flag_list,i)
                                            else:
                                                detect_seane_flag_list = [False] * self.__parse_info_list_num
                                        else:
                                            analyzed_id_list.append(i+1)
                                            timestamp = self.__capture.get(cv2.CAP_PROP_POS_MSEC)/1000
                                            analyzed_ts_list.append(timestamp)
                                            detect_seane_flag_list = self.__analyze_process.change_flag(detect_seane_flag_list,i)

                elif self.__ocr_enable:
                    ocr_process = OcrProcess(self.__logger,toml_obj)
                    for i in range(self.__parse_info_list_num):
                        frame = self.__analyze_process.cropping_img(frame,self.__parse_info_crcp_dict_list[i])
                        current_frame_count = self.__capture.get(cv2.CAP_PROP_POS_FRAMES)
                        if(ocr_process.ocr_frame(frame, self.__parse_info_recognized_language_list[i]) == f'seane{i+1}'):
                            if(current_frame_count + self.__parse_info_skip_frame_list[i] < self.__total_frame_count):
                                if len(analyzed_id_list) > 1:
                                    if analyzed_id_list[len(analyzed_id_list)-2] != analyzed_id_list[len(analyzed_id_list)-1]:
                                        timestamp = self.__capture.get(cv2.CAP_PROP_POS_MSEC)/1000
                                        if analyzed_id_list[len(analyzed_id_list)-1] != i+1:
                                            analyzed_id_list.append(i+1)
                                            analyzed_ts_list.append(timestamp)
                                        self.__capture.set(cv2.CAP_PROP_POS_FRAMES, current_frame_count + self.__parse_info_skip_frame_list[i])
                                        detect_seane_flag_list = self.__analyze_process.change_flag(detect_seane_flag_list,i)
                                    else:
                                        self.__capture.set(cv2.CAP_PROP_POS_FRAMES, current_frame_count + self.__parse_info_skip_frame_list[i])
                                        detect_seane_flag_list = [False] * self.__parse_info_list_num
                                else:
                                    analyzed_id_list.append(i+1)
                                    timestamp = self.__capture.get(cv2.CAP_PROP_POS_MSEC)/1000
                                    analyzed_ts_list.append(timestamp)
                                    detect_seane_flag_list = self.__analyze_process.change_flag(detect_seane_flag_list,i)
                                    self.__capture.set(cv2.CAP_PROP_POS_FRAMES, current_frame_count + self.__parse_info_skip_frame_list[i])
                            else:
                                if len(analyzed_id_list) > 1:
                                    if analyzed_id_list[len(analyzed_id_list)-2] != analyzed_id_list[len(analyzed_id_list)-1]:
                                        if analyzed_id_list[len(analyzed_id_list)-1] != i+1:
                                            analyzed_id_list.append(i+1)
                                            timestamp = self.__capture.get(cv2.CAP_PROP_POS_MSEC)/1000
                                            analyzed_ts_list.append(timestamp)
                                        self.__capture.set(cv2.CAP_PROP_POS_FRAMES, current_frame_count + self.__parse_info_skip_frame_list[i])
                                        detect_seane_flag_list = self.__analyze_process.change_flag(detect_seane_flag_list,i)
                                    else:
                                        detect_seane_flag_list = [False] * self.__parse_info_list_num
                                else:
                                    analyzed_id_list.append(i+1)
                                    timestamp = self.__capture.get(cv2.CAP_PROP_POS_MSEC)/1000
                                    analyzed_ts_list.append(timestamp)
                                    detect_seane_flag_list = self.__analyze_process.change_flag(detect_seane_flag_list,i)
                            
                elif self.__histogram_analysis_enable:
                    for i in range(self.__parse_info_list_num):
                        analyzed_scene_hist_data = self.__analyze_process.alalyzed_hist_data(
                            frame,
                            self.__parse_info_binarizing_thresh_list[i],
                            self.__image_hist_list[i]
                        )
                        if(analyzed_scene_hist_data >= self.__parse_info_hg_comp_correl_thresh_list[i]):
                            if detect_seane_flag_list[i] == False:
                                if len(analyzed_id_list) > 1:
                                    if analyzed_id_list[len(analyzed_id_list)-2] != analyzed_id_list[len(analyzed_id_list)-1]:
                                        if analyzed_id_list[len(analyzed_id_list)-1] != i+1:
                                            analyzed_id_list.append(i+1)
                                            timestamp = self.__capture.get(cv2.CAP_PROP_POS_MSEC)/1000
                                            analyzed_ts_list.append(timestamp)
                                        detect_seane_flag_list = self.__analyze_process.change_flag(detect_seane_flag_list,i)
                                    else:
                                        detect_seane_flag_list = [False] * self.__parse_info_list_num
                                else:
                                    analyzed_id_list.append(i+1)
                                    timestamp = self.__capture.get(cv2.CAP_PROP_POS_MSEC)/1000
                                    analyzed_ts_list.append(timestamp)
                                    detect_seane_flag_list = self.__analyze_process.change_flag(detect_seane_flag_list,i)
                elif self.__seane_detect_enable:
                    mean = self.__analyze_process.analyze_frame(frame)
                    if(mean == self.__seane_detect_mean_val):
                        self.__seane_detect_id += 1
                        self.__logger.info(f'seane_detect_{self.__seane_detect_id}')
                        timestamp = self.__capture.get(cv2.CAP_PROP_POS_MSEC)/1000
                        analyzed_ts_list.append(timestamp)
            count += 1
        self.__logger.info(f'analyzed_id_list:{analyzed_id_list}')
        self.__logger.info(f'analyzed_ts_list:{analyzed_ts_list}')
        return analyzed_id_list,analyzed_ts_list

    def create_ts_list(self,timestamps):
        """
        Create a list of timestamps.

        This function parses the video according to the value of parse_info[0] in the TOML file.
        The parsing process uses the results analyzed according to the specification of 
        scene detection (mean), image comparison, and OCR processing.
        
        Image comparison, and OCR processing can be used together.

        Parameters
        ----------
        self
            set instance variables
        list
            List of timestamps corresponding to frames

        Returns
        -------
        list
            Returns a list of timestamps stored as a set of start and end (two-dimensional)
        
        Raise
        -------
        none
            If it is not possible to create a list of timestamps with a start and end set, 
            create the list using up to the elements that can be created.
        """
        num = 1
        # Create a list of start and end times to be specified in trim processing from analysis results (frames)
        for i in range(len(timestamps)):
            if i % 2 == 0:
                try:
                    self.__timestamp_list.append([timestamps[i], timestamps[i+1],f'seg_{num}'])
                except:
                    # Exit the loop process if timestamps for the start and end sets cannot be created
                    break
                num += 1
        self.__logger.info(f'timestamp_list:{self.__timestamp_list}')
        self.__logger.info('Analyze End & Trim Seg Created')
        return self.__timestamp_list
    
    def create_ts_list_start_to_end(self,analyzed_ts_list):
        """
        Create a list of timestamps for the first and last frames combined.
        Timestamps are handled differently than in create_ts_list(), 
        where the start and end lists are shifted by one element from the first frame.
        
        Parameters
        ----------
        self
            set instance variables
        list
            List of timestamps corresponding to frames

        Returns
        -------
        list
            Returns a list of timestamps stored as a start and end set, 
            including the first and last frames (two-dimensional).
        """
        # Create a list of start and end times to be specified in trim processing from analysis results (frames)
        num = 1
        for i in range(len(analyzed_ts_list)):
            if i == 0:
                # the first time list
                # Start time is set to 0
                self.__timestamp_list.append([0, analyzed_ts_list[i], f'seg_{num+1}'])
            else:
                # After the first time list
                # Shift the start time by 1 second.
                num += 1
                self.__timestamp_list.append([analyzed_ts_list[i-1]+1, analyzed_ts_list[i], f'seg_{num}'])
            # Last start time is created from the last frame information that has already been analyzed.
            unique_last_ts = analyzed_ts_list[i]
        # Create last time list for trim process
        num += 1
        self.__timestamp_list.append([unique_last_ts, self.__play_time, f'seg_{num}'])
        self.__logger.info(f'timestamp_list:{self.__timestamp_list}')
        return self.__timestamp_list

    # Trim Process
    def save_cut_video(self,time_list):
        """
        Trimming and exporting process.

        For Mac, use QuickTime Player from AppleScript.  
        For Windows and linux, use MoviePy.  
        Each process is automatically detected and processed based on platform information.  
        If you want to use MoviePy on a Mac, change ```self.__pf``` to something other than ```'Darwin'```.     
        
        Parameters
        ----------
        self
            set instance variables
        list
            List of timestamps corresponding to frames(two-dimensional).

        Returns
        -------
        none
        """
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
                num += 1
                self.__logger.info(f'Seg{num}: Trim Process Start')
                if self.__pf == 'Darwin':
                    # For Mac
                    # Trim processing with AppleScript(trim-quicktime.applescript)
                    # Create configuration information for Trim processing
                    scpt = ' ./trim-quicktime.applescript'
                    export_file = f' {cwd}/media/{self.__file_name}_trim{num}{self.__extension}'
                    start_time = f' {start}'
                    end_time = f' {end}'
                    self.__logger.info(f'Input File:{input_file}')
                    self.__logger.info(f'Export File:{export_file}')
                    # スクリプト実行
                    execute_applescript = ExeAppleScript(self.__logger)
                    execute_applescript.execute_applescript(scpt, input_file, export_file, start_time, end_time)
                else:
                    # For Windows / Linux
                    # Trim processing with MoviePy
                    execute_moviepy = ExeMovieyPy(self.__logger)
                    export_file = f'{cwd}/media/{self.__file_name}_MoviePy_trim{num}{self.__extension}'
                    execute_moviepy.trim_video(self.__file_path, export_file, start, end, self.__fps)
                self.__logger.info(f'Seg{num}: Trim Process End')

if __name__ == '__main__':
    with open('./setting.toml') as f:
        toml_obj = toml.load(f)

    log_process = LogProccess()
    log_process.logging_info = toml_obj
    logger = log_process.logging_info

    logger.info(f'Program execution start')

    time_list = toml_obj['trim_info']['time_list']
    seane_detect_enable = toml_obj['parse_info'][0]['seane_detect_enable']

    video_edit = VideoEdit(logger,toml_obj)
    timestamps_list = []
    
    # If time information is empty, parse and process to create time information
    if len(time_list) == 0:
        analyzed_id_list,analyzed_ts_list = video_edit.parse_video()
        if seane_detect_enable:
            timestamps_list = video_edit.create_ts_list_start_to_end(analyzed_ts_list)
        else:
            timestamps_list = video_edit.create_ts_list(analyzed_ts_list)
    else:
        num = 1
        for i in range(len(time_list)):
            timestamps_list.append([time_list[i][0], time_list[i][1],f'seg_{num}'])
            num += 1
    
    f = np.vectorize(str)
    timestamps_list = f(timestamps_list)
    output_file = './media/timestamp_data.csv'
    np.savetxt(output_file, timestamps_list, delimiter=',', fmt='%s')

    video_edit.save_cut_video(timestamps_list)

    logger.info(f'Program execution end')

    
