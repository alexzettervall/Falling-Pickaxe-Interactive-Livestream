from pprint import isreadable
from typing import Type, TypeVar, Optional, Dict, cast

from pygame import Vector2
from component import Component
from location import Location
from time import sleep
from threading import Thread

C = TypeVar("C", bound=Component)

class Entity():
    def __init__(self, location, size) -> None:
        self.dead = False
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

    def remove(self, time: float = 0):
        if self.dead:
            return
        Thread(target = self._remove, args = [time], daemon = True).start()
        
    def _remove(self, time: float = 0):
        if self.dead:
            return
        
        if time > 0:
            sleep(time)
        
        self.dead = True
        self.location.world.remove_entity(self)
        for component in self.components:
            component.on_remove()