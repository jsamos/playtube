import os
from redis import Redis
from rq import Queue
import json
from . import video

redis_conn = Redis(host='redis', port=6379)
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

def tracks_enqueued():
    print("TRACKS ENQUEUED")
    print("WAITING FOR ALL TRACKS TO BE PROCESSED") 
    print(q.get_job_ids())
    return q.get_job_ids()