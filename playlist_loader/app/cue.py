"""
the format of the cue file is as follows:
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
def parse_cue(cue_string):
    tracks = []
    lines = cue_string.split('\n')
    track_info = {}
    for line in lines:
        line = line.strip()
        if line.startswith('TRACK'):
            if track_info:
                tracks.append(track_info)
            track_info = {"track": line.split(' ')[1]}
        elif line.startswith('TITLE') and track_info:
            track_info['title'] = line.split('"')[1]
        elif line.startswith('PERFORMER') and track_info:
            track_info['performer'] = line.split('"')[1]
        elif line.startswith('FILE') and track_info:
            track_info['file'] = line.split('"')[1]
        elif line.startswith('INDEX 01') and track_info:
            track_info['index'] = line.split(' ')[2]
    if track_info:
        tracks.append(track_info)
    return tracks
