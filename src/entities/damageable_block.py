from typing import override
from components.crack_visual import CrackVisual
from components.health import Health
from entities.block import Block
import variables


class DamageableBlock(Block):
    @override
    def __init__(self, chunk, material, location):
        super().__init__(chunk, material, location)
        health = self.add_component(Health(self, variables.get_material_health(self.material)))
        self.add_component(CrackVisual(self, health))