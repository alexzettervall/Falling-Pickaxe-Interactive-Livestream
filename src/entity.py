from location import Location
from size import Size

class Entity():
    def __init__(self, location) -> None:
        self.location = location
        self.size = Size(1, 1)
        self.velocity = 0

    def tick(self):
        pass