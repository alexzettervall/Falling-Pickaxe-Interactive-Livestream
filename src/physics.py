from __future__ import annotations
from enum import Enum
import math
from typing import Any, TYPE_CHECKING
from bidict import bidict
from pygame import Vector2
import pymunk
from pymunk import Arbiter, Body, PointQueryInfo, Poly, ShapeFilter, Space, Transform, Vec2d
import pymunk.pygame_util
from entities.entity import Entity
from game_data import config
import game_data

if TYPE_CHECKING:
    from components.rigidbody import RigidBody
    from world import World

class CollisionType(Enum):
    BLOCK = 1,
    ENTITY = 2,

class BodyType(Enum):
    STATIC = 1,
    DYNAMIC = 2,

class PhysicsManager():
    def __init__(self, world: World) -> None:
        self.world: World = world
        self.body_rigidbodies: bidict[Body, RigidBody] = bidict()
        self.space = pymunk.Space()
        self.space.gravity = (0, -600)
        self.space.iterations = 10
        self.space.on_collision(None, None, self.on_collision_begin, None, None, self.on_collision_end)
        self.rigidbodies_to_remove: set[RigidBody] = set()

    def add_rigidbody(self, rigidbody: RigidBody, shapes: list[list[tuple[float, float]]], collision_type: CollisionType, body_type: BodyType):
        # Set up body
        body = pymunk.Body()
        self._set_body_type(body, body_type)

        entity = rigidbody.entity
        body.position = (entity.location.position.x * config.physics_scale, entity.location.position.y * config.physics_scale)
        for shape in shapes:
            pymunk_shape = Poly(body, shape)
            pymunk_shape.density = 1
            pymunk_shape.collision_type = collision_type.value[0]

        # Add to simulation
        self.body_rigidbodies.put(body, rigidbody)
        self.space.add(body)
        for shape in body.shapes:
            shape.elasticity = 0.85
            shape.friction = 0.95
            self.space.add(shape)

    def _set_body_type(self, body: Body, body_type: BodyType):
        if body_type == BodyType.STATIC:
            body.body_type = pymunk.Body.STATIC
        elif body_type == BodyType.DYNAMIC:
            body.body_type = pymunk.Body.DYNAMIC

    def remove_rigidbody(self, rigidbody: RigidBody):
        self.rigidbodies_to_remove.add(rigidbody)

    def tick(self):
        self.space.step(config.delta_time)
        self.remove_rigidbodies()
        self.update_rigidbody_positions()

    def debug(self):
        if config.debug:
            offset: Vector2 = game_data.camera.location.position
            draw_options = pymunk.pygame_util.DrawOptions(game_data.camera.surface)
            draw_options.transform = pymunk.Transform(
                a=1, b=0, c=0, d=-1, tx=config.screen_width / 2, ty=config.screen_height / 2
            ).translated(offset.x * config.physics_scale, -offset.y * config.physics_scale)

            self.space.debug_draw(draw_options)


    def update_rigidbody_positions(self):
        for body in self.body_rigidbodies.keys():
            rigidbody = self.body_rigidbodies[body]
            rigidbody.on_position_update(Vector2(body.position.x / config.physics_scale, body.position.y / config.physics_scale))
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
        body.position = Vec2d(position.x * config.physics_scale, position.y * config.physics_scale)

    def rotate_rigidbody_degrees(self, rigidbody: RigidBody, angle: float):
        body = self.body_rigidbodies.inverse.get(rigidbody)
        if body == None:
            return
        body.angle = math.radians(angle)

    def point_query(self, point: tuple[float, float], max_distance: float) -> list[Entity]:
        queries: list[PointQueryInfo] = self.space.point_query((point[0] * config.physics_scale, point[1] * config.physics_scale), max_distance * config.physics_scale, ShapeFilter())
        entities: list[Entity] = []
        for query in queries:
            if query.shape.body == None:
                continue
            entities.append(self.body_rigidbodies[query.shape.body].entity)
        return entities
    
    def set_rigidbody_body_type(self, rigidbody: RigidBody, body_type: BodyType):
        body = self.body_rigidbodies.inverse.get(rigidbody)
        if body == None:
            return
        self._set_body_type(body, body_type)

    def set_rigidbody_velocity(self, rigidbody: RigidBody, velocity: Vector2):
        body = self.body_rigidbodies.inverse.get(rigidbody)
        if body == None:
            return
        body.velocity = (velocity.x * config.physics_scale, velocity.y * config.physics_scale)

    """
    Set the size of the pymunk body associated with the rigidbody.
    Works but multiplying each vertex by a muliplier determined from the previous size.
    Currently only works with shapes that are instances of Poly.
    """
    def set_rigidbody_size(self, rigidbody: RigidBody, prev_size: Vector2, size: Vector2):
        multiplier: Vector2 = Vector2(size.x / prev_size.x, size.y / prev_size.y)
        body = self.body_rigidbodies.inverse.get(rigidbody)
        if body == None:
            return
        for shape in body.shapes:
            if not isinstance(shape, Poly):
                raise ValueError("set_rigidbody_size currently only works with shapes of type Poly")
        for shape in body.shapes:
            original_vertices = shape.get_vertices()
            new_vertices = [(x * multiplier.x, y * multiplier.y) for x, y in original_vertices]
            shape.unsafe_set_vertices(new_vertices)
            
