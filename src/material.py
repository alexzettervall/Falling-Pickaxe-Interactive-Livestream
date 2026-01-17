import pygame

class MaterialData():
    def __init__(self, sprite: pygame.Surface, max_health: float, spawn_rate: float, break_sound: str | None = None, experience: float = 0):
        self.sprite = sprite
        self.max_health = max_health
        self.spawn_rate = spawn_rate
        self.break_sound: str | None = break_sound
        self.experience: float = experience