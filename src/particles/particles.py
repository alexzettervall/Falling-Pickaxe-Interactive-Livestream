from enum import Enum
from math import cos, floor, sin
import random
from typing import override
from numpy import var
from pygame import Surface, Vector2
import pygame
from location import Location
import game_data
from game_data import config
from render import SpriteData

class ParticleType(Enum):
    EXPLOSION = 1,
    BLOCK = 2,

class Particle():
    def __init__(self, particle_manager, location: Location, size: Vector2, sprite: Surface, time: float) -> None:
        self.particle_manager = particle_manager
        self.location = location
        self.size = size
        self.sprite = sprite
        self.time = time
        self.alpha = 1
    
    def tick(self):
        self.time -= config.delta_time
        if self.time <= 0:
            self.remove()
        pass

    def remove(self):
        self.particle_manager.remove(self)

class ExplosionParticle(Particle):
    @override
    def __init__(self, particle_manager, location: Location) -> None:
        spread = 2
        location.move(random.uniform(-spread, spread), random.uniform(-spread, spread))
        size = random.uniform(1.0, 2.0)
        self.size = Vector2(size, size)
        self.life_span = 0.25
        self.time = self.life_span
        self.sprite_index = 0
        location.rotation = random.uniform(0, 360)
        super().__init__(particle_manager, location, self.size, game_data.explosion_sprites[0], self.time)
        

    @override
    def tick(self):
        self.sprite_index = floor(0 + 15 * ((self.life_span - self.time) / self.life_span))
        self.sprite = game_data.explosion_sprites[self.sprite_index]
        super().tick()

class BlockParticle(Particle):
    @override
    def __init__(self, particle_manager, location: Location, sprite: Surface | None) -> None:
        size = Vector2(0.125, 0.125)
        self.life_span = random.uniform(0.25, 0.5)
        time = self.life_span
        spread = 0.5
        location.move(random.uniform(-spread, spread), random.uniform(-spread, spread))
        location.rotation = 0
        if sprite == None:
            raise ValueError("Sprite shouldn't be None for block particles!")
        pixel_sprite = pygame.Surface((1, 1))
        color = sprite.get_at((random.randint(0, sprite.get_width() - 1),random.randint(0, sprite.get_height() - 1)))
        pixel_sprite.fill(color)
        pixel_sprite = pixel_sprite.convert_alpha()
        self.velocity: Vector2 = Vector2(random.uniform(-0.5, 0.5), 0.5)
        super().__init__(particle_manager, location, size, pixel_sprite, time)

    @override
    def tick(self):
        self.location.move(self.velocity.x * config.delta_time, self.velocity.y * config.delta_time)
        self.velocity.y -= 5 * config.delta_time
        self.alpha = 1 - (self.life_span - self.time) / self.life_span

        return super().tick()

class ParticleManager():
    def __init__(self) -> None:
        self.particles: list[Particle] = []
        self.particles_to_remove: list[Particle] = []

    def emit(self, particle_type: ParticleType, location: Location, count: int, sprite: Surface | None = None):
        for i in range(count):
            if particle_type == ParticleType.EXPLOSION:
                self.particles.append(ExplosionParticle(self, location.clone()))
            elif particle_type == ParticleType.BLOCK:
                self.particles.append(BlockParticle(self, location.clone(), sprite = sprite))

    def remove(self, particle):
        self.particles_to_remove.append(particle)

    def render(self):
        for particle in self.particles:
            location = particle.location
            size = particle.size
            camera = game_data.camera
            screen_position = camera.world_to_screen_point(location.position)
            screen_size_x = camera.world_to_screen_size(size.x)
            screen_size_y = camera.world_to_screen_size(size.y)
            sized_sprite = pygame.transform.scale(particle.sprite, (screen_size_x, screen_size_y))
            rect = pygame.Rect(screen_position.x - screen_size_x / 2, screen_position.y - screen_size_y / 2, screen_size_x, screen_size_y)
            rotated_sprite = pygame.transform.rotate(sized_sprite, location.rotation)
            rotated_sprite.set_alpha(round(particle.alpha * 255))
            rotated_rect = rotated_sprite.get_rect(center=rect.center)
            game_data.renderer.particles.append(SpriteData(rotated_sprite, rotated_rect, z = -1))

    def tick(self):
        for particle in self.particles_to_remove:
            self.particles.remove(particle)
        self.particles_to_remove = []

        for particle in self.particles:
            particle.tick()
