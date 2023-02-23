import cv2
import numpy as np
import scipy.stats as sstats
import toml
from log import LogProcess

class AnalyzeProcess:
    def __init__(self,logger):
        """
        AnalyzeProcess class constructor

        Parameters
        ----------
        logger : LogProcess
            Instance variable of LogProcess class
            Used for log output
        """
        self.__logger = logger

    def analyze_frame(self,im_cv):
        """
        Analyze and process for frames

        Parameters
        ----------
        im_cv : cv2.VideoCapture.read()
            Frames read per second
        
        Return:
        -------
        mean : numpy.mean()
            Average value of Numpy array
        """
        # Grayscaling
        img = cv2.cvtColor(im_cv, cv2.COLOR_RGB2GRAY)
        # one-dimensional array
        img = np.array(img).flatten()
        # Calculate the average of the luminance values
        mean = img.mean()
        #std = np.std(img)
        #median = np.median(img)
        #mode = sstats.mode(img,keepdims=True)[0][0]
        return mean#,std,median,mode
    
    def alalyzed_hist_data(self,frame,threshold_val,image_hist):
        """
        Analyze histograms

        Parameters
        ----------
        frame : cv2.VideoCapture.read()
            Frames read per second
        threshold_val : int
            setting.toml / binarizing_thresh
        image_hist : 
            setting.toml / comparison_source_image_path
            Histogram created after applying binarization and crop processing to the image used for comparison processing
        
        Return:
        -------
        analyzed_scene_hist_data : cv2.compareHist()
            Correlation coefficient between image_hist and frame_hist calculated by the HISTCMP_CORREL method
        """
        _, img_thresh = cv2.threshold(frame, threshold_val, 255, cv2.THRESH_BINARY)
        frame_hist = cv2.calcHist([img_thresh], [0], None, [256], [0, 256])
        analyzed_scene_hist_data = cv2.compareHist(image_hist, frame_hist, cv2.HISTCMP_CORREL)
        return analyzed_scene_hist_data
    
    def change_flag(self,flag_list,current_num):
        """
        Update the flag variable that manages the image being processed

        Create a flag variable that controls which target image is being processed in a list held for each target image, 
        and switch the flag on (TRUE) or off (FALSE) when a different image meets the condition, 
        so that timestamps for the same image are not stored.

        Parameters
        ----------
        flag_list : bool
            List of flag variables for each target image to manage which target image is being processed or not
        current_num : int
            Current Frame Num

        Return:
        -------
        flag_list : bool
            List after updating the flag variables corresponding to each target image
        """
        for i in range(len(flag_list)):
            if(i == current_num):
                flag_list = [False] * len(flag_list)
                flag_list[i] = True
        return flag_list

    def cropping_img(self,img,crcp_dict_list):
        """
        Update the flag variable that manages the image being processed

        Parameters
        ----------
        img : cv2.VideoCapture.read()
            Frames read per second
        crcp_dict_list : dictionary 
            setting.toml / cropping_cordinate_point

        Return:
        -------
        crcp_img : cv2.imread
            Image after crop processing
        """
        crcp_x1 = crcp_dict_list['crcp_x1']
        crcp_x2 = crcp_dict_list['crcp_x2']
        crcp_y1 = crcp_dict_list['crcp_y1']
        crcp_y2 = crcp_dict_list['crcp_y2']
        if crcp_x1 != 0 and crcp_x2 != 0 and crcp_y1 != 0 and crcp_y2 != 0:
            try:
                crcp_img = img[crcp_x1 : crcp_x2, crcp_y1 : crcp_y2]
            except:
                error_value = f"{crcp_dict_list}"
                warning_message = f'Error: Exit the program.\nError Info: The value of "cropping_cordinate_point" is {error_value}. Please check "media_info.toml".'
                self.__logger.error(warning_message)
        else:
            crcp_img = img
        return crcp_img

if __name__ == '__main__':
    with open('./setting.toml') as f:
        toml_obj = toml.load(f)
    path = './media/save_frames/lena.png'
    im_cv = cv2.imread(path)

    log_process = LogProcess()
    log_process.logging_info = toml_obj
    logger = log_process.logging_info

    ap = AnalyzeProcess(logger)
    mean = ap.analyze_frame(im_cv)
    logger.info(f'image_path: {path}')
    logger.info(f'mean: {mean}')