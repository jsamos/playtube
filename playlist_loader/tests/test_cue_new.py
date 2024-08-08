from app.cue import parse_cue
import pytest

def test_parse_cue():
    cue_string = """
        REM DATE 2024-06-10 08:14 PM
        REM RECORDED_BY "rekordbox-dj"
        TITLE "240607-V1P1"
        PERFORMER "B Tweed"
        FILE "01 240607-V1P1.wav" WAVE
            TRACK 01 AUDIO
                TITLE "Confusion"
                PERFORMER "Fickry"
                FILE "/data/240607-V1P1/Fickry - Confusion.mp3" WAVE
                INDEX 01 00:00:00
            TRACK 02 AUDIO
                TITLE "What's Luv (Original Mix)"
                PERFORMER "Carlos A, G-Falex"
                FILE "/data/240607-V1P1/Carlos A, G-Falex - What's Luv (Original Mix).mp3" WAVE
                INDEX 01 00:04:12
    """
    expected_tracks = [
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
        }
    ]
    actual_tracks = parse_cue(cue_string)
    
    assert actual_tracks == expected_tracks         