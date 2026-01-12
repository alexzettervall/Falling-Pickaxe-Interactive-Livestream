from typing import override
from pygame import Vector2
from components.rigidbody import RigidBody
from components.sprite_renderer import SpriteRenderer
from entity import Entity
import variables

class TNT(Entity):
    def __init__(self, location) -> None:
        super().__init__(location, Vector2(2, 2))

        sprite = variables.sprite_tnt
        self.add_component(RigidBody(self))
        self.add_component(SpriteRenderer(self, variables.camera, sprite))

        self.fuse: float = 3

    @override
    def tick(self):
        self.fuse -= variables.DELTA_TIME
        if self.fuse <= 0:
            self.location.world.create_explosion(self.location, 5, 30)
            self.remove()
        return super().tick()
    
