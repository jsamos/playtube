import pytest
import os
import app.tasks as tasks
import json
from unittest.mock import patch
import tempfile

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
        mock_enqueue.assert_any_call('app.tasks.track_found', json.dumps({"file": "track1.mp3"}))
        mock_enqueue.assert_any_call('app.tasks.track_found', json.dumps({"file": "track2.mp3"}))
        mock_enqueue.assert_any_call('app.tasks.tracks_enqueued', json_string)

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

def test_tracks_enqueued():
    json_string = json.dumps({
        "tracks": [
            {"file": "video1.mp4"},
            {"file": "video2.mp4"}
        ]
    })

    with patch('app.tasks.check_all_tracks_processed', side_effect=[False, True]) as mock_check, \
         patch('app.tasks.q.enqueue') as mock_enqueue:
        tasks.tracks_enqueued(json_string, wait_time=1)

        # Check that check_all_tracks_processed was called twice
        assert mock_check.call_count == 2

        # Check that q.enqueue was called with 'tasks.video_files_created'
        mock_enqueue.assert_called_with('app.tasks.video_files_created', json_string)

def test_tracks_enqueued_timeout():
    json_string = json.dumps({
        "tracks": [
            {"file": "video1.mp4"},
            {"file": "video2.mp4"}
        ]
    })

    with patch('app.tasks.check_all_tracks_processed', return_value=False) as mock_check, \
         patch('app.tasks.q.enqueue') as mock_enqueue:
        tasks.tracks_enqueued(json_string, wait_time=0, time_out=0)

        # Check that check_all_tracks_processed was called once
        assert mock_check.call_count == 1

        # Check that q.enqueue was not called
        mock_enqueue.assert_not_called()

def test_video_files_created():
    json_string = json.dumps({
        "tracks": [
            {"video": "video1.mp4"},
            {"video": "video2.mp4"},
            {"video": "video3.mp4"},
            {"video": "video4.mp4"}
        ]
    })

    with patch('app.video.combine_videos', return_value='combined_video.mp4') as mock_combine_videos:
        with patch('app.tasks.q.enqueue') as mock_enqueue:
            tasks.video_files_created(json_string)

            # Check that combine_videos was called once with the correct arguments
            mock_combine_videos.assert_called_once_with([
                "video1.mp4",
                "video2.mp4",
                "video3.mp4",
                "video4.mp4"
            ])

            # Check that q.enqueue was called once with the correct argument
            mock_enqueue.assert_called_once_with('app.tasks.combined_video_created', json_string)

def test_combined_video_created():
    temp_files = []
    try:
        # Create temporary video and image files for tracks
        tracks = []
        for i in range(4):
            video_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
            image_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
            tracks.append({"video": video_file.name, "image": image_file.name})
            temp_files.extend([video_file.name, image_file.name])

        json_string = json.dumps({"tracks": tracks})

        # Call the combined_video_created function
        tasks.combined_video_created(json_string)

        # Assert that the temporary files were removed
        for temp_file in temp_files:
            assert not os.path.exists(temp_file)
    finally:
        # Clean up any remaining temporary files
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)