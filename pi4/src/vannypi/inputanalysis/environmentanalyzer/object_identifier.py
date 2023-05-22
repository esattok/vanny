from typing import List, Tuple

import cv2
import numpy as np
from numpy import ndarray

from vannypi.inputanalysis.objects.door import Door
from vannypi.inputanalysis.objects.fire import Fire
from vannypi.inputanalysis.objects.sharp_object import SharpObjects
from vannypi.inputanalysis.objects.toddler import Toddler
from vannypi.inputanalysis.objects.window import Window
from vannypi.inputmanagement.videomanager.video import Video

from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision


class ObjectsIdentifier:
    def __init__(self):
        self._toddler = Toddler()
        self._sharp_objects = SharpObjects()
        self._fire = Fire()
        self._door = Door()
        self._window = Window()

        return

    @staticmethod
    def digest_models(model, num_threads, enable_edgetpu) -> core.BaseOptions:
        # Initialize the object detection model
        base_options: core.BaseOptions = core.BaseOptions(
            file_name=model, use_coral=enable_edgetpu, num_threads=num_threads)
        return base_options

    def detect_and_identify(self, video: Video) -> None:
        pass

    @staticmethod
    def setup_detector(base_options: core.BaseOptions) -> vision.ObjectDetector:
        detection_options: processor.DetectionOptions = processor.DetectionOptions(
            max_results=3, score_threshold=0.65)
        options: vision.ObjectDetectorOptions = vision.ObjectDetectorOptions(
            base_options=base_options, detection_options=detection_options)
        detector: vision.ObjectDetector = vision.ObjectDetector.create_from_options(options)
        return detector

    def update_detections(self, detections: List[str]):
        self._sharp_objects.update(detections)
        self._fire.update(detections)
        self._window.update(detections)
        self._door.update(detections)
        self._toddler.update(detected=('baby' in detections))
        print(self._toddler.report_status())

        print("sharp objs", self._sharp_objects.in_room)
        print("fire", self._fire.detected)
        print("door", self._door.detected)
        print("window", self._window.detected)

    def detected_text(self):
        sharp_objects = "" if len(self._sharp_objects.in_room) == 0 else "- Sharp objects detected: " + str(
            self._sharp_objects.in_room) + " "

        fire_text = "" if not self._fire.detected else " - FIRE!!"
        door_text = "" if not self._door.detected else " - close to door "
        window_text = "" if not self._window.detected else " - close to window "

        detections = "Toddler: {}{}{}{}{}".format(
            self._toddler.report_status(), fire_text, sharp_objects, door_text, window_text)
        return detections

    def visualize(self, image: np.ndarray, detection_result: processor.DetectionResult) -> ndarray:
        """Draws bounding boxes on the input image and return it.

        Args:
          image: The input RGB image.
          detection_result: The list of all "Detection" entities to be visualize.

        Returns:
          Image with bounding boxes.
        """
        _MARGIN = 10  # pixels
        _ROW_SIZE = 10  # pixels
        _FONT_SIZE = 1
        _FONT_THICKNESS = 1
        _TEXT_COLOR = (0, 0, 255)  # red

        # mocking danger detectionn with water bottles :)

        detected_objects: List[str] = []
        for detection in detection_result.detections:
            # Draw bounding_box
            bbox = detection.bounding_box
            start_point = bbox.origin_x, bbox.origin_y
            end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
            cv2.rectangle(image, start_point, end_point, _TEXT_COLOR, 3)

            # Draw label and score
            category = detection.categories[0]
            category_name = category.category_name

            detected_objects.append(category_name)

            probability = round(category.score, 2)
            result_text = category_name + ' (' + str(probability) + ')'
            text_location = (_MARGIN + bbox.origin_x,
                             _MARGIN + _ROW_SIZE + bbox.origin_y)
            cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                        _FONT_SIZE, _TEXT_COLOR, _FONT_THICKNESS)

        self.update_detections(detected_objects)

        row_size = 20  # pixels
        left_margin = 24  # pixels
        top_margin = 45
        bottomLeftCornerOfText = (10, 500)

        text_location = (left_margin, top_margin)
        cv2.putText(image, self.detected_text(), text_location, cv2.FONT_HERSHEY_COMPLEX_SMALL,
                    _FONT_SIZE, (0, 0, 0), _FONT_THICKNESS + 1)
        return image
