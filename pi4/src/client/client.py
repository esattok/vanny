import base64
from multiprocessing import Queue, Process

import cv2
import numpy as np
import zmq
from zmq.utils.strtypes import unicode

'''client code'''


class Client:
    def __init__(self):
        self.CHUNK_SIZE = 250000
        self.PIPELINE = 10
        self.ctx = zmq.Context()
        self.reports_count = 0

    def display_stream(self):
        print("displayer is on")
        self.stream_context = self.ctx
        self.stream_socket = self.stream_context.socket(zmq.SUB)
        self.stream_socket.connect("tcp://localhost:5555")
        self.stream_socket.setsockopt_string(zmq.SUBSCRIBE, unicode(''))

        while True:
            encoded_frame = self.stream_socket.recv()
            frame = cv2.imdecode(np.frombuffer(encoded_frame, dtype=np.uint8), cv2.IMREAD_COLOR)

            cv2.imshow("Receiver", frame)
            if cv2.waitKey(1) == ord('q'):
                break

        cv2.destroyAllWindows()


def cont_reporting():
    client = Client()

    while True:
        reporter(client)
        client.reports_count += 1


def reporter(client):
    print("reporter on")

    dealer = client.ctx.socket(zmq.DEALER)
    dealer.connect("tcp://127.0.0.1:6000")

    credit = client.PIPELINE  # Up to PIPELINE chunks in transit

    total = 0  # Total bytes received
    chunks = 0  # Total chunks received
    offset = 0  # Offset of next chunk request
    count = 0
    f = open("report_{}.mp4".format(client.reports_count), 'wb+')

    print("before loop")
    while True:
        while credit:
            # ask for next chunk
            dealer.send_multipart([
                b"fetch",
                b"%i" % offset,
                b"%i" % client.CHUNK_SIZE,
            ])

            offset += client.CHUNK_SIZE
            credit -= 1

        try:
            chunk = dealer.recv()
        except zmq.ZMQError as e:
            if e.errno == zmq.ETERM:
                return  # shutting down, quit
            else:
                raise

        chunks += 1
        credit += 1
        size = len(chunk)
        f.write(chunk)
        total += size

        if size < client.CHUNK_SIZE:
            break

    client.reports_count += 1
    f.close()
    print("%i chunks received, %i bytes" % (chunks, total))
    print("done cli")


if __name__ == '__main__':
    print("re")
    report_process = Process(target=cont_reporting, args=())
    report_process.start()
    cli = Client()
    cli.display_stream()
