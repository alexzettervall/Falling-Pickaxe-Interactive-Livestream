import pygame

DELTA_TIME = 1 / 60

camera: "Camera" # type: ignore

# Sprites
sprite_tnt: pygame.Surface

def load_sprites():
    global sprite_tnt
    sprite_tnt = pygame.image.load("..//sprites//blocks//tnt.png")
    sprite_tnt = sprite_tnt.convert_alpha()