import os
import yaml
import logging
import platform
from moviepy.editor import *
from multiprocessing import Pool


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define custom log formatter with color and weight
log_formatter = logging.Formatter("\033[1m%(asctime)s [%(levelname)s] %(name)s:\033[0m %(message)s")
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)


def read_config(config_file: str = "./util/config.yaml") -> dict:
    logger.info('Opening config...')
    with open(config_file, "r") as f:
        config = yaml.safe_load(f)
    logger.info('Config loaded.')
    return config


def create_color_clip(args):
    process_num, size, duration, fps, color, output = args
    logger.info(f'Process {process_num}: Creating color clip...')
    clip = ColorClip(size, color, duration=duration)
    logger.info(f'Process {process_num}: Writing video file...')
    clip.write_videofile(output, fps=fps)
    logger.info(f'Process {process_num}: \033[32mVideo file saved to {output}\033[0m')
    return output


if __name__ == '__main__':
    config = read_config()
    video_size = (config['VIDEO_RESOLUTION']['VIDEO_RES_X'], config['VIDEO_RESOLUTION']['VIDEO_RES_Y'])
    duration = config['VIDEO_TEST_SETTINGS']['SAMPLE_RES_TEST_DURATION']
    fps = config['VIDEO_SETTINGS']['FPS']
    output_folder = config['VIDEO_SETTINGS']['OUTPUT_FOLDER']
    output_file = config['VIDEO_SETTINGS']['OUTPUT_FILE']
    output_type = config['VIDEO_SETTINGS']['OUTPUT_TYPE']
    num_processes = config.get('NUM_PROCESSES', os.cpu_count())

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    args = [(i, video_size, duration, fps, (0, 0, 0), f"{output_folder}/{output_file}_{i}.{output_type}") for i in range(num_processes)]
    with Pool(num_processes) as p:
        results = p.map(create_color_clip, args)

    final_output = f"{output_folder}/{output_file}.{output_type}"
    clips = [VideoFileClip(r) for r in results]
    final_clip = concatenate_videoclips(clips)
    logger.info('\033[34mConcatenating video clips...\033[0m')
    final_clip.write_videofile(final_output, fps=fps)
    logger.info(f'\033[32mFinal video file saved to {final_output}\033[0m')

    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"\033[1mPy2TokVid\033[0m - {platform.system()} Version")
