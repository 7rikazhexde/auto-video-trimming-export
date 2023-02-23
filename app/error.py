import sys, toml
from log import LogProccess

class ErrorProcess:
    def __init__(self,logger):
        """
        ErrorProcess class constructor

        Parameters
        ----------
        logger : LogProccess
            Instance variable of LogProccess class
            Used for log output
        """
        self.__logger = logger

    def on_error(self,value,subject):
        """
        Error log output processing

        Parameters
        ----------
        value
            error value
        subject : str
            Error source variable
        """
        error_value = f'{value}'
        warning_message = f'Error: Exit the program.\nError Info: The value of "{subject}" is {error_value}. Please check "media_info.toml".'
        self.__logger.error(warning_message)
        sys.exit(warning_message)

if __name__ == '__main__':
    with open('./setting.toml') as f:
        toml_obj = toml.load(f)
    log_process = LogProccess()
    log_process.logging_info = toml_obj
    logger = log_process.logging_info
    error = ErrorProcess(logger)

