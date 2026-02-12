from pprint import isreadable
from typing import Type, TypeVar, Optional, Dict, cast

from pygame import Vector2
from component import Component
from location import Location
from time import sleep
from threading import Thread
import game_data

C = TypeVar("C", bound=Component)

class Entity():
    def __init__(self, location, size) -> None:
        self.dead = False
        self.lifetime: float = 0.0
        self.life_timer: bool = False

        self.components: list[Component] = []
        self.location: Location = location
        self.size: Vector2 = size

    def add_component(self, component: C) -> C:
        self.components.append(component)
        return component
    
    def remove_component(self, component_type: Type[C]) -> bool:
        for component in self.components:
            if isinstance(component, component_type):
                component.on_remove()
                self.components.remove(component)
                return True
        return False

    def get_component(self, component_type: Type[C]) -> Optional[C]:
        for component in self.components:
            if isinstance(component, component_type):
                return component
        return None

    def tick(self):
        for component in self.components:
            component.tick()

        if self.life_timer:
            self.lifetime -= game_data.config.delta_time
            if self.lifetime <= 0:
                self.remove()

    def remove_after(self, time: float):
        if self.dead:
            return
        
        self.lifetime = time
        self.life_timer = True
        return

    def remove(self):
        if self.dead:
            return
        
        self.dead = True
        self.location.world.remove_entity(self)
        for component in self.components:
            component.on_remove()