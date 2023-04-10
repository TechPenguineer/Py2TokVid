import os
import sys
import yaml
from moviepy.editor import *

def ReadConfig(config_file: str = "./util/config.yaml"):
    configDoc = str("")
    with open(config_file, "r") as configFile:
        configDoc = str(configFile.read())
    return yaml.safe_load(configDoc)
CONFIG = ReadConfig()

VIDEO_SIZE = (CONFIG['VIDEO_RESOLUTION']['VIDEO_RES_X'],CONFIG['VIDEO_RESOLUTION']['VIDEO_RES_Y'])
DURATION = CONFIG['VIDEO_TEST_SETTINGS']['SAMPLE_RES_TEST_DURATION']
FPS = CONFIG['VIDEO_SETTINGS']['FPS']
OUTPUT_FOLDER = CONFIG['VIDEO_SETTINGS']['OUTPUT_FOLDER']
OUTPUT_FILE = CONFIG['VIDEO_SETTINGS']['OUTPUT_FILE']
OUTPUT_TYPE = CONFIG['VIDEO_SETTINGS']['OUTPUT_TYPE']

def color_clip(size, duration, fps=25, color=(0,0,0), output='color.mp4'):
    ColorClip(size, color, duration=duration).write_videofile(output, fps=fps)

if not os.path.exists(OUTPUT_FOLDER):
    os.mkdir(OUTPUT_FOLDER)

color_clip(VIDEO_SIZE, DURATION, FPS, (0,0,0), f"{OUTPUT_FOLDER}/{OUTPUT_FILE}.{OUTPUT_TYPE}")