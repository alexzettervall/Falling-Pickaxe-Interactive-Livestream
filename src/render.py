from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from components.crack_visual import CrackVisual
import game_data
from entities.block import Block
from pygame import Rect, Surface
from typing import NamedTuple
if TYPE_CHECKING:
    from world import World
    from chunk import Chunk

class SpriteData(NamedTuple):
    surface: Surface
    rect: Rect
    z: int

class Renderer():
    def __init__(self, world: World) -> None:
        self.world: World = world
        
        self.sprites: list[SpriteData] = []
        self.particles: list[SpriteData]= []
        self.texts: list[SpriteData]= []

    def tick(self):
        self.render_background()
        self.render_blocks()
        self.render_sprites()
        self.render_particles()
        self.render_text()

    def render_background(self):
        self.world.background.render()

    def render_blocks(self):
        for chunk in self.world.chunks:
            self.render_chunk(chunk)

    def render_sprites(self):
        for sprite in self.sprites:
            game_data.camera.surface.blit(sprite[0], sprite[1])
        self.sprites = []

    def render_particles(self):
        for particle in self.particles:
            game_data.camera.surface.blit(particle[0], particle[1])
        self.particles = []

    def render_text(self):
        for text in self.texts:
            game_data.camera.surface.blit(text[0], text[1])
        self.texts = []

    def render_chunk(self, chunk: Chunk):
        for block in chunk.blocks:
            self.render_block(block)

    def render_block(self, block: Block,):
        position = block.location.position
        camera = game_data.camera
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
        rotated_sprite = pygame.transform.rotate(sized_sprite, block.location.rotation)
        camera.surface.blit(rotated_sprite, rotated_sprite.get_rect(center = rect.center))

        crack_visual = block.get_component(CrackVisual)
        if crack_visual == None:
            return
        destroy_index = crack_visual.destroy_stage_index - 1
        if destroy_index < 0:
            return
        destroy_sprite = game_data.destroy_stage_sprites[destroy_index]
        sized_destroy_sprite = pygame.transform.scale(destroy_sprite, (screen_size_x, screen_size_y))
        rotated_destroy_sprite = pygame.transform.rotate(sized_destroy_sprite, block.location.rotation)
        camera.surface.blit(rotated_destroy_sprite, rotated_destroy_sprite.get_rect(center = rect.center))


