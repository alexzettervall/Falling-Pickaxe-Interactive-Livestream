from typing import override
from pygame import Vector2, ver
import pymunk.util
from block import Block
from components.rigidbody import RigidBody
from components.sprite_renderer import SpriteRenderer
from entity import Entity
from particles.particles import ParticleManager, ParticleType
from variables import PHYSICS_SCALE
import variables
import pymunk

class Pickaxe(Entity):
    def __init__(self, location) -> None:
        super().__init__(location, Vector2(2, 2))

        sprite = variables.sprite_wooden_pickaxe
        verticies: list[tuple[float, float]] = [
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
        
        for i in range(len(verticies)):
            vert = verticies[i]
            verticies[i] = ((vert[0]) * self.size.x * PHYSICS_SCALE, (-vert[1]) * self.size.y * PHYSICS_SCALE)

        shape = pymunk.Poly(None, verticies, radius=0.3)
        self.add_component(RigidBody(self, [shape]))
        self.add_component(SpriteRenderer(self, variables.camera, sprite))


    @override
    def tick(self):
        p: ParticleManager = self.location.world.particle_manager
        p.emit(ParticleType.EXPLOSION, self.location.clone(), 0)
        return super().tick()
    
    @override
    def on_block_collision(self, block: Block):
        block.damage(10)
        return super().on_block_collision(block)
    
