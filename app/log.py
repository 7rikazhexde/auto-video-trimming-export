import logging, toml

class LogProcess:
    def __init__(self):
        pass
    def set_logging_info(self,toml_obj):
        """
        Setter for Log Information Settings

        Logs are output to the console and log file according to the ``logging_level_stream`` and ``logging_level_file`` specifications in ``setting.toml``.

        Parameters
        ----------
        toml_obj : dict
            Parsing result of the file specified as toml (dictionary)
        """
        log_info = toml_obj['log']['log_file_path']
        logging_level_stream = toml_obj['log']['logging_level_stream']
        logging_level_file = toml_obj['log']['logging_level_file']
        self.__logger = logging.getLogger(__name__)

        match logging_level_stream:
            case 'notset':
                self.__logger.setLevel(logging.NOTSET)
            case 'debug':
                self.__logger.setLevel(logging.DEBUG)
            case 'info':
                self.__logger.setLevel(logging.INFO)
            case 'warnnig':
                self.__logger.setLevel(logging.WARNING)
            case 'error':
                self.__logger.setLevel(logging.ERROR)
            case 'critical':
                self.__logger.setLevel(logging.CRITICAL)
            case _:
                self.__logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s')
        
        file_handler = logging.FileHandler(log_info)

        match logging_level_file:
            case 'notset':
                file_handler.setLevel(logging.NOTSET)
            case 'debug':
                file_handler.setLevel(logging.DEBUG)
            case 'info':
                file_handler.setLevel(logging.INFO)
            case 'warnnig':
                file_handler.setLevel(logging.WARNING)
            case 'error':
                file_handler.setLevel(logging.ERROR)
            case 'critical':
                file_handler.setLevel(logging.CRITICAL)
            case _:
                file_handler.setLevel(logging.DEBUG)
                
        file_handler.setFormatter(formatter)
        
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        self.__logger.addHandler(file_handler)
        self.__logger.addHandler(stream_handler)
    
    def get_logging_info(self):
        """
        Getter for Log Information Settings

        Return
        ----------
        self.__logger : logging.getLogger(__name__)
            Return Module Log Information
        """
        return self.__logger
    
    ''''property() function to property the get_logging_info and set_logging_info methods.'''
    logging_info = property(get_logging_info,set_logging_info)

if __name__ == '__main__':
    with open('./setting.toml') as f:
        toml_obj = toml.load(f)
    log_process = LogProcess()
    log_process.logging_info = toml_obj
    lp = log_process.logging_info
    lp.info('')