(********************************************************
Summary:
	AppleScript for trimming and file export processing using 
	the video file and time information specified in the argument in QuickTime Player on MacOS.
 
Verified Version:
	ProductName:    macOS
	ProductVersion: 12.6.3
	BuildVersion:   21G419

Usage:
	% osascript trim-quicktime.applescript [1.input_file] [2.output_file] [3.startTime] [4.endTime]
	1.Select video files to be trimmed
	2.Specify the path (folder) to output files after trimming
	3.Enter the trim start time
	4.Enter trim end time

Note:
	Video formats other than MOV and MP4 have not been tested.

Reference:
 	1. Batch cut unwanted parts of mp4 with AppleScript
	https://golbitz.com/applescript/applescript%E3%81%A7mp4%E3%81%AE%E4%B8%8D%E8%A6%81%E3%81%AA%E9%83%A8%E5%88%86%E3%82%92%E4%B8%80%E6%8B%AC%E3%82%AB%E3%83%83%E3%83%88-624
	2. apple script quicktime player export permission error
	https://discussions.apple.com/thread/250200823	
	3. Referencing Files and Folders 
	https://sites.google.com/site/zzaatrans/home/macautomationscriptingguide/referencefilesandfolders-html	
	4. Technical Note TN2065 
	https://sites.google.com/site/zzaatrans/home/doshellscriptinas_apple_2006-html/tn2065_apple	
	5. [Linux] Obtain the file size.
	https://ameblo.jp/archive-redo-blog/entry-10196055325.html
	6. Find and Replace Strings
	http://tonbi.jp/AppleScript/Tips/String/FindReplace.html
	7. coreutils
	https://formulae.brew.sh/formula/coreutils
********************************************************)

(********************************************************
Script attributes regarding log information

Note:
	Set to true to write to a log file.
********************************************************)
property DEBUG : true
property LOG_FILE : "./execution.log"
property INFO :  "- INFO - log - "

(******************************************************** 
trimVideo():
	Function to convert date to yyyy-mm-dd hh:mm:ss,3N
	
Argument:
	txt: Output strings to log file and terminal
	
Return:
	none
	
Note:
	Use the gdate command because the mac cannot obtain millisecond time information with the date command.
	If you get an error with the gdate command, run the following to install coreutils.
	```
	% brew install coreutils 
	```
Reference:
	7. coreutils
********************************************************)
on echo(txt)
	if DEBUG then
		set nowTime to do shell script "gdate " & "'+%Y-%m-%d %H:%M:%S,%3N'"
		do shell script "echo " & nowTime & " " & txt & " >> " & LOG_FILE
		log nowTime & " " & txt
	end if
end echo

(******************************************************** 
trimVideo():
	Function to enter trim time
	
Argument:
	* input_file: Input file path (POSIX)
	* output_file: Output file path (POSIX)
	* startTime: Trim start time
	* endTime: Trim end time
	
Return:
	none
	
Note:
	If a file name contains a blank string, it is processed by replacing the blank string with "_".
	
Reference:
	1. Batch cut unwanted parts of mp4 with AppleScript
	2. apple script quicktime player export permission error
	3. Referencing Files and Folders 
	4. Technical Note TN2065 
	5. [Linux] Obtain the file size.
********************************************************)
on trimVideo(input_file, output_file, startTime, endTime)
	set inputPathForPOSIX to input_file
	--echo(INFO & "trim-quicktime.applescript - trimVideo - inputPathForPOSIX: " & inputPathForPOSIX)
	set outFileForPOSIX to output_file
	--echo(INFO & "trim-quicktime.applescript - trimVideo - outFileForPOSIX: " & outFileForPOSIX)
	set inputFilePathForHFS to POSIX file inputPathForPOSIX
	--echo(INFO & "trim-quicktime.applescript - trimVideo - inputFilePathForHFS: " & inputFilePathForHFS)
	set outputFilePathForHFS to POSIX file outFileForPOSIX
	--echo(INFO & "trim-quicktime.applescript - trimVideo - outputFilePathForHFS: " & outputFilePathForHFS)

	echo(INFO & "trim-quicktime.applescript - trimVideo - Trim Start Time: " & startTime & "[sec]")
	echo(INFO & "trim-quicktime.applescript - trimVideo - Trim End Time: " & endTime & "[sec]")
	tell application "QuickTime Player"
		activate
		
		-- Open video file
		try
			set theOpenedFile to open for access file outputFilePathForHFS with write permission
			set eof of theOpenedFile to 0
		end try
		
		open file inputFilePathForHFS
		
		-- Set trimming and export video file
		trim front document from startTime to endTime
		export front document in outputFilePathForHFS using settings preset "480p"
		
		-- File close
		delay 1
		try
			close access theOpenedFile
		end try
		-- Even in the case of dirty, it does not save.
		close every document saving no
		
		-- File export
		-- The file export progress bar does not automatically close after exporting, use the quit command to close it after exporting.
		-- File export completion is determined by file size.
		-- Set the file size in each of the two variables and compare their values.
		-- If the file sizes are the same, determine that file export is complete.

		echo(INFO & "trim-quicktime.applescript - trimVideo - Start Trim") of me
		repeat
			tell current application
				-- Get the file size after an interval of 0.5 second
				set fileSize1 to do shell script "ls -lt " & outFileForPOSIX & " | awk '{print $5}'"
				delay 0.5
				set fileSize2 to do shell script "ls -lt " & outFileForPOSIX & " | awk '{print $5}'"
			end tell
			-- If the file size is the same, the iterative process is exsited.
			if fileSize1 = fileSize2 then
				exit repeat
			end if
		end repeat

		echo(INFO & "trim-quicktime.applescript - trimVideo - End Trim and File Export Complete") of me
		echo(INFO & "trim-quicktime.applescript - trimVideo - Export File Path: " & outFileForPOSIX) of me
		--log "fileSize1: " & fileSize1 & " / " & "fileSize2: " & fileSize1
		quit
	end tell
end trimVideo

(********************************************************
run argv:
	Run handler specifying command line arguments.
	Executed when the Applet is launched.
	
Argument:
	none
	
Return:
	none
	
Note:
	When executing the script, the following information must be specified as space-delimited command line arguments
	* Input file path (POSIX)
	* Output file path (POSIX)
	* Trim start time
	* Trim end time
	If the arguments are not specified correctly, the trim process will not start.
********************************************************)
on run argv
	if (count of argv) = 4 then
		set input_file to item 1 of argv
		set output_file to item 2 of argv
		set startTime to item 3 of argv as number
		set endTime to item 4 of argv as number
		trimVideo(input_file, output_file, startTime, endTime)
	else
		display alert "Trim process could not be started. " & return & "Please check the specified arguments."
	end if
end run