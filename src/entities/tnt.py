from __future__ import annotations
import math
from typing import TYPE_CHECKING, override
from pygame import Vector2
import pygame
from components.health import Health
from components.text_renderer import TextRenderer
from components.rigidbody import RigidBody
from components.sprite_renderer import SpriteRenderer
from entities.block import Block, BlockBreaker
from entities.damageable_block import DamageableBlock
from entities.entity import Entity
from location import Location
import material
from particles.particles import ParticleType
from text import AlignmentType
import game_data
import random

if TYPE_CHECKING:
    from chunk import Chunk

class TNT(DamageableBlock):
    def __init__(self, chunk: Chunk | None = None, location = None, user: str | None = None) -> None:
        material = "tnt"
        super().__init__(chunk = chunk, location = location, material = material)
        
        self.text_renderer = self.add_component(TextRenderer(self, Vector2(0, 0.5), alignment_type = AlignmentType.CENTER))
        if user != None:
            self.text_renderer.text = user

        self.fuse: float = game_data.config.tnt.fuse_time + random.uniform(-0.5, 0.5)
        self.ignited: bool = False

        self.explosion_radius = game_data.config.tnt.radius
        self.explosion_damage = game_data.config.tnt.damage

    @override
    def on_damaged(self):
        self.ignite()

        return super().on_damaged()

    @override
    def tick(self):
        self._update_fuse()

        return super().tick()
    
    def _update_fuse(self):
        if not self.ignited:
            return
        
        self.flash_sprite_renderer.alpha = math.sin(2 * math.pi * (game_data.config.tnt.fuse_time - self.fuse) / game_data.config.tnt.flash_interval) / 2 + 0.5
        self.fuse -= game_data.config.delta_time
        if self.fuse <= 0:
            self.explode()

    def ignite(self):
        if self.ignited:
            return
        self.location.world.sound_manager.play_sound("fuse")
        self.ignited = True
        self.dislodge()

        self.sprite_renderer = self.add_component(SpriteRenderer(self, None, game_data.MATERIAL_DATA[self.material].sprite))

        if not self in self.location.world.entities:
            self.location.world.entities.append(self)
        if self.chunk != None:
            self.chunk.blocks.remove(self)
            self.chunk = None

        square = pygame.Surface((1, 1))
        square.fill("white")
        square = square.convert_alpha()
        self.flash_sprite_renderer = self.add_component(SpriteRenderer(self, None, square))

    @override
    def dislodge(self):
        super().dislodge()
        self.ignite()
        self.remove_component(BlockBreaker)
        self.remove_component(Health)
        
    
    def explode(self):
        self.location.world.create_explosion(self.location, self.explosion_radius, self.explosion_damage)
        self.remove()
    
