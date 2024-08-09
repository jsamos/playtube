import os
from mutagen import File
from mutagen.id3 import ID3, APIC
from mutagen.flac import Picture
from PIL import Image
import io

def list_all_tags(audio):
    # Load the audio file
    if audio is None:
        raise ValueError("Unsupported audio format or corrupted file")

    # Print all tags and their values
    if hasattr(audio, 'tags') and audio.tags is not None:
        for tag, value in audio.tags.items():
            print(f"Tag: {tag}, Value: {value}")
    else:
        print("No tags found or unsupported file type")

def extract_album_cover(file_path):
    # Load the audio file
    audio = File(file_path)

    if audio is None:
        raise ValueError("Unsupported audio format or corrupted file")

    image_data = None

    # Iterate through tags to find the APIC frame with the description 'Cover'
    if hasattr(audio, 'tags'):
        for tag in audio.tags.values():
            if isinstance(tag, APIC):
                if tag.desc == "Cover":  # Specifically check for 'Cover' description
                    image_data = tag.data
                    break
    if image_data is None:
        raise ValueError("No album artwork found in the audio file")

    # Determine the output image path
    base, _ = os.path.splitext(file_path)
    output_image_path = f"{base}.jpg"

    # Save the image data as a PNG file
    image = Image.open(io.BytesIO(image_data))
    image.save(output_image_path, format='JPEG')
    return output_image_path
