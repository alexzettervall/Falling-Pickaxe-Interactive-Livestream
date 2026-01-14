from typing import override
from components.crack_visual import CrackVisual
from components.health import Health
from entities.block import Block
import game_data
from particles.particles import ParticleType


class DamageableBlock(Block):
    @override
    def __init__(self, chunk, material, location):
        super().__init__(chunk, material, location)
        self.health = self.add_component(Health(self, game_data.MATERIAL_DATA[self.material].max_health))
        self.add_component(CrackVisual(self, self.health))
        self.health.add_listener(self.on_damaged)


    def on_damaged(self):
        amount = 0
        if self.health.health <= 0:
            amount = 25
        self.location.world.particle_manager.emit(ParticleType.BLOCK, self.location, amount, game_data.MATERIAL_DATA[self.material].sprite)