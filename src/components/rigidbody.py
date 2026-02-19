from pygame import Vector2
from component import Component
from typing import Callable, override, TYPE_CHECKING
from entities.entity import Entity
from game_data import config
from physics import CollisionType, BodyType

class RigidBody(Component):
    def __init__(self, entity, shapes: list[list[tuple[float, float]]], collision_type: CollisionType = CollisionType.ENTITY, body_type: BodyType = BodyType.DYNAMIC) -> None:
        super().__init__(entity)

        for vertices in shapes:
            for i in range(len(vertices)):
                vertex = vertices[i]
                vertices[i] = ((vertex[0]) * self.entity.size.x * config.physics.scale, (-vertex[1]) * self.entity.size.y * config.physics.scale)

        self.entity.location.world.physics_manager.add_rigidbody(self, shapes, collision_type, body_type)
        self._rigidbodies_in_contact: set[RigidBody] = set()

        self._collision_begin_listeners: list[Callable] = []
        self._collision_while_listeners: list[Callable] = []
        self._collision_end_listeners: list[Callable] = []
    
    @override
    def on_remove(self):
        self.entity.location.world.physics_manager.remove_rigidbody(self)
        return super().on_remove()
    
    # Used to tell physics manager to change position
    def move_position(self, position: Vector2):
        self.entity.location.world.physics_manager.move_rigidbody_position(self, position)

    # Used to tell physics manager to change rotation
    def rotate_degrees(self, angle):
        self.entity.location.world.physics_manager.rotate_rigidbody_degrees(self, angle)

    def add_on_collision_begin_listener(self, callback: Callable):
        self._collision_begin_listeners.append(callback)

    def remove_on_collision_begin_listener(self, callback: Callable):
        self._collision_begin_listeners.remove(callback)

    def add_on_collision_end_listener(self, callback: Callable):
        self._collision_end_listeners.append(callback)

    def remove_on_collision_end_listener(self, callback: Callable):
        self._collision_end_listeners.remove(callback)

    def add_while_in_contact_listener(self, callback: Callable):
        self._collision_while_listeners.append(callback)

    def remove_while_in_contact_listener(self, callback: Callable):
        self._collision_while_listeners.remove(callback)

    def on_collision_begin(self, collided_rigidbody):
        for callback in self._collision_begin_listeners:
            callback(collided_rigidbody)
        self._rigidbodies_in_contact.add(collided_rigidbody)

    def on_collision_end(self, collided_rigidbody):
        for callback in self._collision_end_listeners:
            callback(collided_rigidbody)
        if collided_rigidbody in self._rigidbodies_in_contact:
            self._rigidbodies_in_contact.remove(collided_rigidbody)

    def while_in_contact(self, colliding_rigidbody):
        for callback in self._collision_while_listeners:
            callback(colliding_rigidbody)

    def set_body_type(self, body_type: BodyType):
        self.entity.location.world.physics_manager.set_rigidbody_body_type(self, body_type)

    def set_velocity(self, velocity: Vector2):
        self.entity.location.world.physics_manager.set_rigidbody_velocity(self, velocity)

    def set_size(self, new_size: Vector2):
        prev_size = self.entity.size
        self.entity.location.world.physics_manager.set_rigidbody_size(self, prev_size, new_size)
        self.entity.size = new_size

    @override
    def tick(self):
        to_remove: list[RigidBody] = []
        for rigidbody in self._rigidbodies_in_contact:
            if rigidbody.entity.dead:
                to_remove.append(rigidbody)
                continue
            self.while_in_contact(rigidbody)
        for rigidbody in to_remove:
            self._rigidbodies_in_contact.remove(rigidbody)

        return super().tick()

    # Used by physics manager to change location
    def on_position_update(self, position: Vector2):
        self.entity.location.position = position

    # Used by physics manager to change rotation
    def update_rotation_degrees(self, rotation: float):
        self.entity.location.rotation = rotation
    

    
    
