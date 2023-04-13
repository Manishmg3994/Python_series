# install all those packages/modules first then
# python main.py  --urls "['https://download.samplelib.com/mp4/sample-5s.mp4', 'https://download.samplelib.com/mp4/sample-10s.mp4']" --output "output.mp4" 

import argparse
import os
import subprocess
import ast
import requests
import datetime
import json
# conditional comment if not required
# import facebook

from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import concatenate_videoclips


# Parse command-line arguments
parser = argparse.ArgumentParser(description="Download and concatenate videos from URL links.")
parser.add_argument("--urls", type=str, default=None, help="video URL links as '[]' list string")
parser.add_argument("--intro", type=str, default=None, help="Path to intro video file directory")
parser.add_argument("--outro", type=str, default=None, help="Path to outro video file directory")
parser.add_argument("--output", type=str, default="output.mp4", help="Name of the output file")
# parser.add_argument("--tokenjson", type=str, default=None, help="Full token Json file as String")
# parser.add_argument("--clientjson", type=str, default=None, help="Full client Json file as String")
# parser.add_argument("--scopes", type=str, default=None, help="Full client Json file as String") # or add them as org secr or default
args = parser.parse_args()

# client_secrets_file = "client_secret.json"
# tokenjson = "token.json"


# # save Scopes
# str_scope_list = args.scopes
# scopes = ast.literal_eval(str_scope_list)


# with open(tokenjson, 'w') as f:
#     json.dump(json.loads(args.tokenjson), f)


# with open(client_secrets_file, 'w') as f:
#     json.dump(json.loads(args.clientjson), f)


# Download and validate the videos
video_clips = []
for url in ast.literal_eval(args.urls):
    r = requests.get(url)
    if r.status_code == 200:
        content_type = r.headers.get("content-type")
        if "video" in content_type:
            # save the video file to disk
            filename = os.path.basename(url)
            with open(filename, "wb") as f:
                f.write(r.content)

            # validate that the file is a video
            try:
                video_clip = VideoFileClip(filename)
                video_clips.append(video_clip)
            except Exception as e:
                print(f"[WARN] {filename} is not a valid video file")

        else:
            print(f"[WARN] {url} does not appear to be a video file")
    else:
        print(f"[ERROR] Failed to download {url}")

# Prepare the video clips
if args.intro is not None:
    intro_clip = VideoFileClip(args.intro)
    video_clips.insert(0, intro_clip)


if args.outro is not None:
    outro_clip = VideoFileClip(args.outro)
    video_clips.append(outro_clip)

# Concatenate the video clips
concatenated_clip = concatenate_videoclips(video_clips)

# Write the output file
output_file = os.path.join(os.getcwd(), args.output)
concatenated_clip.write_videofile(output_file)

# path in env  saved 
output_path = os.path.abspath(output_file)
