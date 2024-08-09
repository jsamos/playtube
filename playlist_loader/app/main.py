import argparse
from app import cue
from app import audio

def load_tracks(cue_path):
    with open(cue_path) as f:
        cue_string = f.read()
    tracks = cue.parse_cue_tracks(cue_string)
    return tracks

def add_mix_length(playlist):
    audio_length = audio.get_audio_length(playlist['file'])
    length = f"{audio_length // 3600:02d}:{(audio_length % 3600) // 60:02d}:{audio_length % 60:02d}"
    playlist['length'] = length


"""
takes and array of dictionaries and calculates the length of each track in mm:ss format
length of track i = index of track i+1 - index of track i
in the case of the last track lenghth = None
"""
def add_track_lengths(tracks):
    for i in range(len(tracks) - 1):
        current_track = tracks[i]
        current_index = current_track['index']
        current_seconds = int(current_index[:2]) * 3600 + int(current_index[3:5]) * 60 + int(current_index[6:8])

        next_track = tracks[i + 1]
        next_index = next_track['index']
        next_seconds = int(next_index[:2]) * 3600 + int(next_index[3:5]) * 60 + int(next_index[6:8])
        
        length_seconds = next_seconds - current_seconds
        length = f"{length_seconds // 60:02d}:{length_seconds % 60:02d}"
        tracks[i]['length'] = length
    tracks[-1]['length'] = None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cue_path", help="Path to the cue file")
    args = parser.parse_args()

    cue_path = args.cue_path
    tracks = load_tracks(cue_path)
    print(tracks)