from typing import Callable
from component import Component


class Health(Component):
    def __init__(self, entity, max_health: float) -> None:
        super().__init__(entity)
        self.max_health = max_health
        self.health = self.max_health
        self._listeners: list[Callable] = []

    def damage(self, damage: float):
        self.health -= damage
        if self.health <= 0:
            self.entity.remove()
        self._notify()
            
    def add_listener(self, callback: Callable):
        self._listeners.append(callback)

    def _notify(self):
        for callback in self._listeners:
            callback()