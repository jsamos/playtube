import pytest
import os
import json
from unittest.mock import patch
import moviepy.editor as mp
import app.video

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