import math
from typing import override
from pygame import Vector2
import pygame
from components.rigidbody import RigidBody
from components.sprite_renderer import SpriteRenderer
from entities.entity import Entity
from location import Location
from particles.particles import ParticleType
import variables

class TNT(Entity):
    def __init__(self, location) -> None:
        super().__init__(location, size = Vector2(1, 1))

        sprite = variables.sprite_tnt
        square = pygame.Surface((1, 1))
        square.fill("white")
        square = square.convert_alpha()
        
        vertices = [
            (-0.5, 0.5),
            (0.5, 0.5),
            (0.5, -0.5),
            (-0.5, -0.5)
        ]

        self.add_component(RigidBody(self, [vertices]))
        self.sprite_renderer = self.add_component(SpriteRenderer(self, variables.camera, sprite))
        self.flash_sprite_renderer = self.add_component(SpriteRenderer(self, variables.camera, square))

        self.fuse: float = variables.TNT_FUSE_TIME

    @override
    def tick(self):
        self.flash_sprite_renderer.alpha = math.sin(2 * math.pi * (variables.TNT_FUSE_TIME - self.fuse) / variables.TNT_FLASH_INTERVAL) / 2 + 0.5
        self.fuse -= variables.DELTA_TIME
        if self.fuse <= 0:
            self.explode()
        return super().tick()
    
    def explode(self):
        self.location.world.particle_manager.emit(ParticleType.EXPLOSION, self.location, 20)
        self.location.world.create_explosion(self.location, 4, 100)
        self.remove()
    
