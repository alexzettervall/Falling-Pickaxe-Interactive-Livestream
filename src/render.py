import pygame
from entity import Entity
import variables
from world import World
from chunk import Chunk
from block import Block
from camera import Camera
from material import *

def render_world(camera: Camera, world: World, block_size: int):
    for chunk in world.chunks:
        render_chunk(camera, chunk, block_size)

def render_chunk(camera: Camera, chunk: Chunk, block_size: int):
    for block in chunk.blocks:
        render_block(camera, block, block_size)

def render_block(camera: Camera, block: Block, block_size: int):
    position = block.location.position
    screen_position = camera.world_to_screen_point(position)
    screen_size = camera.world_to_screen_size(block_size)
    
    material_data = variables.material_data

    material = block.material
    if not material in material_data:
        ValueError(f"Material: {material} not in material_data!")
    sprite = material_data[material].sprite
    sized_sprite = pygame.transform.scale(sprite, (screen_size, screen_size))
    rect = pygame.Rect(screen_position.x - screen_size / 2, screen_position.y - screen_size / 2, screen_size, screen_size)
    camera.surface.blit(sized_sprite, rect)

    destroy_index = block.destroy_state_index - 1
    if destroy_index < 0:
        return
    destroy_sprite = variables.destroy_stage_sprites[destroy_index]
    sized_destroy_sprite = pygame.transform.scale(destroy_sprite, (screen_size, screen_size))
    camera.surface.blit(sized_destroy_sprite, rect)
