import argparse
from app import cue
from app import audio

def load_tracks(cue_path):
    with open(cue_path) as f:
        cue_string = f.read()
    tracks = cue.parse_cue_tracks(cue_string)
    return tracks

def convert_time_to_seconds(time):
    return int(time[:2]) * 3600 + int(time[3:5]) * 60 + int(time[6:8])

def add_mix_length(playlist):
    audio_length = audio.get_audio_length(playlist['file'])
    length = f"{audio_length // 3600:02d}:{(audio_length % 3600) // 60:02d}:{audio_length % 60:02d}"
    playlist['length'] = length


"""
{
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
"""
def add_track_lengths(playlist):
    tracks = playlist['tracks']
    mix_length_seconds = convert_time_to_seconds(playlist['length'])

    for i in range(len(tracks)):
        current_track = tracks[i]
        current_index = current_track['index']
        current_seconds = convert_time_to_seconds(current_index)

        if i ==  len(tracks) - 1:
            length_seconds = mix_length_seconds - current_seconds
        else:  
            next_track = tracks[i + 1]
            next_index = next_track['index']
            next_seconds = convert_time_to_seconds(next_index)
            length_seconds = next_seconds - current_seconds
            
        length = f"{length_seconds // 60:02d}:{length_seconds % 60:02d}"
        tracks[i]['length'] = length
    #tracks[-1]['length'] = None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cue_path", help="Path to the cue file")
    args = parser.parse_args()

    cue_path = args.cue_path
    tracks = load_tracks(cue_path)
    print(tracks)