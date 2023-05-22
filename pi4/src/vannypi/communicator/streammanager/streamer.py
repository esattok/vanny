import base64
from multiprocessing import Queue, Process

import cv2
import numpy as np

from vannypi.communicator.streammanager.stream_manager import StreamManager
from vannypi.inputmanagement.videomanager.video import Video
import zmq


class Streamer:

    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://*:5555")


def stream(mq: Queue) -> None:
    streamer = Streamer()
    streamer.queue = mq

    while True:
        frame = streamer.queue.get()

        if isinstance(frame, str):
            print("no more stream")
            break

        encoded_frame = cv2.imencode('.jpg', frame)[1].tobytes()
        streamer.socket.send(encoded_frame)

        #cv2.imshow("Sender", frame)
        #if cv2.waitKey(1) == ord('q'):
        #    break

        #cv2.destroyAllWindows()


def start_streaming_process(mq):
    streaming_process = Process(target=stream, args=(mq,))
    streaming_process.start()


