import pytest
import main
from unittest.mock import patch

def test_add_track_lengths():
    playlist = {
        'title': 'Mix 1',
        'performer': 'DJ Copilot',
        'file': 'tests/fixtures/fixture.mp3',
        'track': '01',
        'index': '00:00:00',
        'length': '00:13:09',
        'tracks': [
            {
                'title': 'Confusion',
                'performer': 'Fickry',
                'file': '/data/240607-V1P1/Fickry - Confusion.mp3',
                'track': '01',
                'index': '00:00:00'
            },
            {
                'title': "What's Luv (Original Mix)",
                'performer': 'Carlos A, G-Falex',
                'file': "/data/240607-V1P1/Carlos A, G-Falex - What's Luv (Original Mix).mp3",
                'track': '02',
                'index': '00:04:12'
            },
            {
                'title': "What's Luv (Original Mix)",
                'performer': 'Carlos A, G-Falex',
                'file': "/data/240607-V1P1/Carlos A, G-Falex - What's Luv (Original Mix).mp3",
                'track': '03',
                'index': '00:08:12'
            }
        ]
    }
    # NOTE: difference between 00:08:12 and 00:13:09 is 04:57
    expected_track_lengths = ['04:12', '04:00', '04:57']
    main.add_track_lengths(playlist)
    for i, track in enumerate(playlist['tracks']):
        assert track['length'] == expected_track_lengths[i]

def test_add_mix_length():
    playlist = {
        'title': 'Mix 1',
        'performer': 'DJ Copilot',
        'file': 'tests/fixtures/fixture.mp3',
        'track': '01',
        'index': '00:00:00'
    }
    expected_length = "00:00:12"
    main.add_mix_length(playlist)
    assert playlist['length'] == expected_length

def test_get_video_file_path():
    file_path = "/path/to/video.avi"
    expected_result = "/path/to/video.mp4"
    result = main.get_video_file_path(file_path)
    assert result == expected_result

def test_get_video_file_path_empty_string():
    file_path = ""
    expected_result = ""
    result = main.get_video_file_path(file_path)
    assert result == expected_result

@pytest.fixture
def playlist():
    return {
        'tracks': [
            {'file': 'tests/fixtures/Fickry - Confusion.mp3'},
            {'file': 'tests/fixtures/Another - Track.mp3'}
        ]
    }

def test_create_media_and_add_paths(playlist):
    with patch('app.audio.extract_album_cover', return_value='tests/fixtures/Another - Track.jpg') as mock_extract_album_cover:
        main.create_media_and_add_paths(playlist)
        
        # Check if extract_album_cover was called for each track
        assert mock_extract_album_cover.call_count == len(playlist['tracks'])

        # Check if the media file paths were set correctly
        assert playlist['tracks'][0]['image'] == 'tests/fixtures/Another - Track.jpg'
        assert playlist['tracks'][1]['image'] == 'tests/fixtures/Another - Track.jpg'
        assert playlist['tracks'][0]['video'] == 'tests/fixtures/Fickry - Confusion.mp4'
        assert playlist['tracks'][1]['video'] == 'tests/fixtures/Another - Track.mp4'
