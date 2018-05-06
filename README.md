# ASCII
## Description
Convert Pictures to ASCII Pictures and Videos to ASCII Videos

## Variables
+ picRows: Rows of ASCII chars in each frame
+ picCols: Columns of ASCII chars in each frame
+ workingDir: Any empty directory, temporary file will be written here
+ ttfFile: Location of a font, need to be a Monospaced Font, I only tested Consolas
+ blank1: Need to prepare a 100 x 100 white picture, this picture is used as background to analyze char brightness
+ blank: Need to prepare a picture, width=picCols*8 height=picRows*16, this picture is used as background of output picture/video
+ imgType: '.png' or '.bmp', png saves disk space, bmp is faster
+ videoIn, videoOut, videoFramerate in asciiVideo.py: input and output video location and input video framerate
+ inputFile, outputFile in asciiPicture.py: input and output picture location
+ charpng, pngin, txt, pngout are contants, do not modify
