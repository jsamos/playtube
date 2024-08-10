import pytest
import os
import json
from unittest.mock import patch
import moviepy.editor as mp
import app.video
import tempfile

def test_create_video_from_image():
    data = {
        "image": "/code/tests/fixtures/Fickry - Confusion.jpg",
        "file": "/code/tests/fixtures/Fickry - Confusion.mp3",
        "length": "00:02",
        "video": "/code/tests/fixtures/Fickry - Confusion.mp4"
    }
    
    app.video.create_video_from_image(data)

    assert os.path.exists(data['video'])

    video = mp.VideoFileClip(data['video'])
    duration = video.duration
    minutes = int(duration // 60)
    seconds = int(duration % 60)
    actual_length = f"{minutes:02d}:{seconds:02d}"

    assert actual_length == data['length']
    
    os.remove(data['video'])

def create_temp_video_file(duration, filename):
    clip = mp.ColorClip(size=(640, 480), color=(255, 0, 0), duration=duration)
    clip.fps = 24
    clip.write_videofile(filename, codec='libx264')
    return filename

def test_combine_videos():
    temp_files = []
    try:
        # Create 4 temporary video files of 1 second each
        for i in range(4):
            temp_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
            temp_files.append(create_temp_video_file(1, temp_file.name))
        
        # Combine the videos
        combined_video_path = app.video.combine_videos(temp_files)
        
        # Check that the combined video file exists
        assert os.path.exists(combined_video_path)
        
        # Check the length of the combined video
        combined_video = mp.VideoFileClip(combined_video_path)
        duration = combined_video.duration
        assert duration == 4  # 4 seconds
    finally:
        # Clean up temporary files
        for temp_file in temp_files:
            os.remove(temp_file)
        if os.path.exists(combined_video_path):
            os.remove(combined_video_path)