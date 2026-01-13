from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from world import World
from pygame import Vector2

class Location():
    def __init__(self, world: World, position: Vector2, rotation: float = 0.0) -> None:
        self.world: World = world
        self.position: Vector2 = position
        self.rotation: float = rotation

    def move(self, x: float, y: float):
        self.position.x += x
        self.position.y += y

    def set_position(self, x: float, y: float):
        self.position.x = x
        self.position.y = y

    def clone(self):
        return Location(self.world, Vector2(self.position.x, self.position.y), self.rotation)