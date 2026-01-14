from typing import override
from component import Component
from components import rigidbody
from components.health import Health
from components.rigidbody import RigidBody
from entities.block import Block


class BlockBreaker(Component):
    @override
    def __init__(self, entity, damage: float) -> None:
        super().__init__(entity)
        self.damage = damage
        self.rigidbody = self.entity.get_component(RigidBody)
        if self.rigidbody != None:
            self.rigidbody.add_on_collision_listener(self.on_collision)

    def on_collision(self, rigidbody: RigidBody):
        if isinstance(rigidbody.entity, Block):
            self.on_block_collision(rigidbody.entity)

    def on_block_collision(self, block: Block):
        block_health = block.get_component(Health)
        if block_health == None:
            return
        block_health.damage(self.damage)
        self.entity.location.world.sound_manager.play_sound("stone")