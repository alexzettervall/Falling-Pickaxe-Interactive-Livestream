class Location():
    def __init__(self, world, position) -> None:
        self.position = position
        self.world = world

    def move(self, x: float, y: float):
        self.position.move(x, y)