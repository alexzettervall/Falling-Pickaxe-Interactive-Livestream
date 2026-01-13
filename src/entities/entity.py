from typing import Type, TypeVar, Optional, Dict, cast

from pygame import Vector2
from component import Component
from location import Location

C = TypeVar("C", bound=Component)

class Entity():
    def __init__(self, location, size) -> None:
        self.components: list[Component] = []
        self.location: Location = location
        self.size: Vector2 = size

    def add_component(self, component: C) -> C:
        self.components.append(component)
        return component

    def get_component(self, component_type: Type[C]) -> Optional[C]:
        for component in self.components:
            if isinstance(component, component_type):
                return component
        return None

    def tick(self):
        for component in self.components:
            component.tick()

    def remove(self):
        self.location.world.remove_entity(self)
        for component in self.components:
            component.on_remove()