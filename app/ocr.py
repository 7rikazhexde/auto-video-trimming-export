import pytesseract, toml, sys
from PIL import Image
from log import LogProccess

class OcrProcess:
    def __init__(self,logger,toml_obj):
        """
        OcrProcess class constructor

        Parameters
        ----------
        logger : LogProccess
            Instance variable of LogProccess class
            Used for log output
        toml_obj : dict
            Parsing result of the file specified as toml (dictionary)
        """
        self.__parse_info = toml_obj['parse_info']
        self.__logger = logger

    def ocr_frame(self,input,lang):
        """
        OCR for video file.

        This method performs OCR on video frame.

        Parameters
        ----------
        input
            Frame information read by cv2 module
        lang
            Language information for converting text images to text strings
        Note
        -------
        OCR depends on the pytesseract module (wrapper for Tesseract-OCR).
        OCR requires data files in the supported languages, but users are requested to install them themselves.
        
        See Also
        -------
        pytesseract.image_to_string
        """
        parse_info_ocr_detect_info_list = []
        for i in range(1,len(self.__parse_info)):
            if not lang in pytesseract.get_languages(config=''):
                warning_message = f'Error: Exit the program.\nError Info: The value of "ocr_detect_info" is {lang}. Please check "media_info.toml".'
                self.__logger.error(warning_message)
                sys.exit(warning_message)
            else:
                parse_info_ocr_detect_info_list.append(self.__parse_info[i]['ocr_detect_info'])

        try:
            str = pytesseract.image_to_string(input,lang)
        except ValueError as e:
            warning_message = f'{e.__class__.__name__}:{e}'
            self.__logger.error(warning_message)
            sys.exit(warning_message)
        str_rp = str.replace('\n', '')

        recognition_result = 'none'
        for i in range(len(parse_info_ocr_detect_info_list)):
            if all((i in str_rp) for i in parse_info_ocr_detect_info_list[i]):
                recognition_result = f'seane{i+1}'
                self.__logger.info(f'ocr_detect:{str_rp} - seane{i+1}')
        return recognition_result

if __name__ == '__main__':
    with open('./setting.toml') as f:
        toml_obj = toml.load(f)

    path = "./media/comparison_source_images/seane2.png"
    img = Image.open(path)
    lang = 'jpn'

    log_process = LogProccess()
    log_process.logging_info = toml_obj
    logger = log_process.logging_info

    ocr_p = OcrProcess(logger,toml_obj)
    ocr_p.ocr_frame(img,lang)