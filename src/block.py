import pymunk

import physics


class Block:
    def __init__(self, material, location):
        self.material = material
        self.location = location

        self.body = pymunk.Body(body_type = pymunk.Body.STATIC)
        self.body.position = (self.location.position.x, self.location.position.y)
        poly = pymunk.Poly.create_box(self.body, (1, 1))
        poly.mass = 1
        physics.physicsManager.add_body(self.body)