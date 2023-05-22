from typing import List

from vannypi.inputanalysis.environmentanalyzer.object_identifier import ObjectsIdentifier
from vannypi.inputanalysis.objects.sharp_object import SharpObjects
from vannypi.inputmanagement.cameramanager.camera import Camera

from vannypi.inputmanagement.videomanager.video import Video


class Watcher:
    def __int__(self):
        self._sharp_objects = SharpObjects()


    def watch(self) -> None:  # everything happens here
        pass

    def is_up(self) -> bool:
        pass

    def identify_objects(self) -> None:
        pass

    def analyze(self, video: Video) -> None:
        pass

    def run(self, model: str, camera_id: int, width: int, height: int, num_threads: int,
            enable_edgetpu: bool) -> None:
        """Continuously run inference on images acquired from the camera.

        Args:
          model: Name of the TFLite object detection model.
          camera_id: The camera id to be passed to OpenCV.
          width: The width of the frame captured from the camera.
          height: The height of the frame captured from the camera.
          num_threads: The number of CPU threads to run the model.
          enable_edgetpu: True/False whether the model is a EdgeTPU model.
        """
