from pygame.font import Font
from enum import Enum
from pygame import Color, Surface

import game_data
from render import SpriteData

class AlignmentType(Enum):
    Center = 1,
    Left = 2,
    Right = 3,

def render_text(font: Font, text: str, position: tuple[int, int], alignment_type: AlignmentType, color: str | Color = "white", antialias: bool = True):
    rendered_text = font.render(text, True, color)
    width, height = rendered_text.get_width(), rendered_text.get_height()
    aligned_position: tuple[int, int]
    if alignment_type == AlignmentType.Center:
        aligned_position = (position[0] - width // 2, position[1] - height // 2)
    elif alignment_type == AlignmentType.Left:
        aligned_position = (position[0], position[1] - height // 2)
    elif alignment_type == AlignmentType.Right:
        aligned_position = (position[0] - width, position[1] - height // 2)
    else:
        aligned_position = position
    game_data.renderer.texts.append(SpriteData(rendered_text, aligned_position, z = -1))