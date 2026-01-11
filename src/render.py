import pygame
from entity import Entity
from world import World
from chunk import Chunk
from block import Block
from camera import Camera
from material import *

def render_world(camera: Camera, material_data: dict[Material, MaterialData], world: World, block_size: int):
    for chunk in world.chunks:
        render_chunk(camera, material_data, chunk, block_size)

    for entity in world.entities:
        render_entity(camera, entity)

def render_chunk(camera: Camera, material_data: dict[Material, MaterialData], chunk: Chunk, block_size: int):
    for block in chunk.blocks:
        render_block(camera, material_data, block, block_size)

def render_block(camera: Camera, material_data: dict[Material, MaterialData], block: Block, block_size: int):
    position = block.location.position
    screen_position = camera.world_to_screen_point(position)
    screen_size = camera.world_to_screen_size(block_size)
    
    material = block.material
    if not material in material_data:
        ValueError(f"Material: {material} not in material_data!")
    sprite = material_data[material].sprite
    sized_sprite = pygame.transform.scale(sprite, (screen_size, screen_size))
    rect = pygame.Rect(screen_position.x - screen_size / 2, screen_position.y - screen_size / 2, screen_size, screen_size)
    camera.surface.blit(sized_sprite, rect)

def render_entity(camera: Camera, entity: Entity):
    screen_position = camera.world_to_screen_point(entity.location.position)
    screen_size_x = camera.world_to_screen_size(entity.size.width)
    screen_size_y = camera.world_to_screen_size(entity.size.height)
    sprite = pygame.image.load("..//sprites//blocks//tnt.png")
    sized_sprite = pygame.transform.scale(sprite, (screen_size_x, screen_size_y))
    rect = pygame.Rect(screen_position.x - screen_size_x / 2, screen_position.y - screen_size_y / 2, screen_size_x, screen_size_y)
    camera.surface.blit(sized_sprite, rect)