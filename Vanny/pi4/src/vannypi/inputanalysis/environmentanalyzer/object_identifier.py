from vannypi.inputanalysis.objects.object import Object
from vannypi.inputmanagement.videomanager.video import Video


class ObjectsIdentifier:
    def __int__(self):
        self._objects_to_look_for: list[Object] = []

    def digest_models(self, file_path: str) -> None:
        pass

    def detect_and_identify(self, video: Video) -> None:
        pass

        