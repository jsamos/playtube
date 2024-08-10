import pytest
import os
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

@pytest.fixture
def tracks_all_exist():
    fixtures_dir = 'tests/fixtures'
    return [{"video": os.path.join(fixtures_dir, file)} for file in os.listdir(fixtures_dir) if os.path.isfile(os.path.join(fixtures_dir, file))]

@pytest.fixture
def tracks_with_nonexistent(tracks_all_exist):
    tracks = tracks_all_exist.copy()
    tracks.append({"video": "tests/fixtures/nonexistent.mp4"})
    return tracks

def test_check_all_tracks_processed_all_exist(tracks_all_exist):
    assert tasks.check_all_tracks_processed(tracks_all_exist) == True

def test_check_all_tracks_processed_with_nonexistent(tracks_with_nonexistent):
    assert tasks.check_all_tracks_processed(tracks_with_nonexistent) == False