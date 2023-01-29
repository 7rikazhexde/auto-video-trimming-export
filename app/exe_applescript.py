import subprocess
import os

def execute_applescript(scpt, input_file, export_file, start_time, end_time):
    print(f'execute_applescript - Start AppleScript Execution\n')
    cmd = 'osascript' + scpt + input_file + export_file + start_time + end_time
    rtn = subprocess.check_output(cmd.split()).decode('utf-8')
    print(rtn)
    print(f'execute_applescript - Execution AppleScript Complete')

if __name__ == '__main__':
    scpt = ' ./trim-quicktime.applescript'
    cwd = os.getcwd()
    input_file = f' {cwd}/media/test.mp4'
    export_file = f' {cwd}/media/test_mac_trim.mp4'
    start_time = 50
    start_time = f' {start_time}'
    end_time = 250
    end_time = f' {end_time}'
    execute_applescript(scpt, input_file, export_file, start_time, end_time)