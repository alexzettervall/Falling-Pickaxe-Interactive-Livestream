from pygame import Vector2
import pymunk
from component import Component
from typing import override
from entity import Entity
import physics

class RigidBody(Component):
    def __init__(self, entity: Entity) -> None:
        super().__init__(entity)

        self.body = pymunk.Body()
        self.body.position = (self.entity.location.position.x, self.entity.location.position.y)
        self.poly = pymunk.Poly.create_box(self.body, (self.entity.size.x, self.entity.size.y))
        self.poly.mass = 1
        physics.physicsManager.add_body(self.body)
        

    @override
    def tick(self):
        self.entity.location.set_position(self.body.position.x, self.body.position.y)
        self.entity.location.rotation = self.body.angle * 57.2957795
        return super().tick()
    
    @override
    def on_remove(self):
        physics.physicsManager.remove_body(self.body)
        return super().on_remove()
    
    
