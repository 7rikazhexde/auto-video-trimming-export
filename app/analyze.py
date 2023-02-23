import cv2
import numpy as np
import scipy.stats as sstats
import toml
from log import LogProccess

class AnalyzeProcess:
    def __init__(self,logger):
        self.__logger = logger

    def analyze_frame(self,im_cv):
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
        _, img_thresh = cv2.threshold(frame, threshold_val, 255, cv2.THRESH_BINARY)
        frame_hist = cv2.calcHist([img_thresh], [0], None, [256], [0, 256])
        analyzed_scene_hist_data = cv2.compareHist(image_hist, frame_hist, cv2.HISTCMP_CORREL)
        return analyzed_scene_hist_data
    
    def change_flag(self,flag_list,current_num):
        for i in range(len(flag_list)):
            if(i == current_num):
                flag_list = [False] * len(flag_list)
                flag_list[i] = True
        return flag_list

    def cropping_img(self,img,crcp_dict_list):
        crcp_x1 = crcp_dict_list['crcp_x1']
        crcp_x2 = crcp_dict_list['crcp_x2']
        crcp_y1 = crcp_dict_list['crcp_y1']
        crcp_y2 = crcp_dict_list['crcp_y2']
        if crcp_x1 != 0 and crcp_x2 != 0 and crcp_y1 != 0 and crcp_y2 != 0:
            try:
                crcp_img = img[crcp_x1 : crcp_x2, crcp_y1 : crcp_y2]
            except:
                #on_error(crcp_dict_list,'cropping_cordinate_point')
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

    log_process = LogProccess()
    log_process.logging_info = toml_obj
    logger = log_process.logging_info

    ap = AnalyzeProcess(logger)
    mean = ap.analyze_frame(im_cv)
    logger.info(f'image_path: {path}')
    logger.info(f'mean: {mean}')