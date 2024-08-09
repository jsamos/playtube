import os
import pytest
from app.audio import *

def test_get_audio_length():
    file_path = "tests/fixtures/fixture.mp3"
    expected_length = 12
    assert get_audio_length(file_path) == expected_length