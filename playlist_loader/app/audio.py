from mutagen import File

def get_audio_length(file_path):
    audio = File(file_path)
    if audio is not None and audio.info is not None:
        return round(audio.info.length + 0.5)
    else:
        raise ValueError("Unsupported audio format or corrupted file")
