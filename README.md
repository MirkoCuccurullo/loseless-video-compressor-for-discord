# LOSELESS VIDEO COMPRESSOR FOR DISCORD AND EMAILS

## Installation:

Python 3.10 or above needed.

Step-by-Step Guide
1. Download FFmpeg:

Go to the FFmpeg download page.
Choose the correct version for Windows and download the executable.
Extract FFmpeg:

2. Extract the contents of the downloaded archive to a folder, e.g., C:\ffmpeg.

3. Add FFmpeg to PATH:

Press Win + X and select System.
Click on Advanced system settings.
Click on Environment Variables.
In the System variables section, find the Path variable and click Edit.
Click New and add C:\ffmpeg\bin. ( this must be the same path as where you extracted the folder)
Click OK to close all dialog boxes.
Verify FFmpeg Installation:

4. Open a new command prompt and type ffmpeg -version

5. Install package by using:

```bash
pip install ffmpeg-python
```
 ## Usage:

 1. paste the video you want compres in this folder and call it 'input.mp4'

 2. run the command 
 ```bash
 python3 compress.py
 ```

 This will output the compressed video as 'output.mp4'