from __future__ import annotations
import json
import os
import game_data
import text
from typing import TYPE_CHECKING, Any
import pygame
from pygame import Surface, Vector2
from data.config import Config
from material import MaterialData
from sound_data import SoundData
from pygame.mixer import Sound
import biome
from typing import NamedTuple
from pygame.font import Font



def load_texture(path):
    texture_packs = "..//texture-packs//"
    dirs = os.listdir(texture_packs)
    for dir in dirs:
        if dir == ".DS_Store":
            continue
        pack = texture_packs + dir
        path = pack + "//" + path
        if os.path.isfile(path):
            surface = pygame.image.load(path)
            surface = surface.convert_alpha()
            return surface
    
    raise ValueError(f"Couldn't find texture: {path}!")

def load_sprite(path):
    return pygame.image.load("assets//sprites//" + path)

def load_material_data() -> dict[str, MaterialData]:
    path = "data//materials.json"

    material_datas: dict[str, MaterialData] = {}
    material_datas_json: dict[str, dict[str, Any]] = json.loads(open(path, 'r').read())

    for material in material_datas_json.keys():
        material_data_json = material_datas_json[material]

        sprite: Surface = load_texture(material_data_json["texture_path"])
        max_health: float = material_data_json["max_health"]
        spawn_rate: float = material_data_json["spawn_rate"]
        break_sound: str | None = None
        if "break_sound" in material_data_json:
            break_sound = material_data_json["break_sound"]
        
        material_datas[material] = MaterialData(sprite, max_health, spawn_rate, break_sound)

    return material_datas
    
def load_sound_data() -> dict[str, SoundData]:
    path = "data//sounds.json"

    sound_datas: dict[str, SoundData] = {}
    sound_datas_json: dict[str, dict[str, Any]] = json.loads(open(path, 'r').read())

    for sound in sound_datas_json.keys():
        sound_data_json = sound_datas_json[sound]

        sounds: list[Sound] = []
        sound_names: list[str] = sound_data_json["sounds"]
        for sound_name in sound_names:
            sounds.append(Sound("assets//sounds//" + sound_name))
        volume: float = sound_data_json["volume"]

        max_play_frequency: float = 50.0
        if "max_play_frequency" in sound_data_json:
            max_play_frequency = sound_data_json["max_play_frequency"]

        queue_rate_limited_sounds: bool = False
        if "queue_rate_limited_sounds" in sound_data_json:
            queue_rate_limited_sounds = sound_data_json["queue_rate_limited_sounds"]
        
        sound_datas[sound] = SoundData(sounds, volume, max_play_frequency, queue_rate_limited_sounds)

    return sound_datas

def load_config() -> Config:
    path = "data//config.json"
    
    file = open(path, 'r')
    config_json: dict[str, Any] = json.loads(file.read())
    file.close()

    stream_url: str = config_json["stream_url"]
    listen_to_stream: bool = config_json["listen_to_stream"]
    screen_width: int = config_json["screen_width"]
    screen_height: int = config_json["screen_height"]
    chunk_size: tuple[int, int] = tuple(config_json["chunk_size"])
    camera_size: int = config_json["camera_size"]
    fps: float = config_json["fps"]
    debug: bool = config_json["debug"]
    delta_time: float = config_json["delta_time"]
    physics_scale: float = config_json["physics_scale"]
    render_distance: float = config_json["render_distance"]
    tnt_fuse_time: float = config_json["tnt"]["fuse_time"]
    tnt_flash_interval: float = config_json["tnt"]["flash_interval"]
    tnt_radius: float = config_json["tnt"]["radius"]
    tnt_damage: float = config_json["tnt"]["damage"]
    block_size: Vector2 = Vector2(config_json["block_size"])
    pickaxe_break_delay: float = config_json["default_break_speed"]

    config = Config(
        stream_url=stream_url,
        listen_to_stream=listen_to_stream,
        screen_width=screen_width,
        screen_height=screen_height,
        chunk_size=chunk_size,
        camera_size=camera_size,
        fps=fps,
        debug=debug,
        delta_time=delta_time,
        physics_scale=physics_scale,
        render_distance=render_distance,
        tnt_fuse_time=tnt_fuse_time,
        tnt_flash_interval=tnt_flash_interval,
        tnt_radius=tnt_radius,
        tnt_damage=tnt_damage,
        block_size=block_size,
        default_break_speed=pickaxe_break_delay,
        normal_speed=config_json["normal_speed"],
        fast_speed=config_json["fast_speed"],
        slow_speed=config_json["slow_speed"],
        speed_change_duration=config_json["speed_change_duration"],
        normal_pickaxe_size=config_json["normal_pickaxe_size"],
        big_pickaxe_size=config_json["big_pickaxe_size"],
        small_pickaxe_size=config_json["small_pickaxe_size"],
        pickaxe_size_change_duration=config_json["pickaxe_size_change_duration"],

        chat_message_time=config_json["chat_message_time"],
        chat_color=config_json["chat_color"],
        chat_font=config_json["chat_font"],
        chat_max_displayed_messages=config_json["chat_max_displayed_messages"],
        chat_position=tuple(config_json["chat_position"]),
        chat_alignment_type=text.AlignmentType[config_json["chat_alignment_type"]],
    )

    return config

def load_biome_data() -> dict[str, biome.BiomeData]:
    path = "data//biomes.json"

    file = open(path, 'r')
    biomes_json: dict[str, Any] = json.loads(file.read())
    biomes: dict[str, biome.BiomeData] = {}
    file.close()

    for biome_name in biomes_json.keys():
        biome_json = biomes_json[biome_name]
        blocks_json = biome_json["blocks"]
        blocks: list[biome.BlockData] = []
        for block_name in blocks_json.keys():
            block_json = blocks_json[block_name]
            blocks.append(biome.BlockData(block_name, block_json["frequency"]))
        biomes[biome_name] = biome.BiomeData(blocks, biome_json["frequency"])

    return biomes

class PickaxeData(NamedTuple):
    sprite: Surface
    damage: float
    dig_speed: float

def load_pickaxe_data() -> dict[str, PickaxeData]:
    path = "data//pickaxes.json"

    file = open(path, 'r')
    pickaxes_json: dict[str, Any] = json.loads(file.read())
    pickaxes: dict[str, PickaxeData] = {}
    file.close()

    for pickaxe_name in pickaxes_json.keys():
        pickaxe_json = pickaxes_json[pickaxe_name]
        pickaxes[pickaxe_name] = PickaxeData(
            sprite=load_texture(pickaxe_json["texture_path"]),
            damage=pickaxe_json["damage"],
            dig_speed=pickaxe_json["dig_speed"]
        )

    return pickaxes

def load_display() -> text.Display:
    path = "data//display.json"

    file = open(path, 'r', encoding = "utf-8")
    display_json: dict[str, Any] = json.loads(file.read())
    file.close()

    texts: list[text.Text] = []

    for text_name in display_json.keys():
        text_json: dict[str, Any] = display_json[text_name]
        font_name: str = text_json["font"]
        font: Font = game_data.FONTS[font_name]

        screen_position: tuple[int, int] = (
            text_json["screen_position"][0],
            text_json["screen_position"][1]
        )
        
        texts.append(text.Text(
            font=font,
            text=text_json["text"],
            screen_position=screen_position,
            alignment_type=text.AlignmentType[text_json["alignment_type"]],
            color=text_json["color"],
            antialias=text_json["antialias"]
        ))

    return text.Display(texts)