from typing import override
from numpy import var
from math import floor
from components.rigidbody import RigidBody
from entities.entity import Entity
from physics import BodyType, CollisionType
from game_data import config
import game_data


class Block(Entity):
    def __init__(self, chunk, material: str, location):
        super().__init__(location, size = game_data.config.block_size)
        self.dead = False
        self.chunk = chunk
        self.material: str = material

        vertices = [
            (-0.5, 0.5),
            (0.5, 0.5),
            (0.5, -0.5),
            (-0.5, -0.5)
        ]
        self.rigidbody = self.add_component(RigidBody(self, [vertices], collision_type = CollisionType.BLOCK, body_type = BodyType.STATIC))

    """@override
    def damage(self, damage: float):
        self.health -= damage
        n = len(variables.destroy_stage_sprites)
        self.destroy_state_index = min(floor(n * ((self.max_health - self.health) / self.max_health)), n)
        if self.health <= 0:
            self.destroy()

    def destroy(self):
        if self.dead:
            return
        self.dead = True
        physics.physicsManager.remove_entity(self.body)
        self.chunk.remove_block(self)"""