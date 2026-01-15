from typing import override
from pygame import Vector2, ver
from entities.block import BlockBreaker
from components.rigidbody import RigidBody
from components.sprite_renderer import SpriteRenderer
from entities.entity import Entity
import game_data

class Pickaxe(Entity):
    @override
    def __init__(self, location) -> None:
        super().__init__(location, Vector2(2, 2))

        sprite = game_data.sprite_wooden_pickaxe
        shapes: list[list[tuple[float, float]]] = [[(-4.0, -7.0), (-4.0, -5.0), (-6.0, -5.0), (-6.0, -7.0)], [(-3.0, -6.0), (-3.0, -4.0), (-5.0, -4.0), (-5.0, -6.0)], [(-2.0, -5.0), (-2.0, -3.0), (-4.0, -3.0), (-4.0, -5.0)], [(-1.0, -4.0), (-1.0, -2.0), (-3.0, -2.0), (-3.0, -4.0)], [(0.0, -3.0), (0.0, -1.0), (-2.0, -1.0), (-2.0, -3.0)], [(1.0, -2.0), (1.0, 0.0), (-1.0, 0.0), (-1.0, -2.0)], [(2.0, -1.0), (2.0, 1.0), (0.0, 1.0), (0.0, -1.0)], [(3.0, 0.0), (3.0, 2.0), (1.0, 2.0), (1.0, 0.0)], [(6.0, 1.0), (6.0, 5.0), (2.0, 5.0), (2.0, 1.0)], [(3.0, 3.0), (3.0, 6.0), (-2.0, 6.0), (-2.0, 3.0)], [(-2.0, 4.0), (-2.0, 5.0), (-3.0, 5.0), (-3.0, 4.0)], [(7.0, -3.0), (7.0, 2.0), (4.0, 2.0), (4.0, -3.0)], [(6.0, -4.0), (6.0, -3.0), (5.0, -3.0), (5.0, -4.0)]]

        for i in range(len(shapes)):
            shape = shapes[i]
            for j in range(len(shape)):
                point = shape[j]
                shape[j] = (point[0] / 16, -point[1] / 16)


        self.rigidbody = self.add_component(RigidBody(self, shapes))
        self.add_component(SpriteRenderer(self, None, sprite))
        self.add_component(BlockBreaker(self, 10))