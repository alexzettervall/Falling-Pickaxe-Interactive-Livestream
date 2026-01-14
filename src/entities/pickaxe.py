from typing import override
from pygame import Vector2, ver
from components.block_breaker import BlockBreaker
from entities.block import Block
from components.rigidbody import RigidBody
from components.sprite_renderer import SpriteRenderer
from entities.entity import Entity
from particles.particles import ParticleManager, ParticleType
from game_data import PHYSICS_SCALE
import game_data

class Pickaxe(Entity):
    def __init__(self, location) -> None:
        super().__init__(location, Vector2(2, 2))

        sprite = game_data.sprite_wooden_pickaxe
        vertices: list[tuple[float, float]] = [
            (-0.375, 0.375),
            (0.0, -0.125),
            (-0.0625, -0.0625),
            (-0.125, 0.0),
            (-0.1875, 0.0625),
            (-0.25, 0.125),
            (-0.3125, 0.1875),
            (-0.375, 0.25),
            (-0.3125, 0.1875),
            (-0.25, 0.125),
            (-0.1875, 0.0625),
            (-0.125, 0.0),
            (-0.0625, -0.0625),
            (-0.0625, -0.4375),
            (-0.125, -0.375),
            (-0.1875, -0.375),
            (-0.1875, -0.3125),
            (-0.1875, -0.25),
            (-0.125, -0.25),
            (-0.0625, -0.25),
            (0.0, -0.25),
            (0.0625, -0.25),
            (0.0, -0.25),
            (-0.0625, -0.25),
            (-0.125, -0.25),
            (-0.1875, -0.3125),
            (-0.125, -0.375),
            (-0.0625, -0.4375),
            (0.0, -0.4375),
            (0.0625, -0.4375),
            (0.125, -0.375),
            (0.1875, -0.375),
            (0.25, -0.375),
            (0.3125, -0.3125),
            (0.3125, -0.25),
            (0.375, -0.1875),
            (0.375, -0.125),
            (0.375, -0.0625),
            (0.375, 0.0),
            (0.375, 0.0625),
            (0.375, 0.125),
            (0.3125, 0.1875),
            (0.25, 0.125),
            (0.1875, 0.0625),
            (0.125, 0.0),
            (0.1875, -0.0625),
            (0.125, 0.0),
            (0.0625, 0.0625),
            (0.0, 0.125),
            (-0.0625, 0.1875),
            (-0.125, 0.25),
            (-0.1875, 0.3125),
            (-0.25, 0.375),
            (-0.1875, 0.3125),
            (-0.125, 0.25),
            (-0.0625, 0.1875),
            (0.0, 0.125),
            (0.0625, 0.0625),
            (0.125, 0.0),
            (0.1875, 0.0625),
            (0.25, 0.125),
            (0.25, 0.1875),
            (0.3125, 0.1875),
            (0.375, 0.1875),
            (0.375, 0.125),
            (0.375, 0.0625),
            (0.375, 0.0),
            (0.375, -0.0625),
            (0.375, -0.125),
            (0.375, -0.1875),
            (0.3125, -0.25),
            (0.3125, -0.3125),
            (0.25, -0.375),
            (0.1875, -0.375),
            (0.125, -0.375),
            (0.0625, -0.4375),
            (0.0, -0.4375),
            ]

        self.add_component(RigidBody(self, [vertices]))
        self.add_component(SpriteRenderer(self, None, sprite))
        self.add_component(BlockBreaker(self, 10))