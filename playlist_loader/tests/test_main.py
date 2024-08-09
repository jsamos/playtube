import pytest
import app.main

def test_add_track_lengths():
    tracks = [
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
    expected_track_lengths = ['04:12', '04:00', None]
    app.main.add_track_lengths(tracks)
    for i, track in enumerate(tracks):
        assert track['length'] == expected_track_lengths[i]
