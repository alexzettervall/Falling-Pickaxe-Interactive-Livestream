import math
from pygame import Vector2
import pymunk
from component import Component
from typing import override
from entity import Entity
import physics
from variables import PHYSICS_SCALE
from collision_type import CollisionType
from pymunk import Shape

class RigidBody(Component):
    def __init__(self, entity: Entity, shapes: list[Shape]) -> None:
        super().__init__(entity)

        self.body = pymunk.Body()
        self.body.position = (self.entity.location.position.x * PHYSICS_SCALE, self.entity.location.position.y * PHYSICS_SCALE)
        for shape in shapes:
            shape.body = self.body
            shape.mass = 1
            shape.collision_type = CollisionType.ENTITY.value[0]
        physics.physicsManager.add_body(self.body, self.entity)
        

    @override
    def tick(self):
        self.entity.location.set_position(self.body.position.x / PHYSICS_SCALE, self.body.position.y / PHYSICS_SCALE)
        self.entity.location.rotation = math.degrees(self.body.angle)
        
        return super().tick()
    
    @override
    def on_remove(self):
        physics.physicsManager.remove_body(self.body)
        return super().on_remove()
    
    
