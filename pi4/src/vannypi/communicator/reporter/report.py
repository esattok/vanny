from vannypi.inputmanagement.audiomanager.audio import Audio
from vannypi.inputmanagement.videomanager.video import Video


class Report:
    def __int__(self):
        self._videos: list[Video] = []
        self._audios: list[Audio] = []
        self._details: str = ""
        self._title: str = ""
