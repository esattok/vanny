import os
from multiprocessing import Queue, get_context

from typing import List

import cv2
import sys
import time
from tflite_support.task import vision
import numpy as np

from vannypi.inputanalysis.environmentanalyzer.object_identifier import ObjectsIdentifier
from vannypi.inputanalysis.objects.toddler import Toddler
from vannypi.inputmanagement.audiomanager.audio_recorder import start_process
from vannypi.inputmanagement.videomanager.video_encoder import encode


class Camera:
    def __init__(self):
        self._toddler = Toddler()
        self._object_identifier = ObjectsIdentifier()
        print(self._toddler.report_status())

    def run_camera(self, detector, height, width, camera_id):
        # Start capturing video input from the camera

        cap = cv2.VideoCapture('window_slow.mp4') #(camera_id)
        #cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        # Visualization parameters
        row_size = 20  # pixels
        left_margin = 24  # pixels
        text_color = (0, 0, 255)  # red
        font_size = 1
        font_thickness = 1
        fps_avg_frame_count = 10
        # Variables to calculate FPS
        counter, fps = 0, fps_avg_frame_count
        frames: List[np.ndarray] = []

        max_length_of_record_seconds: List[int] = [10, 10]
        videos_count: int = 0
        capture_starting_time = time.time()
        start_time = time.time()
        mode: int = 0
        capture_length = max_length_of_record_seconds[mode]
        # mocking danger detectionn with water bottles :)
        bottle_detected: bool = False

        fourcc = cv2.VideoWriter_fourcc(*'MJPG')

        # Continuously capture images from the camera and run inference
        ctx = get_context('spawn')
        audio_recorder_queue: Queue = ctx.Queue()
        start_process(main_seconds=max_length_of_record_seconds[0],
                      post_incidentt_seconds=max_length_of_record_seconds[1],
                      rate=48000, chunk_length=4096, mq=audio_recorder_queue)

        frames_count = 0
        actual_seconds_pre = 0

        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("writing post")
                for i in range(len(frames)):
                    video_writer.write(frames[i])

                print(frames_count, "fps")
                print(actual_seconds_pre + max_length_of_record_seconds[1], "time")
                audio_recorder_queue.put('done')
                encode(videos_count, frames_count, actual_seconds_pre + max_length_of_record_seconds[1])
                videos_count += 1
                print('End of stream.')
                return

            frames_count += 1
            counter += 1
            #image = cv2.flip(image, 1)  # .astype('uint8')
            # keep the size of video as intended
            if len(frames) >= max_length_of_record_seconds[mode] * fps:
                frames = frames[1:]

            frames.append(image)

            # Convert the image from BGR to RGB as required by the TFLite model.
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Create a TensorImage object from the RGB image.
            input_tensor = vision.TensorImage.create_from_array(rgb_image)

            # Run object detection estimation using the model.
            detection_result = detector.detect(input_tensor)

            # Draw keypoints and edges on input image
            image, detected_objects = self._object_identifier.visualize(image, detection_result)
            self._toddler.update(detected=('baby' in detected_objects))
            print(self._toddler.report_status())

            cur_time = time.time()
            if (cur_time - capture_starting_time > 5) and mode == 0:
                # if detected:
                print("\ndetected")
                bottle_detected = True
                audio_recorder_queue.put(True)

            # Calculate the FPS
            if counter % fps_avg_frame_count == 0:
                end_time = time.time()
                fps = fps_avg_frame_count / (end_time - start_time)
                start_time = time.time()

            # Show the FPS
            fps_text = 'FPS = {:.1f}'.format(fps)
            text_location = (left_margin, row_size)
            cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                        font_size, text_color, font_thickness)

            # Stop the program if the ESC key is pressed.
            if cv2.waitKey(1) == 27:
                break
            cv2.imshow('object_detector', image)

            cur_time = time.time()
            print(cur_time - capture_starting_time)

            if mode == 0:
                if bottle_detected:
                    os.system('clear')
                    print("writing")
                    cur_time = time.time()
                    actual_seconds_pre = int(cur_time - capture_starting_time)
                    video_writer = cv2.VideoWriter('video_capture_{}.avi'.format(videos_count), fourcc, fps,
                                                   (int(cap.get(3)), int(cap.get(4))))

                    for i in range(len(frames)):
                        video_writer.write(frames[i])

                    frames: List[np.ndarray] = []
                    mode = 1
                    bottle_detected = False
                    capture_starting_time = time.time()

            elif mode == 1:
                if len(frames) >= fps * max_length_of_record_seconds[mode]:
                    print("writing post")
                    for i in range(len(frames)):
                        video_writer.write(frames[i])

                    frames: List[np.ndarray] = []
                    mode = 0
                    bottle_detected = False
                    capture_starting_time = time.time()

                    print(frames_count, "fps")
                    print(actual_seconds_pre + max_length_of_record_seconds[1], "time")
                    encode_process = ctx.Process(target=encode, args=(
                        videos_count, frames_count, actual_seconds_pre + max_length_of_record_seconds[1],))
                    encode_process.start()
                    videos_count += 1
                    frames_count = 0
                    actual_seconds_pre = 0

        cap.release()
        cv2.destroyAllWindows()




'''
pi code for camera
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 24
time.sleep(2)

while True:
    image = np.empty((240 * 320 * 3,), dtype=np.uint8)
    camera.capture(image, 'bgr')
    image = image.reshape((240, 320, 3))
'''
