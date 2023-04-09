from vannypi.inputanalysis.objects.object import Object


class DangerDetector:
    def __int__(self):
        self.dangerous_object: list[Object] = []
        self.current_status: int = 0

    def determine_danger(self, objects: list[Object]) -> list[list]:
        pass
