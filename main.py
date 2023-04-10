import os
import sys
import yaml
import logging
import platform
from moviepy.editor import *
from multiprocessing import Process, Manager


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


def color_clip_process(size, duration, fps, color, output, process_num, results):
    logger.info(f'Process {process_num}: Creating color clip...')
    clip = ColorClip(size, color, duration=duration)
    logger.info(f'Process {process_num}: Writing video file...')
    clip.write_videofile(output, fps=fps)
    logger.info(f'Process {process_num}: Video file saved to {output}')
    results[process_num] = output


if __name__ == '__main__':
    CONFIG = ReadConfig()

    VIDEO_SIZE = (CONFIG['VIDEO_RESOLUTION']['VIDEO_RES_X'],CONFIG['VIDEO_RESOLUTION']['VIDEO_RES_Y'])
    DURATION = CONFIG['VIDEO_TEST_SETTINGS']['SAMPLE_RES_TEST_DURATION']
    FPS = CONFIG['VIDEO_SETTINGS']['FPS']
    OUTPUT_FOLDER = CONFIG['VIDEO_SETTINGS']['OUTPUT_FOLDER']
    OUTPUT_FILE = CONFIG['VIDEO_SETTINGS']['OUTPUT_FILE']
    OUTPUT_TYPE = CONFIG['VIDEO_SETTINGS']['OUTPUT_TYPE']
    NUM_PROCESSES = CONFIG.get('NUM_PROCESSES', os.cpu_count())

    if not os.path.exists(OUTPUT_FOLDER):
        os.mkdir(OUTPUT_FOLDER)

    manager = Manager()
    results = manager.dict()
    processes = []
    for i in range(NUM_PROCESSES):
        output = f"{OUTPUT_FOLDER}/{OUTPUT_FILE}_{i}.{OUTPUT_TYPE}"
        process = Process(target=color_clip_process, args=(VIDEO_SIZE, DURATION, FPS, (0,0,0), output, i, results))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    final_output = f"{OUTPUT_FOLDER}/{OUTPUT_FILE}.{OUTPUT_TYPE}"
    with VideoFileClip(results[0]) as final_clip:
        for i in range(1, NUM_PROCESSES):
            clip = VideoFileClip(results[i])
            final_clip = concatenate_videoclips([final_clip, clip])
        logger.info('Concatenating video clips...')
        final_clip.write_videofile(final_output, fps=FPS)
        logger.info(f'Final video file saved to {final_output}')

    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Py2TokVid - {platform.system()} Version")
