from __future__ import annotations
import random
from typing import TYPE_CHECKING, override
from numpy import var
from math import floor

from pygame import Vector2
from component import Component
from components.health import Health
from components.rigidbody import RigidBody
from entities.entity import Entity
from physics import BodyType, CollisionType
from game_data import config
import game_data
import physics

if TYPE_CHECKING:
    from chunk import Chunk

class Block(Entity):
    def __init__(self, chunk: Chunk | None, material: str, location):
        super().__init__(location, size = game_data.config.block_size)
        self.dead = False
        self.dislodged = False
        self.chunk = chunk
        self.material: str = material

        vertices = [
            (-0.5, 0.5),
            (0.5, 0.5),
            (0.5, -0.5),
            (-0.5, -0.5)
        ]
        self.rigidbody = self.add_component(RigidBody(self, [vertices], collision_type = CollisionType.BLOCK, body_type = BodyType.STATIC))

    def dislodge(self):
        if self.dislodged:
            return
        self.dislodged = True
        self.rigidbody.set_body_type(physics.BodyType.DYNAMIC)
        self.rigidbody.set_velocity(Vector2(random.uniform(-5, 5), random.uniform(0, 5)))
        self.add_component(BlockBreaker(self, 1, self_damage = 1))

    @override
    def remove(self):
        sound = game_data.MATERIAL_DATA[self.material].break_sound
        if sound != None:
            self.location.world.sound_manager.play_sound(sound)

        return super().remove()

class BlockBreaker(Component):
    @override
    def __init__(self, entity, damage: float = 0, dig_speed = game_data.config.default_break_speed, self_damage: float = 0.0) -> None:
        super().__init__(entity)
        self.damage = damage
        self.dig_speed = dig_speed
        self.self_damage = self_damage
        self.rigidbody = self.entity.get_component(RigidBody)
        if self.rigidbody != None:
            self.rigidbody.add_while_in_contact_listener(self.while_in_contact)
        self.block_damage_timers: dict[Block, float] = {}

    def while_in_contact(self, rigidbody: RigidBody):
        if isinstance(rigidbody.entity, Block):
            block = rigidbody.entity
            timer = 0
            if block in self.block_damage_timers.keys():
                timer = self.block_damage_timers[block]
            if timer > 0:
                return
            self.damage_block(block)

    def damage_block(self, block: Block):

        block_health = block.get_component(Health)
        if block_health == None:
            return

        block_health.damage(self.damage)
        health = self.entity.get_component(Health)
        if health != None:
            health.damage(self.self_damage)
        self.entity.location.world.sound_manager.play_sound("stone")
        self.block_damage_timers[block] = 1 / self.dig_speed

    @override
    def tick(self):
        for block in self.block_damage_timers.keys():
            self.block_damage_timers[block] -= config.delta_time

        return super().tick()
