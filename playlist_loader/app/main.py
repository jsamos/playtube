import argparse
import cue

def load_tracks(cue_path):
    with open(cue_path) as f:
        cue_string = f.read()
    tracks = cue.parse_cue(cue_string)
    return tracks

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cue_path", help="Path to the cue file")
    args = parser.parse_args()

    cue_path = args.cue_path
    tracks = load_tracks(cue_path)
    print(tracks)