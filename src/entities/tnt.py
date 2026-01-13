from typing import override
from pygame import Vector2
from components.rigidbody import RigidBody
from components.sprite_renderer import SpriteRenderer
from entities.entity import Entity
from location import Location
from particles.particles import ParticleType
import variables
from variables import PHYSICS_SCALE

class TNT(Entity):
    def __init__(self, location) -> None:
        super().__init__(location, size = Vector2(1, 1))

        sprite = variables.sprite_tnt
        
        vertices = [
            (-0.5, 0.5),
            (0.5, 0.5),
            (0.5, -0.5),
            (-0.5, -0.5)
        ]

        self.add_component(RigidBody(self, [vertices]))
        self.add_component(SpriteRenderer(self, variables.camera, sprite))

        self.fuse: float = 3

    @override
    def tick(self):
        self.fuse -= variables.DELTA_TIME
        if self.fuse <= 0:
            self.explode()
        return super().tick()
    
    def explode(self):
        self.location.world.particle_manager.emit(ParticleType.EXPLOSION, self.location, 20)
        self.location.world.create_explosion(self.location, 4, 100)
        self.remove()
    
