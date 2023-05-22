import os
import subprocess
import time
import zmq


def server_thread(filename):
    file = open(filename, "rb")
    ctx = zmq.Context()
    router = ctx.socket(zmq.ROUTER)
    router.bind("tcp://*:6000")
    print("Server")

    while True:
        # First frame in each message is the sender identity
        # Second frame is "fetch" command
        try:
            msg = router.recv_multipart()
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                return  # shutting down, quit
            else:
                raise

        identity, command, offset_str, chunksz_str = msg

        assert command == b"fetch"

        offset = int(offset_str)
        chunksz = int(chunksz_str)

        # Read chunk of data from file
        file.seek(offset, os.SEEK_SET)
        data = file.read(chunksz)
        time.sleep(0.01)

        # Send resulting chunk to client
        router.send_multipart([identity, data])

        # Break when all data is read
        if not data:
            break
    print("done serv")


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
    cmd = "ffmpeg -fflags +discardcorrupt -y -ac 2 -r {} -channel_layout stereo -i audio_capture_{}.wav -i video_capture_{}.avi  capture_{}.avi".format(
        fps, video_count, video_count, video_count)
    subprocess.run(cmd, shell=True)
    server_thread("capture_{}.avi".format(video_count))

    pass
