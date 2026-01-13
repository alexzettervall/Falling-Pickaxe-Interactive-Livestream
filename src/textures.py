from genericpath import isfile
import os

import pygame

def GetTexture(path):
    texture_packs = "..//texture-packs//"
    dirs = os.listdir(texture_packs)
    for dir in dirs:
        
        pack = texture_packs + dir
        path = pack + "//" + path
        if os.path.isfile(path):
            return pygame.image.load(path)
    
    raise ValueError(f"Couldn't find texture: {path}!")
