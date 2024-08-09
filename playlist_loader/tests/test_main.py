import pytest
import app.main

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
    app.main.add_track_lengths(playlist)
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
    app.main.add_mix_length(playlist)
    assert playlist['length'] == expected_length
