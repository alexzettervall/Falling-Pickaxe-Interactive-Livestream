from pygame import Vector2
from component import Component
from typing import Callable, override, TYPE_CHECKING
from variables import PHYSICS_SCALE
from physics import CollisionType, BodyType

class RigidBody(Component):
    def __init__(self, entity, shapes: list[list[tuple[float, float]]], collision_type: CollisionType = CollisionType.ENTITY, body_type: BodyType = BodyType.DYNAMIC) -> None:
        super().__init__(entity)
        
        for vertices in shapes:
            for i in range(len(vertices)):
                vertex = vertices[i]
                vertices[i] = ((vertex[0]) * self.entity.size.x * PHYSICS_SCALE, (-vertex[1]) * self.entity.size.y * PHYSICS_SCALE)

        self.entity.location.world.physics_manager.add_rigidbody(self, shapes, collision_type, body_type)
        self._collision_begin_listeners: list[Callable] = []
    
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

    def on_collision_begin(self, collided_rigidbody):
        for callback in self._collision_begin_listeners:
            callback(collided_rigidbody)

    def add_on_collision_listener(self, callback: Callable):
        self._collision_begin_listeners.append(callback)

    def on_collision_end(self, collided_rigidbody):
        pass

    # Used by physics manager to change location
    def update_position(self, position: Vector2):
        self.entity.location.position = position

    # Used by physics manager to change rotation
    def update_rotation_degrees(self, rotation: float):
        self.entity.location.rotation = rotation
    

    
    
