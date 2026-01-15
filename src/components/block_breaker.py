from typing import override
from component import Component
from components import rigidbody
from components.health import Health
from components.rigidbody import RigidBody
from entities.block import Block
from game_data import config


class BlockBreaker(Component):
    @override
    def __init__(self, entity, damage: float, self_damage: float = 0.0) -> None:
        super().__init__(entity)
        self.damage = damage
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
        self.block_damage_timers[block] = config.pickaxe_break_delay

    @override
    def tick(self):
        for block in self.block_damage_timers.keys():
            self.block_damage_timers[block] -= config.delta_time

        return super().tick()

    