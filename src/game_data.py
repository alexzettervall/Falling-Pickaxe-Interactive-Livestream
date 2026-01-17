from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from pygame.font import Font
from data import data_loader


if TYPE_CHECKING:
    from sound_data import SoundData
    from material import MaterialData
    from camera import Camera
    from render import Renderer
    import biome
    from text import Display
    from data.config import Config

"""SCREEN_WIDTH, SCREEN_HEIGHT = 1400,800
DEBUG = False
DELTA_TIME = 1 / 60
PHYSICS_SCALE = 32
RENDER_DISTANCE = 24
TNT_FUSE_TIME: float = 4
TNT_FLASH_INTERVAL: float = 0.4
BLOCK_SIZE = pygame.Vector2(1, 1)
PICKAXE_BREAK_DELAY = 0.05"""


config: Config = data_loader.load_config()
MATERIAL_DATA: dict[str, MaterialData] = data_loader.load_material_data()
SOUND_DATA: dict[str, SoundData] = data_loader.load_sound_data()
BIOME_DATA: dict[str, biome.BiomeData] = data_loader.load_biome_data()
PICKAXE_DATA: dict[str, data_loader.PickaxeData] = data_loader.load_pickaxe_data()
camera: Camera
renderer: Renderer

font_name = "arial"

_normalized_font_size: float = 0.0320512821 * config.screen_width

FONTS: dict[str, Font] = {
        "default": Font("assets/fonts/PixelEmulator-xq08.ttf", round(1 * _normalized_font_size)),
        "big": Font("assets/fonts/PixelEmulator-xq08.ttf", round(1.5 * _normalized_font_size))
        }
DISPLAY: Display = data_loader.load_display()
#font = pygame.font.SysFont(font_name, 20)

def load_sprites():
    global sprite_tnt
    sprite_tnt = data_loader.load_texture("assets//minecraft//textures//block//tnt_side.png")
    sprite_tnt = sprite_tnt.convert_alpha()

    global sprite_wooden_pickaxe
    sprite_wooden_pickaxe = data_loader.load_texture("assets//minecraft//textures//item//wooden_pickaxe.png")
    sprite_wooden_pickaxe = sprite_wooden_pickaxe.convert_alpha()

    global sprite_smoke_particle
    sprite_smoke_particle = data_loader.load_texture("assets//minecraft//textures//particle//spark_6.png")
    sprite_smoke_particle = sprite_smoke_particle.convert_alpha()

    global sprite_background
    sprite_background = data_loader.load_sprite("background.png")
    sprite_background = sprite_background.convert_alpha()

    global explosion_sprites
    explosion_sprites = []
    for i in range(16):
        explosion_sprites.append(data_loader.load_texture(f"assets//minecraft//textures//particle//explosion_{i}.png"))
        explosion_sprites[i].convert_alpha()

    global destroy_stage_sprites
    destroy_stage_sprites = []
    for i in range(10):
        destroy_stage_sprites.append(data_loader.load_texture(f"assets//minecraft//textures//block//destroy_stage_{i}.png"))
        destroy_stage_sprites[i].convert_alpha()
    