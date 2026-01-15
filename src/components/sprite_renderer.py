from typing import override

import pygame
from camera import Camera
from component import Component
import game_data
from render import SpriteData


class SpriteRenderer(Component):
    def __init__(self, entity, camera: Camera | None, sprite) -> None:
        super().__init__(entity)

        self.sprite = sprite
        self.camera: Camera | None = camera
        self.alpha: float = 1.0

    @override
    def tick(self):
        self.render(self.camera, self.sprite)

    def render(self, camera: Camera | None, sprite):
        if camera == None:
            camera = game_data.camera
        if camera == None:
            return
        
        location = self.entity.location
        size = self.entity.size
        screen_position = camera.world_to_screen_point(location.position)
        screen_size_x = camera.world_to_screen_size(size.x)
        screen_size_y = camera.world_to_screen_size(size.y)
        sized_sprite = pygame.transform.scale(sprite, (screen_size_x, screen_size_y))
        rect = pygame.Rect(screen_position.x - screen_size_x / 2, screen_position.y - screen_size_y / 2, screen_size_x, screen_size_y)
        rotated_sprite = pygame.transform.rotate(sized_sprite, location.rotation)
        rotated_sprite.set_alpha(round(self.alpha * 255))
        rotated_rect = rotated_sprite.get_rect(center=rect.center)
        game_data.renderer.sprites.append(SpriteData(rotated_sprite, rotated_rect, z = -1))
