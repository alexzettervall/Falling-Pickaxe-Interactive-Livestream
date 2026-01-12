import pymunk

from location import Location
import physics


class Block:
    def __init__(self, chunk, material, location):
        self.dead = False
        self.chunk = chunk
        self.material = material
        self.location: Location = location
        self.health: float = 3.0

        self.body = pymunk.Body(body_type = pymunk.Body.STATIC)
        self.body.position = (self.location.position.x, self.location.position.y)
        poly = pymunk.Poly.create_box(self.body, (1, 1))
        poly.mass = 1
        physics.physicsManager.add_body(self.body)

    def damage(self, damage: float):
        self.health -= damage
        if self.health <= 0:
            self.destroy()

    def destroy(self):
        if self.dead:
            return
        self.dead = True
        physics.physicsManager.remove_body(self.body)
        self.chunk.remove_block(self)