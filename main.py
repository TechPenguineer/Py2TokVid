import os
import sys
import yaml
import logging
from moviepy.editor import *
import platform


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ReadConfig(config_file: str = "./util/config.yaml"):
    configDoc = str("")
    with open(config_file, "r") as configFile:
        logger.info('Opening config...')
        configDoc = str(configFile.read())
        logger.info('Log read...')
    logger.info('Returning YAML safe load...')
    return yaml.safe_load(configDoc)
CONFIG = ReadConfig()

VIDEO_SIZE = (CONFIG['VIDEO_RESOLUTION']['VIDEO_RES_X'],CONFIG['VIDEO_RESOLUTION']['VIDEO_RES_Y'])
DURATION = CONFIG['VIDEO_TEST_SETTINGS']['SAMPLE_RES_TEST_DURATION']
FPS = CONFIG['VIDEO_SETTINGS']['FPS']
OUTPUT_FOLDER = CONFIG['VIDEO_SETTINGS']['OUTPUT_FOLDER']
OUTPUT_FILE = CONFIG['VIDEO_SETTINGS']['OUTPUT_FILE']
OUTPUT_TYPE = CONFIG['VIDEO_SETTINGS']['OUTPUT_TYPE']

def color_clip(size, duration, fps=25, color=(0,0,0), output='color.mp4'):
    logger.info('Creating color clip...')
    clip = ColorClip(size, color, duration=duration)
    logger.info('Writing video file...')
    clip.write_videofile(output, fps=fps)
    logger.info(f'Video file saved to {output}')

if not os.path.exists(OUTPUT_FOLDER):
    os.mkdir(OUTPUT_FOLDER)

os.system('cls' if os.name == 'nt' else 'clear')
color_clip(VIDEO_SIZE, DURATION, FPS, (0,0,0), f"{OUTPUT_FOLDER}/{OUTPUT_FILE}.{OUTPUT_TYPE}")
os.system('cls' if os.name == 'nt' else 'clear')

print(f"Py2TokVid - {platform.system()} Version")