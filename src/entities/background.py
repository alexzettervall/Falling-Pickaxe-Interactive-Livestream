
from pygame import Rect, Surface
import game_data
import pygame


class Background():
    def __init__(self) -> None:
        self.sprite = game_data.sprite_background
        self.scaled_sprite: Surface | None = None
        self.rect: Rect | None = None
        self._rescale()

    def _rescale(self):
        screen_w, screen_h = game_data.SCREEN_WIDTH, game_data.SCREEN_HEIGHT
        sprite_w, sprite_h = self.sprite.get_size()
        scale = max(screen_w / sprite_w, screen_h / sprite_h)

        new_w = int(sprite_w * scale)
        new_h = int(sprite_h * scale)

        self.scaled_sprite = pygame.transform.smoothscale(
            self.sprite, (new_w, new_h)
        )

        self.rect = self.scaled_sprite.get_rect(
            center = (screen_w // 2, screen_h // 2)
        )

    def render(self):
        if self.scaled_sprite == None or self.rect == None:
            return
        game_data.camera.surface.blit(self.scaled_sprite, self.rect)

    