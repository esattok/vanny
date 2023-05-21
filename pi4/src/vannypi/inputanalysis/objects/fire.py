from typing import List


class Fire:
    def __init__(self):
        self.detected: bool = False
        self._count: int = 0
        self._THRESHOLD: int = 6

    def update(self, names: List[str]):
        if 'fire' in names:
            if self._count < self._THRESHOLD:
                self._count += 1

            if self._count == self._THRESHOLD and not self.detected:
                self.detected = True

        else:
            self._count -= 1

            if self._count == 0:
                self.detected = False
