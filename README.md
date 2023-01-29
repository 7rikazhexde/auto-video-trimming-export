# auto-video-trimming-export

## Overview
This project aims to automate the trimming and exporting of video files.

## Notes
Due to the incomplete video analysis process, this program is not generic.  
In the future, we would like to support analysis processing based on certain rules.  
At this time, please use the method of specifying time information in ```media_info.toml``` to execute the program.

## Approaches to Automation
MoviePy and QuickTime are used for trimming and exporting.

The key element in the automation process is the "creation of time information to be specified in the trimming process," which requires analysis of the video file (frame information). 

OpenCV is used to extract and analyze frame information.

Analysis processing is performed on the extracted frame information for each second, but since analysis processing must be tailored to the video, we are working on this as an issue.

## Usage
1. Get project
```
% git clone https://github.com/7rikazhexde/auto-video-trimming-export.git
```

2. Various settings
Creating a video file for trimming

* File name setting  
AppleScript will not execute the process if the file name contains spaces or special characters.  
The file name should be in a format that excludes spaces and special characters.

* File path setting  
Set path = "path of the video file" in ```[media]``` of ```media_info.toml```.

* Trimming processing time setting  
Set the time information in the time_list key (list) in ```[trim_info]``` of ```media_info.toml```.

* Trimming processing time setting based on video analysis (deprecated)  
Set an empty time information in the time_list key (list) in ```[trim_info]``` of ```media_info.toml```.

* trimming and exporting process  
  For Mac, use QuickTime Player from AppleScript.For Windows and linux, use MoviePy.
  Each process is automatically detected and processed based on platform information.
  MoviePy can be used for Mac, but QuickTime Player is used because QuickTime Player is faster for export processing.
  If you want to use MoviePy on a Mac, change ```self.__pf``` to something other than ```'Darwin'```.

### Notes
* Output file resolution is 640X360.
* Codec specification is as follows

| Program | codec         | codec audio    | 
| ----- | ----------- | --------------- |
| AppleScript   | H264     | AAC | 
| MoviePy   | libx264     | AAC | 

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
* Please run poetry env info to check your development environment.
* If your python version is not 3.10 or higher, please run poetry env use python3.10 to recreate your development environment.

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
