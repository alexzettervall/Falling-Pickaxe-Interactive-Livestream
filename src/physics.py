from __future__ import annotations
from enum import Enum
import math
from typing import Any, TYPE_CHECKING
from bidict import bidict
from pygame import Vector2
import pymunk
from pymunk import Arbiter, Body, PointQueryInfo, Poly, ShapeFilter, Space, Vec2d
import pymunk.pygame_util
from entities.entity import Entity
from game_data import DELTA_TIME
from game_data import PHYSICS_SCALE
import game_data
if TYPE_CHECKING:
    from components.rigidbody import RigidBody

class CollisionType(Enum):
    BLOCK = 1,
    ENTITY = 2,

class BodyType(Enum):
    STATIC = 1,
    DYNAMIC = 2,

class PhysicsManager():
    def __init__(self) -> None:
        self.body_rigidbodies: bidict[Body, RigidBody] = bidict()
        self.space = pymunk.Space()
        self.space.gravity = (0, -400)
        self.space.iterations = 30
        self.space.on_collision(None, None, self.on_collision_begin, None, None, self.on_collision_end)
        self.rigidbodies_to_remove: set[RigidBody] = set()

    def add_rigidbody(self, rigidbody: RigidBody, shapes: list[list[tuple[float, float]]], collision_type: CollisionType, body_type: BodyType):
        # Set up body
        body = pymunk.Body()
        if body_type == BodyType.STATIC:
            body.body_type = pymunk.Body.STATIC
        elif body_type == BodyType.DYNAMIC:
            body.body_type = pymunk.Body.DYNAMIC

        entity = rigidbody.entity
        body.position = (entity.location.position.x * PHYSICS_SCALE, entity.location.position.y * PHYSICS_SCALE)
        for shape in shapes:
            pymunk_shape = Poly(body, shape)
            pymunk_shape.mass = 1
            pymunk_shape.collision_type = collision_type.value[0]

        # Add to simulation
        self.body_rigidbodies.put(body, rigidbody)
        self.space.add(body)
        for shape in body.shapes:
            shape.elasticity = 0.8
            shape.friction = 0.3
            self.space.add(shape)

    def remove_rigidbody(self, rigidbody: RigidBody):
        self.rigidbodies_to_remove.add(rigidbody)

    def tick(self):
        self.space.step(DELTA_TIME)
        self.remove_rigidbodies()
        self.update_rigidbody_positions()
        self.debug()

    def debug(self):
        if game_data.DEBUG:
            draw_options = pymunk.pygame_util.DrawOptions(game_data.camera.surface)
            draw_options.transform = pymunk.Transform(
                a=1, b=0, c=0, d=-1, tx=game_data.SCREEN_WIDTH / 2, ty=game_data.SCREEN_HEIGHT / 2
            )
            self.space.debug_draw(draw_options)


    def update_rigidbody_positions(self):
        for body in self.body_rigidbodies.keys():
            rigidbody = self.body_rigidbodies[body]
            rigidbody.update_position(Vector2(body.position.x / PHYSICS_SCALE, body.position.y / PHYSICS_SCALE))
            rigidbody.update_rotation_degrees(math.degrees(body.angle))

    def remove_rigidbodies(self):
        for rigidbody in self.rigidbodies_to_remove:
            body = self.body_rigidbodies.inverse.pop(rigidbody)
            for shape in body.shapes:
                self.space.remove(shape)
            self.space.remove(body)
        self.rigidbodies_to_remove.clear()
    
    def on_collision_begin(self, arbiter: Arbiter, space: Space, any: Any):        
        rigidbody1 = self.body_rigidbodies.get(arbiter.bodies[0])
        rigidbody2 = self.body_rigidbodies.get(arbiter.bodies[1])
        if rigidbody1 == None or rigidbody2 == None:
            return
        rigidbody1.on_collision_begin(rigidbody2)
        rigidbody2.on_collision_begin(rigidbody1)

    def on_collision_end(self, arbiter: Arbiter, space: Space, any: Any):
        rigidbody1 = self.body_rigidbodies.get(arbiter.bodies[0])
        rigidbody2 = self.body_rigidbodies.get(arbiter.bodies[1])
        if rigidbody1 == None or rigidbody2 == None:
            return
        rigidbody1.on_collision_end(rigidbody2)
        rigidbody2.on_collision_end(rigidbody1)

    def move_rigidbody_position(self, rigidbody: RigidBody, position: Vector2):
        body = self.body_rigidbodies.inverse.get(rigidbody)
        if body == None:
            return
        body.position = Vec2d(position.x, position.y)

    def rotate_rigidbody_degrees(self, rigidbody: RigidBody, angle: float):
        body = self.body_rigidbodies.inverse.get(rigidbody)
        if body == None:
            return
        body.angle = math.radians(angle)

    def point_query(self, point: tuple[float, float], max_distance: float) -> list[Entity]:
        queries: list[PointQueryInfo] = self.space.point_query((point[0] * PHYSICS_SCALE, point[1] * PHYSICS_SCALE), max_distance * PHYSICS_SCALE, ShapeFilter())
        entities: list[Entity] = []
        for query in queries:
            if query.shape.body == None:
                continue
            entities.append(self.body_rigidbodies[query.shape.body].entity)
        return entities

    


