# subtitle-renamer
Description

The Subtitle Renamer is a Python script designed to help users organize and rename subtitle files (.srt, .sub, etc.) according to a specified naming convention. This tool is particularly useful for media libraries where subtitles need to match the naming of video files for seamless playback.
  

Features

    Batch Renaming: Rename multiple subtitle files in a single run.
    Custom Naming Convention: Specify a naming pattern that includes the base name of the video file.
    File Type Support: Supports common subtitle file formats such as .srt and .sub.
    Error Handling: Gracefully handles errors such as missing files or incorrect formats.

Requirements

    Python 3.x
    os and re modules (included in the Python standard library)

Usage

    Clone the repository:

bash

git clone https://github.com/yourusername/subtitle-renamer.git
cd subtitle-renamer

Place your subtitle files in the same directory as the script or specify the path in the script.

Run the script:

    python subtitle_renamer.py

    Follow the prompts to enter the base name for the subtitles.

Example

If you have a video file named movie_title.mp4 and corresponding subtitle files like movie_title_1.srt, movie_title_2.srt, the script can rename them to a consistent format such as movie_title.srt, movie_title_1.srt, etc.
