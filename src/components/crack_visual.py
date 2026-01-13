from math import floor
from typing import override
from component import Component
from components.health import Health
import game_data


class CrackVisual(Component):
    @override
    def __init__(self, entity, health: Health) -> None:
        super().__init__(entity)
        self.health: Health = health
        self.health.add_listener(self.on_health_change)
        self.destroy_stage_index = 0

    def on_health_change(self):
        health = self.health.health
        max_health = self.health.max_health
        n = len(game_data.destroy_stage_sprites)
        self.destroy_stage_index = min(floor(n * ((max_health - health) / max_health)), n)