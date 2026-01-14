from typing import override
from components.crack_visual import CrackVisual
from components.health import Health
from entities.block import Block
import game_data


class DamageableBlock(Block):
    @override
    def __init__(self, chunk, material, location):
        super().__init__(chunk, material, location)
        health = self.add_component(Health(self, game_data.MATERIAL_DATA[self.material].max_health))
        self.add_component(CrackVisual(self, health))