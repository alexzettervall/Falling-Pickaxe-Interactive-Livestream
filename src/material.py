import pygame
from enum import Enum 

class Material(Enum):
    BEDROCK = 1,
    GRASS = 2,
    STONE = 3,

class MaterialData():
    def __init__(self, sprite: pygame.Surface):
        self.sprite = sprite