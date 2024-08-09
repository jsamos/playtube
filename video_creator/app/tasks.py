from redis import Redis
from rq import Queue
import json
import audio

redis_conn = Redis(host='redis', port=6379)
q = Queue(connection=redis_conn)

def playlist_created(json_string):
    data = json.loads(json_string)
    for track in data['tracks']:
        q.enqueue('tasks.track_found', json.dumps(track))
    print("PLAYLIST RECEIVED")
def track_found(json_string):
    print("TRACK RECEIVED")
    data = json.loads(json_string)
    data['image'] = audio.extract_album_cover(data['file'])
    print(data)
