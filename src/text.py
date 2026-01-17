from __future__ import annotations
from typing import TYPE_CHECKING
from pygame.font import Font
from enum import Enum
from pygame import Color, Rect, Surface

import game_data
from render import SpriteData
if TYPE_CHECKING:
    from world import World

class AlignmentType(Enum):
    CENTER = 1,
    LEFT = 2,
    RIGHT = 3,

COLOR_PREFIXES = {
    "🔴": "red",
    "🟢": "green",
    "🔵": "blue",
    "🟡": "yellow",
    "🟠": "orange",
    "🟣": "purple",
    "⚫": "black",
    "⚪": "white",
}

def render_text(font: Font, text: str, screen_position: tuple[int, int], alignment_type: AlignmentType, color: str | Color = "white", antialias: bool = True, lines_go_down: bool = True):
    lines: list[str] = str.splitlines(text)
    text_height = font.get_height()
    for i in range(len(lines)):
        line = lines[i]
        if lines_go_down:
            new_screen_position = (screen_position[0], screen_position[1] + i * text_height)
        else:
            new_screen_position = (screen_position[0], screen_position[1] + i * -text_height)
        _render_line(font, line, new_screen_position, alignment_type, color, antialias)
    
def _render_line(font: Font, text: str, screen_position: tuple[int, int], alignment_type: AlignmentType, color: str | Color = "white", antialias: bool = True):
    for emoji, color_name in COLOR_PREFIXES.items():
        if text.startswith(emoji):
            text = text.removeprefix(emoji)
            color = color_name
            break

    rendered_text = font.render(text, True, color)
    drop_shadows: list[tuple[Surface, tuple[int, int]]] = []
    outline_width = 2
    drop_shadows.append((font.render(text, True, "black"), (0, -outline_width)))
    drop_shadows.append((font.render(text, True, "black"), (0, outline_width)))
    drop_shadows.append((font.render(text, True, "black"), (-outline_width, 0)))
    drop_shadows.append((font.render(text, True, "black"), (outline_width, 0)))
    width, height = rendered_text.get_width(), rendered_text.get_height()
    x, y = 0, 0
    if alignment_type == AlignmentType.CENTER:
        x, y = (screen_position[0] - width // 2), (screen_position[1] - height // 2)
    elif alignment_type == AlignmentType.LEFT:
        x, y = (screen_position[0], screen_position[1] - height // 2)
    elif alignment_type == AlignmentType.RIGHT:
        x, y = (screen_position[0] - width, screen_position[1] - height // 2)
    else:
        aligned_position = screen_position
        
    for drop_shadow in drop_shadows:
        game_data.renderer.texts.append(SpriteData(drop_shadow[0], Rect(x + drop_shadow[1][0], y + drop_shadow[1][1], 0, 0), z = -1))
    game_data.renderer.texts.append(SpriteData(rendered_text, Rect(x, y, 0, 0), z = -1))

class Text():
    def __init__(self, font: Font, text: str, screen_position: tuple[int, int], alignment_type: AlignmentType, color: str | Color = "white", antialias: bool = True) -> None:
        self.font: Font = font
        self.text: str = text
        self.screen_position: tuple[int, int] = screen_position
        self.alignment_type: AlignmentType = alignment_type
        self.color: Color | str = color
        self.antialias: bool = antialias

        self.text_to_render = text

    def render(self):
        render_text(self.font, self.text_to_render, self.screen_position, self.alignment_type, self.color, self.antialias)

class Display():
    def __init__(self, texts: dict[str, Text]) -> None:
        self.texts = texts

    def tick(self, world: World):
        nuke_text = self.texts["nuke"].text
        nuke_text = str.replace(nuke_text, "{xp}", str(round(world.xp)))
        nuke_text = str.replace(nuke_text, "{nuke_xp}", str(round(game_data.config.nuke_xp)))
        self.texts["nuke"].text_to_render = nuke_text

        self._render()

    def _render(self):
        for text in self.texts.values():
            text.render()