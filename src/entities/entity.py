from typing import Type, TypeVar, Optional, Dict, cast

from pygame import Vector2
from component import Component
from location import Location

C = TypeVar("C", bound=Component)

class Entity():
    def __init__(self, location, size) -> None:
        self.components: Dict[Type[Component], Component] = {}
        self.location: Location = location
        self.size: Vector2 = size

    def add_component(self, component: C) -> C:
        self.components[type(component)] = component
        return component

    def get_component(self, component_type: Type[C]) -> Optional[C]:
        component = self.components.get(component_type)
        return cast(Optional[C], component)

    def tick(self):
        for component in self.components.values():
            component.tick()

    def remove(self):
        self.location.world.remove_entity(self)
        for component in self.components.values():
            component.on_remove()