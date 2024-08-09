import pytest
import pytest
import os
import time
import app.tasks as tasks
import moviepy.editor as mp
import json
from unittest.mock import patch

def test_get_video_file_path():
    file_path = "/path/to/video.avi"
    expected_result = "/path/to/video.mp4"
    
    result = tasks.get_video_file_path(file_path)
    
    assert result == expected_result
def test_get_video_file_path_empty_string():
    file_path = ""
    expected_result = ""
    
    result = tasks.get_video_file_path(file_path)
    
    assert result == expected_result

def test_track_found():
    mp3_path = "/code/tests/fixtures/Fickry - Confusion.mp3"
    image_path = "/code/tests/fixtures/Fickry - Confusion.jpg"
    video_file_path = "/code/tests/fixtures/Fickry - Confusion.mp4"
    expected_length = "00:02"

    data = {
        "image": image_path,
        "file": mp3_path,
        "length": expected_length
    }

    json_string = json.dumps(data)
    
    tasks.track_found(json_string)
    
    assert os.path.exists(video_file_path)
    
    video = mp.VideoFileClip(video_file_path)
    duration = video.duration
    minutes = int(duration // 60)
    seconds = int(duration % 60)
    actual_length = f"{minutes:02d}:{seconds:02d}"

    assert actual_length == expected_length
    
    os.remove(video_file_path)

def test_playlist_created():
    json_string = json.dumps({
        "tracks": [
            {"file": "track1.mp3"},
            {"file": "track2.mp3"}
        ]
    })

    with patch('app.tasks.q.enqueue') as mock_enqueue:
        tasks.playlist_created(json_string)

        # Check that enqueue was called twice
        assert mock_enqueue.call_count == 2

        # Check the arguments passed to enqueue
        mock_enqueue.assert_any_call('tasks.track_found', json.dumps({"file": "track1.mp3"}))
        mock_enqueue.assert_any_call('tasks.track_found', json.dumps({"file": "track2.mp3"}))