import pygame

class MaterialData():
    def __init__(self, sprite: pygame.Surface, max_health: float, spawn_rate: float):
        self.sprite = sprite
        self.max_health = max_health
        self.spawn_rate = spawn_rate