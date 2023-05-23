from typing import Dict, List


class SharpObjects:
    def __init__(self):
        self._detected: Dict[str, int] = {'scissor': 0, 'knife': 0, 'pen': 0}
        self.in_room: List[str] = []
        self._THRESHOLD: int = 4

    def update(self, names: List[str]):
        for object_name in self._detected.keys():
            if object_name in names:
                if self._detected[object_name] < self._THRESHOLD:
                    self._detected[object_name] += 1

                if self._detected[object_name] == self._THRESHOLD and object_name not in self.in_room:
                    self.in_room.append(object_name)

            elif object_name not in names:
                self._detected[object_name] -= 1

                if self._detected[object_name] == 0:
                    self.in_room.remove(object_name)
