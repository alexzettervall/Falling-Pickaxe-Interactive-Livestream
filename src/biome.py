import random
from typing import NamedTuple
from pygame import Vector2
import game_data

class BlockData(NamedTuple):
    name: str
    frequency: float

class BiomeData(NamedTuple):
    blocks: list[BlockData]
    frequency: float

last_biome: str = ""

def get_biome() -> str:
    global last_biome
    total_weight: float = 0.0
    for biome_name in game_data.BIOME_DATA.keys():
        if biome_name == last_biome:
            continue
        total_weight += game_data.BIOME_DATA[biome_name].frequency
    for biome_name in game_data.BIOME_DATA.keys():
        if biome_name == last_biome:
            continue
        biome_data = game_data.BIOME_DATA[biome_name]
        rand = random.uniform(0, total_weight)
        if rand < biome_data.frequency:
            last_biome = biome_name
            return biome_name
        total_weight -= biome_data.frequency
    return "none"

def get_block(biome: str) -> str:
    biome_data: BiomeData = game_data.BIOME_DATA[biome]

    total_weight: float = 0.0
    for block_data in biome_data.blocks:
        total_weight += block_data.frequency
    for block_data in biome_data.blocks:
        rand = random.uniform(0, total_weight)
        spawn_rate = block_data.frequency
        if rand < spawn_rate:
            return block_data.name
        total_weight -= spawn_rate
    return "none"