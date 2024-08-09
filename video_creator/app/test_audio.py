import os
import pytest
from app.audio import *

@pytest.fixture
def audio_file():
    return 'tests/fixtures/Ezequiel G - Phatt Square.mp3'

@pytest.fixture
def expected_image_file(audio_file):
    base, _ = os.path.splitext(audio_file)
    return f"{base}.jpg"

def test_extract_album_artwork(audio_file, expected_image_file):
    # Run the function
    result = extract_album_artwork(audio_file)
    
    # Check if the PNG file is created
    assert os.path.exists(expected_image_file)
    assert result == expected_image_file

    # Clean up the created PNG file
    if os.path.exists(expected_image_file):
        os.remove(expected_image_file)