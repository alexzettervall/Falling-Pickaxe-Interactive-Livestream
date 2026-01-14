from __future__ import annotations
import json
import os
from typing import TYPE_CHECKING, Any
import pygame
from pygame import Surface
from material import MaterialData
from sound_data import SoundData
from pygame.mixer import Sound


def load_texture(path):
    texture_packs = "..//texture-packs//"
    dirs = os.listdir(texture_packs)
    for dir in dirs:
        
        pack = texture_packs + dir
        path = pack + "//" + path
        if os.path.isfile(path):
            return pygame.image.load(path)
    
    raise ValueError(f"Couldn't find texture: {path}!")

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