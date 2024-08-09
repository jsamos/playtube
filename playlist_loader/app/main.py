import argparse
from . import cue
from . import audio
from redis import Redis
from rq import Queue
import json

redis_conn = Redis(host='redis', port=6379)
q = Queue(connection=redis_conn)

def load_mix(cue_path):
    with open(cue_path) as f:
        cue_string = f.read()
    return cue.parse_cue(cue_string)

def convert_time_to_seconds(time):
    return int(time[:2]) * 3600 + int(time[3:5]) * 60 + int(time[6:8])

def add_mix_length(playlist):
    audio_length = audio.get_audio_length(playlist['file'])
    length = f"{audio_length // 3600:02d}:{(audio_length % 3600) // 60:02d}:{audio_length % 60:02d}"
    playlist['length'] = length

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cue_path", help="Path to the cue file")
    args = parser.parse_args()
    playlist = load_mix(args.cue_path)
    add_mix_length(playlist)
    add_track_lengths(playlist)
    playlist_json = json.dumps(playlist)
    q.enqueue('tasks.playlist_created', playlist_json)