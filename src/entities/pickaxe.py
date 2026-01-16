from typing import override
from pygame import Surface, Vector2, ver
from data import data_loader
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
       
        self.pickaxe_type: str
        self.pickaxe_data: data_loader.PickaxeData
        

        shapes: list[list[tuple[float, float]]] = [[(-4.0, -7.0), (-4.0, -5.0), (-6.0, -5.0), (-6.0, -7.0)], [(-3.0, -6.0), (-3.0, -4.0), (-5.0, -4.0), (-5.0, -6.0)], [(-2.0, -5.0), (-2.0, -3.0), (-4.0, -3.0), (-4.0, -5.0)], [(-1.0, -4.0), (-1.0, -2.0), (-3.0, -2.0), (-3.0, -4.0)], [(0.0, -3.0), (0.0, -1.0), (-2.0, -1.0), (-2.0, -3.0)], [(1.0, -2.0), (1.0, 0.0), (-1.0, 0.0), (-1.0, -2.0)], [(2.0, -1.0), (2.0, 1.0), (0.0, 1.0), (0.0, -1.0)], [(3.0, 0.0), (3.0, 2.0), (1.0, 2.0), (1.0, 0.0)], [(6.0, 1.0), (6.0, 5.0), (2.0, 5.0), (2.0, 1.0)], [(3.0, 3.0), (3.0, 6.0), (-2.0, 6.0), (-2.0, 3.0)], [(-2.0, 4.0), (-2.0, 5.0), (-3.0, 5.0), (-3.0, 4.0)], [(7.0, -3.0), (7.0, 2.0), (4.0, 2.0), (4.0, -3.0)], [(6.0, -4.0), (6.0, -3.0), (5.0, -3.0), (5.0, -4.0)]]

        for i in range(len(shapes)):
            shape = shapes[i]
            for j in range(len(shape)):
                point = shape[j]
                shape[j] = (point[0] / 16, -point[1] / 16)

        self._pickaxe_size = PickaxeSize.NORMAL
        self.rigidbody = self.add_component(RigidBody(self, shapes))
        self.sprite_renderer = self.add_component(SpriteRenderer(self))
        self.block_breaker = self.add_component(BlockBreaker(self))

        self.set_pickaxe_type("diamond")

    @override
    def tick(self):
        self.keep_within_bounds()

        return super().tick()
    
    def set_pickaxe_type(self, pickaxe_type: str):
        self.pickaxe_type = pickaxe_type
        self.pickaxe_data = game_data.PICKAXE_DATA[pickaxe_type]
        self.sprite_renderer.sprite = self.pickaxe_data.sprite
        self.block_breaker.damage = self.pickaxe_data.damage
        self.block_breaker.dig_speed = self.pickaxe_data.dig_speed

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