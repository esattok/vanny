import subprocess
import time
from typing import List

def _import_raw_data(raw_data: List[float]) -> None:
    pass


def _calculate_frame_rate(frames_count: int, duration_s: int) -> float:
    return frames_count / duration_s


def encode(video_count: int, frames_count: int, duration_s: int) -> None:
    import os.path
    while not os.path.isfile(os.getcwd() + '/' + "audio_capture_{}.wav".format(video_count)):
        print(os.getcwd() + '/' + "audio_capture_{}.wav")
        print("audio file not found")
        time.sleep(0.1)

    fps = _calculate_frame_rate(frames_count, duration_s)
    print("actual fps", fps)

    time.sleep(1)
    cmd = "ffmpeg -fflags +discardcorrupt -y -ac 2 -r {} -channel_layout stereo -i audio_capture_{}.wav -i video_capture_{}.avi -pix_fmt yuv420p capture_{}.avi".format(
        fps, video_count, video_count, video_count)
    subprocess.call(cmd, shell=True)
    pass
