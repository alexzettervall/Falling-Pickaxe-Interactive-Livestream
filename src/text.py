from pygame.font import Font
from enum import Enum
from pygame import Color, Surface

class AlignmentType(Enum):
    Center = 1,
    Left = 2,
    Right = 3,

def render_text(font: Font, text: str, surface: Surface, alignment_type: AlignmentType, color: str | Color = "white", antialias: bool = True):
    rendered_text = font.render(text, True, color)
    surface.blit(render_text, ())