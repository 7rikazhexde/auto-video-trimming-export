# auto-video-trimming-export

## Overview
This project aims to automate the trimming and exporting of video files.

## Notes
Due to the incomplete video analysis process, this program is not generic.  
In the future, I’d like to support analysis processing based on certain rules.  
At this time, please use the method of specifying time information in ```setting.toml``` to execute the program.

## Approaches to Automation and Processing Flow
MoviePy and QuickTime are used for trimming and exporting.

The key to automation is "creating the time information to be specified for trimming," which requires analysis of the video file (frame information).

OpenCV is used to extract frame information, and analysis processing is performed in units of seconds according to the specifications in the TOML file.

The analysis process obtains timestamps corresponding to frames that match the conditions and saves them as trimming data in a list.

## Usecase
Trimming can be performed on video files according to the following specifications.
* Detect scenes
  * Average of brightness data
* Character recognition(*1)
  * OCR(pytesseract)
* Image similarity (*1)
  * Correlation coefficient of histogram

(*1) Can be used together

## Usage
1. Get project
```
% git clone https://github.com/7rikazhexde/auto-video-trimming-export.git 
```

2. Trimming Process Settings

This project uses the information defined in ```setting.toml``` to read, log, analyze, create timestamps, and process the export of video files.

* [log]
  Define settings for outputting execution results to the log and console.
  
* [media]
  Defines the video file path to be analyzed and processed.
  This program targets MOV and MP4 operation. Others are not guaranteed.

* [[parse_info]]
  parse_info[0] defines whether the analysis process can be performed or not.

  parse_info[1] and thereafter define variables to be used in the analysis process.

  For example, if you want to analyze three different times, define elements 1 through 3.

* [trim_info]
  * Trimming processing time   
  Set the time information in the ```time_list``` key (list) in ```[trim_info]``` of ```setting.toml```.

  * Trimming processing time setting based on video analysis (deprecated)  
  Set an empty time information in the ```time_list``` key (list) in ```[trim_info]``` of ```setting.toml```.

### Trimming and exporting process  
  For Mac, use QuickTime Player from AppleScript.  

  For Windows and linux, use MoviePy.  

  Each process is automatically detected and processed based on platform information.  

  MoviePy can be used for Mac, but QuickTime Player is used because QuickTime Player is faster for export processing.  

  If you want to use MoviePy on a Mac, change ```self.__pf``` to something other than ```'Darwin'```.

### Notes
* Output file resolution is 640X360.
* Codec specification is as follows

  | Program     | codec       | codec audio | 
  | ----------- | ----------- | ----------- |
  | AppleScript | H264        | AAC         | 
  | MoviePy     | libx264     | AAC         | 

* Except for the resolution setting (480p), the default settings will be used.
* [MoviePy more details](https://zulko.github.io/moviepy/ref/VideoClip/VideoClip.html#moviepy.video.VideoClip.VideoClip.write_videofile
)

3. Setup of virtual environment
Run the poetry command.
```
% poetry install
```
* If the package DL fails after installation, there may be a problem with the development environment.
* See Switching between environments.
* Please run ```poetry env info``` to check your development environment.
* If your python version is not 3.10 or higher, please run ```poetry env use python3.10``` to recreate your development environment.

Or create a virtual environment with venv, pyenv, etc. and run the following command.
```
% pip install -r requirements.txt
```

3. Execute the program in a virtual environment
```
% cd app
% poetry shell
% python main.py
```

4. When executing a single trimming process

* To use AppleScript (Mac only)
```
% cd app
% python exe_applescript.py
```
* To use MoviePy
```
% cd app
% python moviepy_trim.py
```
