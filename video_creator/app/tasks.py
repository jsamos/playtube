import os
import json
import yaml
from redis import Redis
from rq import Queue
from . import video
import time

# Load configuration
with open(os.path.join(os.path.dirname(__file__), '../config.yaml'), 'r') as config_file:
    config = yaml.safe_load(config_file)

redis_conn = Redis(host=config['redis']['host'], port=config['redis']['port'])
q = Queue(connection=redis_conn)

def playlist_created(json_string):
    data = json.loads(json_string)
    for track in data['tracks']:
        q.enqueue('tasks.track_found', json.dumps(track))
    q.enqueue('tasks.tracks_enqueued', json.dumps(data))
    print("PLAYLIST TRACKS ENQUEUED")

def track_found(json_string):
    print("TRACK RECEIVED")
    data = json.loads(json_string)
    video.create_video_from_image(data)
    print(data)

def check_all_tracks_processed(tracks):
    return all(os.path.exists(track['video']) for track in tracks)

def tracks_enqueued(json_string, wait_time=config['track_processing']['pause_time'], time_out=config['track_processing']['time_out']):
    print("TRACKS ENQUEUED")
    data = json.loads(json_string)
    start_time = time.time()
    while not check_all_tracks_processed(data['tracks']):
        if time.time() - start_time > time_out:
            print('TIMEOUT PROCESSING FILES')
            return
        else:
            print(f"WAITING FOR ALL TRACKS TO BE PROCESSED (wait time: {wait_time} seconds)") 
            time.sleep(wait_time)
    
    q.enqueue('tasks.video_files_created', json_string)

def video_files_created(json_string):
    print("VIDEO FILES CREATED")
    data = json.loads(json_string)
    video_paths = [track['video'] for track in data['tracks']]
    combined_video_path = video.combine_videos(video_paths)
    print(f"Combined video created: {combined_video_path}")
    q.enqueue('tasks.combined_video_created', json_string)

def combined_video_created(json_string):
    print("COMBINED VIDEO CREATED")
    data = json.loads(json_string)
    print(f"Playlist video created: {data['video']}")
