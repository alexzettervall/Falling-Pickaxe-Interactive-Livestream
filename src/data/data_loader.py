from __future__ import annotations
import json
import os
from typing import TYPE_CHECKING, Any
import pygame
from pygame import Surface, Vector2
from data.config import Config
from material import MaterialData
from sound_data import SoundData
from pygame.mixer import Sound


def load_texture(path):
    texture_packs = "..//texture-packs//"
    dirs = os.listdir(texture_packs)
    for dir in dirs:
        if dir == ".DS_Store":
            continue
        pack = texture_packs + dir
        path = pack + "//" + path
        if os.path.isfile(path):
            return pygame.image.load(path)
    
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
        
        material_datas[material] = MaterialData(sprite, max_health, spawn_rate)

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
        
        sound_datas[sound] = SoundData(sounds, volume)

    return sound_datas

def load_config() -> Config:
    path = "data//config.json"

    config_json: dict[str, Any] = json.loads(open(path, 'r').read())

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
    pickaxe_break_delay: float = config_json["pickaxe_break_delay"]

    config = Config(
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
        pickaxe_break_delay=pickaxe_break_delay,
    )

    return config