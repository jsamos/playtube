import pytest
import app.tasks as tasks
import json
from unittest.mock import patch

def test_track_found():
    data = {
        "file": "track1.mp3"
    }

    with patch('app.tasks.video.create_video_from_image') as mock_create_video:
        tasks.track_found(json.dumps(data))

        # Check that create_video_from_image was called once
        assert mock_create_video.call_count == 1

        # Check the arguments passed to create_video_from_image
        mock_create_video.assert_called_with(data)

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
        assert mock_enqueue.call_count == 3

        # Check the arguments passed to enqueue
        mock_enqueue.assert_any_call('tasks.track_found', json.dumps({"file": "track1.mp3"}))
        mock_enqueue.assert_any_call('tasks.track_found', json.dumps({"file": "track2.mp3"}))
        mock_enqueue.assert_any_call('tasks.tracks_enqueued', json_string)