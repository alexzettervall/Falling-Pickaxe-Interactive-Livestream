import pygame
pygame.mixer.init()
pygame.mixer.set_num_channels(1000)
from location import Location
from physics import PhysicsManager
import render
from camera import Camera
from world import World
from material import *
from pygame import Vector2
import game_data
FPS = 60
CHUNK_SIZE = (16, 9)
CAMERA_SIZE = 16


pygame.init()
screen = pygame.display.set_mode((game_data.SCREEN_WIDTH, game_data.SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

# Physics Manager
physics_manager = PhysicsManager()

# Load sprites
game_data.load_sprites()

# Game world
world = World(CHUNK_SIZE)
# Game camera
game_data.camera = Camera(screen, Location(world, Vector2(0, 0)), CAMERA_SIZE)

# Set world of camera
# We have to set this after because the world has to be created after the camera
game_data.camera.location.world = world

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    # RENDER
    render.render_world(game_data.camera, world)
    world.tick()

    
    game_data.camera.move_towards(world.pickaxe.location.position.y)
    
    pygame.display.flip()

    clock.tick(FPS)
    pygame.display.set_caption(str(clock.get_fps()))

pygame.quit()