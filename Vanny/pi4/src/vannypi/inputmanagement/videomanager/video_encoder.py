class VideoEncoder:
    def __int__(self):
        self._frame: list[float] = []
        self._audio_frame: list[float] = []

    def _import_raw_data(self, raw_data: list[float]) -> None:
        pass

    def _set_frame_rate(self, rate: int) -> None:
        pass

    def _set_compression_ratio(self, ratio: float) -> None:
        pass

    def encode(self, data: list[float]) -> list[float]:
        pass
