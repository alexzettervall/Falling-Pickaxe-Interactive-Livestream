from typing import override

from pygame import Vector2
from chunk import Chunk
from entities.block import BlockBreaker
from entities.tnt import TNT
import game_data


class Nuke(TNT):
    @override
    def __init__(self, location, user: str | None = None) -> None:
        super().__init__(None, location, user)
        self.rigidbody.set_size(Vector2(2.5, 2.5))

        self.explosion_radius = game_data.config.nuke_radius
        self.explosion_damage = game_data.config.nuke_damage
        self.text_renderer.font = "big"
        self.text_renderer.text = "🔴NUKE"
        self.text_renderer.offset = Vector2(0, 1.5)
        self.fuse *= 2