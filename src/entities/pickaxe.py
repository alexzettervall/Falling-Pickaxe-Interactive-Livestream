from typing import override
from pygame import Vector2, ver
from entities.block import BlockBreaker
from components.rigidbody import RigidBody
from components.sprite_renderer import SpriteRenderer
from entities.entity import Entity
import game_data
from pickaxe_size import PickaxeSize

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

        self._pickaxe_size = PickaxeSize.NORMAL
        self.rigidbody = self.add_component(RigidBody(self, shapes))
        self.add_component(SpriteRenderer(self, None, sprite))
        self.add_component(BlockBreaker(self, 10))

    @override
    def tick(self):
        self.keep_within_bounds()

        return super().tick()
    
    def set_pickaxe_size(self, pickaxe_size: PickaxeSize):
        self._pickaxe_size = pickaxe_size
        size = game_data.config.normal_pickaxe_size
        if pickaxe_size == PickaxeSize.BIG:
            size = game_data.config.big_pickaxe_size
        elif pickaxe_size == PickaxeSize.SMALL:
            size = game_data.config.small_pickaxe_size
        self.rigidbody.set_size(Vector2(size, size))

    def get_pickaxe_size(self) -> PickaxeSize:
        return self._pickaxe_size
    
    def keep_within_bounds(self):
        chunk_width = game_data.config.chunk_size[0]
        x_pos = self.location.position.x
        if x_pos < -chunk_width / 2 or x_pos > chunk_width / 2:
            self.rigidbody.move_position(Vector2(0, self.location.position.y))
            self.rigidbody.set_velocity(Vector2(0, 0))