from typing import Any
import pymunk
from pymunk import Arbiter, Body, Shape, Space

from block import Block
from entity import Entity
from variables import DELTA_TIME
from collision_type import CollisionType

class PhysicsManager():
    def __init__(self) -> None:
        self.bodies: dict[Body, object] = {}
        self.space = pymunk.Space()
        self.space.gravity = (0, -400)
        self.space.iterations = 30
        self.space.on_collision(CollisionType.ENTITY.value[0], CollisionType.BLOCK.value[0], self.entity_block_collision)

    def add_body(self, body: Body, object: object):
        self.bodies[body] = object
        self.space.add(body)
        for shape in body.shapes:
            shape.elasticity = 0.8
            shape.friction = 0.2
            self.space.add(shape)

    def remove_body(self, body: Body):
        self.bodies.pop(body)
        self.space.remove(body)
        for shape in body.shapes:
            self.space.remove(shape)

    def tick(self):
        self.space.step(DELTA_TIME)

    def entity_block_collision(self, arbiter: Arbiter, space: Space, any: Any):
        if len(arbiter.bodies) != 2:
            return
        object1 = self.bodies.get(arbiter.bodies[0])
        object2 = self.bodies.get(arbiter.bodies[1])
        entity = None
        block = None
        if isinstance(object1, Entity):
            entity = object1
            if isinstance(object2, Block):
                block = object2
        elif isinstance(object2, Entity):
            entity = object2
            if isinstance(object1, Block):
                block = object1
        if entity == None or block == None:
            return
        
        entity.on_block_collision(block)


physicsManager = PhysicsManager()

    


