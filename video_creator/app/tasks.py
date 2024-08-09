import os
from redis import Redis
from rq import Queue
import json
from . import audio, video

redis_conn = Redis(host='redis', port=6379)
q = Queue(connection=redis_conn)

def get_video_file_path(file_path):
    if not file_path:
        return ''
    image_dir = os.path.dirname(file_path)
    output_filename = os.path.basename(file_path)
    output_filename = os.path.splitext(output_filename)[0]  # Remove file extension
    output_path = os.path.join(image_dir, f'{output_filename}.mp4')
    return output_path

def playlist_created(json_string):
    data = json.loads(json_string)
    for track in data['tracks']:
        q.enqueue('tasks.track_found', json.dumps(track))
    print("PLAYLIST RECEIVED")

def track_found(json_string):
    print("TRACK RECEIVED")
    data = json.loads(json_string)
    data['image'] = audio.extract_album_cover(data['file'])
    data['video'] = get_video_file_path(data['image'] )
    video.create_video_from_image(data)
    print(data)
