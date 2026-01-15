

from typing import override

from pygame import Vector2
from component import Component
from text import AlignmentType, render_text
import game_data

class TextRenderer(Component):
    @override
    def __init__(self, entity, offset: Vector2, alignment_type: AlignmentType) -> None:
        super().__init__(entity)

        self.offset: Vector2 = offset
        self.text: str = ""
        self.alignment_type: AlignmentType = alignment_type

    @override
    def tick(self):
        position = self.entity.location.position + self.offset
        screen_position = game_data.camera.world_to_screen_point(position)
        render_text(game_data.font, self.text, (round(screen_position.x), round(screen_position.y)),
                     AlignmentType.Center)

        return super().tick()