from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from data import data_loader

if TYPE_CHECKING:
    from sound_data import SoundData
    from material import MaterialData

SCREEN_WIDTH, SCREEN_HEIGHT = 700,1300
DEBUG = False
DELTA_TIME = 1 / 60
PHYSICS_SCALE = 32
RENDER_DISTANCE = 32
TNT_FUSE_TIME: float = 4.0
TNT_FLASH_INTERVAL: float = 0.4
BLOCK_SIZE = pygame.Vector2(1, 1)
PICKAXE_BREAK_DELAY = 0.05

camera: "Camera" # type: ignore

# Material Data
MATERIAL_DATA: dict[str, MaterialData] = data_loader.load_material_data()
SOUND_DATA: dict[str, SoundData] = data_loader.load_sound_data()


"""MATERIAL_SPAWN_RATE = {
    Material.BEDROCK: 0,

    Material.DIRT: 40,
    Material.STONE: 60,
    Material.ANDESITE: 15,
    Material.DIORITE: 15,
    Material.GRANITE: 15,
    Material.MOSSY_COBBLESTONE: 5,

    Material.COAL_ORE: 12,
    Material.IRON_ORE: 10,
    Material.COPPER_ORE: 10,
    Material.REDSTONE_ORE: 8,
    Material.LAPIS_ORE: 6,
    Material.GOLD_ORE: 5,
    Material.DIAMOND_ORE: 2,
    Material.EMERALD_ORE: 1,

    Material.OBSIDIAN: 1,
}

def get_material_health(material) -> float:
    if material == Material.BEDROCK:
        return 10_000_000_000

    elif material == Material.OBSIDIAN:
        return 200

    elif material in (
        Material.DIAMOND_ORE,
        Material.EMERALD_ORE,
        Material.GOLD_ORE
    ):
        return 25

    elif material in (
        Material.IRON_ORE,
        Material.COPPER_ORE,
        Material.REDSTONE_ORE,
        Material.LAPIS_ORE,
        Material.COAL_ORE
    ):
        return 20

    # Standard blocks
    elif material in (
        Material.DIRT,
        Material.STONE,
        Material.ANDESITE,
        Material.DIORITE,
        Material.GRANITE,
        Material.MOSSY_COBBLESTONE
    ):
        return 15

    else:
        return 15
"""
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
    