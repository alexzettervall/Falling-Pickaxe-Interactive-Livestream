from math import ceil
from pygame import Surface
from position import Position
from location import Location

class Camera:
    def __init__(self, surface: Surface, location: Location, size: float): # Size is the horizontal world distance from the left of the screen to the right of the screen.
        self.surface: Surface = surface
        self.location: Location = location
        self.size: float = size
    
    def screen_to_world_point(self, screen_position: Position) -> Position:
        width = self.surface.get_width()
        height = self.surface.get_height()
        conversion = width / self.size

        relative_pixel_x = screen_position.x - width / 2
        relative_pixel_y = screen_position.y - height / 2

        world_x = (relative_pixel_x / conversion) + self.location.position.x
        world_y = (-relative_pixel_y / conversion) + self.location.position.y

        return Position(world_x, world_y)
    
    def world_to_screen_point(self, position: Position) -> Position:
        width = self.surface.get_width()
        height = self.surface.get_height()
        conversion = width / self.size

        relative_pixel_x = (position.x - self.location.position.x) * conversion
        relative_pixel_y = (position.y - self.location.position.y) * conversion

        screen_x = relative_pixel_x + width / 2
        screen_y = -relative_pixel_y + height / 2
        return Position(screen_x, screen_y)


    def world_to_screen_size(self, size: float) -> int:
        return ceil(size * (self.surface.get_width() / self.size))
    
    def screen_to_world_size(self, screen_size: int) -> float:
        return screen_size * (self.size / self.surface.get_width())