from moviepy.editor import ImageClip
import re
import subprocess
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

def create_video_from_image(data):
    # Extract length and image from the dictionary
    length_str = data.get('length', '00:00')
    image_path = data.get('image')
    output_path = data.get('video')
    
    # Convert the length from mm:ss to seconds
    match = re.match(r'(\d+):(\d+)', length_str)
    if match:
        minutes = int(match.group(1))
        seconds = int(match.group(2))
        total_seconds = minutes * 60 + seconds
    else:
        raise ValueError("Invalid length format. Expected mm:ss.")

    # Use FFmpeg to create the video
    command = [
        'ffmpeg',
        '-loop', '1',  # Loop the image to create a video
        '-i', image_path,  # Input image
        '-c:v', 'libx264',  # Video codec
        '-t', str(total_seconds),  # Duration in seconds
        '-pix_fmt', 'yuv420p',  # Pixel format for compatibility
        '-vf', 'fps=24',  # Set frame rate to 24 fps
        output_path  # Output video file
    ]
    
    # Run the FFmpeg command
    subprocess.run(command, check=True)
    
    print(f"Video created successfully: {output_path}")
    return output_path

def combine_videos(video_paths):
    # Determine the output path from the directory of the first video
    output_dir = os.path.dirname(video_paths[0])
    output_path = os.path.join(output_dir, 'combined_video.mp4')
    # Load all video clips
    video_clips = [VideoFileClip(path) for path in video_paths]
    
    # Concatenate the video clips
    final_clip = concatenate_videoclips(video_clips)
    
    # Write the final video to a file
    final_clip.write_videofile(output_path, codec='libx264', fps=24)    
    return output_path