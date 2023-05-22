class Toddler:

    def __init__(self):
        self._detected = False
        self._in_room = False
        self._count_of_detected = 0
        self._count_of_not_seen = 0
        self._THREASHOLD = 6

    def update(self, detected: bool):
        if detected and not self._in_room:
            if self._count_of_detected >= self._THREASHOLD:
                self._detected = True
                self._in_room = True
                self._count_of_not_seen = 0
                self._count_of_detecte = 0


            elif self._count_of_detected < self._THREASHOLD:
                self._count_of_detected += 1


        elif not detected and self._in_room:
            if self._count_of_not_seen >= self._THREASHOLD:
                self._in_room = False


            elif self._count_of_not_seen < self._THREASHOLD:
                self._count_of_not_seen += 1

        return

    def report_status(self):
        if self._in_room:
            return "IN ROOM"
        elif not self._in_room:
            if not self._detected:
                return "NOT DETECTED"
            elif self._detected:
                return "NOT IN ROOM!"
