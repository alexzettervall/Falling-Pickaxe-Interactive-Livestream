import pygame
from enum import Enum 

class Material(Enum):
    BEDROCK = 1,
    DIRT = 2,
    STONE = 3,
    ANDESITE = 4,
    DIORITE = 5,
    GRANITE = 6,
    COAL_ORE = 7,
    IRON_ORE = 8,
    COPPER_ORE = 9,
    GOLD_ORE = 10,
    DIAMOND_ORE = 11,
    EMERALD_ORE = 12,
    OBSIDIAN = 13,
    REDSTONE_ORE = 14,
    LAPIS_ORE = 15,
    MOSSY_COBBLESTONE = 16

class MaterialData():
    def __init__(self, sprite: pygame.Surface):
        self.sprite = sprite