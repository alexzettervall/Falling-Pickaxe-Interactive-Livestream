import pygame
from components.crack_visual import CrackVisual
from entities.entity import Entity
import game_data
from world import World
from chunk import Chunk
from entities.block import Block
from camera import Camera
from material import *

def render_world(camera: Camera, world: World):
    world.background.render()
    for chunk in world.chunks:
        render_chunk(camera, chunk)

def render_chunk(camera: Camera, chunk: Chunk):
    for block in chunk.blocks:
        render_block(camera, block)

def render_block(camera: Camera, block: Block,):
    position = block.location.position
    screen_position = camera.world_to_screen_point(position)
    screen_size_x = camera.world_to_screen_size(game_data.config.block_size.x)
    screen_size_y = camera.world_to_screen_size(game_data.config.block_size.y)
    
    material_data = game_data.MATERIAL_DATA

    material = block.material
    if not material in material_data:
        ValueError(f"Material: {material} not in material_data!")
    sprite = material_data[material].sprite
    sized_sprite = pygame.transform.scale(sprite, (screen_size_x, screen_size_y))
    rect = pygame.Rect(screen_position.x - screen_size_x / 2, screen_position.y - screen_size_y / 2, screen_size_x, screen_size_y)
    camera.surface.blit(sized_sprite, rect)

    crack_visual = block.get_component(CrackVisual)
    if crack_visual == None:
        return
    destroy_index = crack_visual.destroy_stage_index - 1
    if destroy_index < 0:
        return
    destroy_sprite = game_data.destroy_stage_sprites[destroy_index]
    sized_destroy_sprite = pygame.transform.scale(destroy_sprite, (screen_size_x, screen_size_y))
    camera.surface.blit(sized_destroy_sprite, rect)


