import subprocess, os, sys, toml
from log import LogProcess

class ExeAppleScript:
    def __init__(self,logger):
        """
        ExeAppleScript class constructor

        Parameters
        ----------
        logger : LogProcess
            Instance variable of LogProcess class
            Used for log output
        """
        self.__logger = logger

    def execute_applescript(self, scpt, input_file, export_file, start_time, end_time):
        """
        Video trimming process for QicktimePlayer

        Parameters
        ----------
        scpt
            applescript file path
        input_file
            Path of video file to be trimmed (.mov or .mp4)
        export_file
            Path to output video after trimming process
        start_time
            Trimming start position
        end_time
            Trimming end position
        
        Raises:
        -------
            check_output method, and errors in AppleScript execution are handled as built-in exceptions in Exception
        Note
        -------
        The trimming process uses osascript and AWK commands.
        Variables(command line arguments) must be defined in a format that includes spaces.
        """
        self.__logger.info(f'Start AppleScript Execution')
        cmd = 'osascript' + scpt + input_file + export_file + start_time + end_time
        try:
            subprocess.check_output(cmd.split()).decode('utf-8')
        except Exception as e:
            self.__logger.error(e)
            sys.exit()
        self.__logger.info(f'Execution AppleScript Complete')

if __name__ == '__main__':
    scpt = ' ./trim-quicktime.applescript'
    cwd = os.getcwd()
    # Variables (command line arguments) are defined in a format that includes spaces.
    input_file = f' {cwd}/media/test.mp4'
    export_file = f' {cwd}/media/test_mac_trim.mp4'
    start_time = 50
    start_time = f' {start_time}'
    end_time = 100
    end_time = f' {end_time}'

    with open('./setting.toml') as f:
        toml_obj = toml.load(f)

    log_process = LogProcess()
    log_process.logging_info = toml_obj
    logger = log_process.logging_info

    execute_applescript = ExeAppleScript(logger)
    execute_applescript.execute_applescript(scpt, input_file, export_file, start_time, end_time)