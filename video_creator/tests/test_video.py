# video_creator/tests/test_video.py

import pytest
from unittest.mock import patch
import app.video as video

def test_create_video_from_image():
    data = {
        'length': '00:02',
        'image': '/path/to/image.jpg',
        'video': '/path/to/output.mp4'
    }

    expected_command = [
        'ffmpeg',
        '-loop', '1',
        '-i', data['image'],
        '-c:v', 'libx264',
        '-t', '2',
        '-pix_fmt', 'yuv420p',
        '-vf', 'fps=24',
        data['video']
    ]

    with patch('subprocess.run') as mock_run:
        video.create_video_from_image(data)
        mock_run.assert_called_once_with(expected_command, check=True)