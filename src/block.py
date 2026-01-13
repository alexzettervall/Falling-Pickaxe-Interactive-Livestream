from numpy import var
import pymunk
from math import floor
from location import Location
import physics
from variables import PHYSICS_SCALE
from collision_type import CollisionType
import variables


class Block:
    def __init__(self, chunk, material, location):
        self.dead = False
        self.chunk = chunk
        self.material = material
        self.location: Location = location
        self.max_health: float = variables.get_material_health(self.material)
        self.health: float = self.max_health
        self.destroy_state_index = 0

        self.body = pymunk.Body(body_type = pymunk.Body.STATIC)
        self.body.position = (self.location.position.x * PHYSICS_SCALE, self.location.position.y * PHYSICS_SCALE)
        poly = pymunk.Poly.create_box(self.body, (1 * PHYSICS_SCALE, 1 * PHYSICS_SCALE))
        poly.collision_type = CollisionType.BLOCK.value[0]
        poly.mass = 1
        physics.physicsManager.add_body(self.body, self)

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
        physics.physicsManager.remove_body(self.body)
        self.chunk.remove_block(self)