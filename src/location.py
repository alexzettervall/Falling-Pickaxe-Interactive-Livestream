from pygame import Vector2

class Location():
    def __init__(self, world, position, rotation = 0) -> None:
        self.world = world
        self.position: Vector2 = position
        self.rotation: float = rotation

    def move(self, x: float, y: float):
        self.position.x += x
        self.position.y += y

    def set_position(self, x: float, y: float):
        self.position.x = x
        self.position.y = y