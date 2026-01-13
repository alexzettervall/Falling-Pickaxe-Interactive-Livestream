import pygame
from textures import GetTexture
from material import Material
from material import MaterialData

DELTA_TIME = 1 / 60
PHYSICS_SCALE = 32
RENDER_DISTANCE = 32

camera: "Camera" # type: ignore

# Material Data
material_data: dict[Material, MaterialData] = {
    Material.BEDROCK: MaterialData(
        sprite=GetTexture("assets//minecraft//textures//block//bedrock.png")
    ),
    Material.DIRT: MaterialData(
        sprite=GetTexture("assets//minecraft//textures//block//dirt.png")
    ),
    Material.STONE: MaterialData(
        sprite=GetTexture("assets//minecraft//textures//block//stone.png")
    ),
    Material.ANDESITE: MaterialData(
        sprite=GetTexture("assets//minecraft//textures//block//andesite.png")
    ),
    Material.DIORITE: MaterialData(
        sprite=GetTexture("assets//minecraft//textures//block//diorite.png")
    ),
    Material.GRANITE: MaterialData(
        sprite=GetTexture("assets//minecraft//textures//block//granite.png")
    ),
    Material.COAL_ORE: MaterialData(
        sprite=GetTexture("assets//minecraft//textures//block//coal_ore.png")
    ),
    Material.IRON_ORE: MaterialData(
        sprite=GetTexture("assets//minecraft//textures//block//iron_ore.png")
    ),
    Material.COPPER_ORE: MaterialData(
        sprite=GetTexture("assets//minecraft//textures//block//copper_ore.png")
    ),
    Material.GOLD_ORE: MaterialData(
        sprite=GetTexture("assets//minecraft//textures//block//gold_ore.png")
    ),
    Material.DIAMOND_ORE: MaterialData(
        sprite=GetTexture("assets//minecraft//textures//block//diamond_ore.png")
    ),
    Material.EMERALD_ORE: MaterialData(
        sprite=GetTexture("assets//minecraft//textures//block//emerald_ore.png")
    ),
    Material.OBSIDIAN: MaterialData(
        sprite=GetTexture("assets//minecraft//textures//block//obsidian.png")
    ),
    Material.REDSTONE_ORE: MaterialData(
        sprite=GetTexture("assets//minecraft//textures//block//redstone_ore.png")
    ),
    Material.LAPIS_ORE: MaterialData(
        sprite=GetTexture("assets//minecraft//textures//block//lapis_ore.png")
    ),
    Material.MOSSY_COBBLESTONE: MaterialData(
        sprite=GetTexture("assets//minecraft//textures//block//mossy_cobblestone.png")
    ),
}


MATERIAL_SPAWN_RATE = {
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

def get_material_health(material):
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

def load_sprites():
    global sprite_tnt
    sprite_tnt = GetTexture("assets//minecraft//textures//block//tnt_side.png")
    sprite_tnt = sprite_tnt.convert_alpha()

    global sprite_wooden_pickaxe
    sprite_wooden_pickaxe = GetTexture("assets//minecraft//textures//item//wooden_pickaxe.png")
    sprite_wooden_pickaxe = sprite_wooden_pickaxe.convert_alpha()

    global sprite_smoke_particle
    sprite_smoke_particle = GetTexture("assets//minecraft//textures//particle//spark_6.png")
    sprite_smoke_particle = sprite_smoke_particle.convert_alpha()

    global explosion_sprites
    explosion_sprites = []
    for i in range(16):
        explosion_sprites.append(GetTexture(f"assets//minecraft//textures//particle//explosion_{i}.png"))
        explosion_sprites[i].convert_alpha()

    global destroy_stage_sprites
    destroy_stage_sprites = []
    for i in range(10):
        destroy_stage_sprites.append(GetTexture(f"assets//minecraft//textures//block//destroy_stage_{i}.png"))
        destroy_stage_sprites[i].convert_alpha()
    