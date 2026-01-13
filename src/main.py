import pygame
from location import Location
from physics import PhysicsManager
import physics
import render
from camera import Camera
from world import World
from material import *
from pygame import Vector2
import variables

FPS = 60
CHUNK_SIZE = (16, 9)
CAMERA_SIZE = 16


pygame.init()
screen = pygame.display.set_mode((variables.SCREEN_WIDTH, variables.SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

# Physics Manager
physics_manager = PhysicsManager()

# Load sprites
variables.load_sprites()

# Game world
world = World(CHUNK_SIZE)
# Game camera
variables.camera = Camera(screen, Location(world, Vector2(0, 0)), CAMERA_SIZE)

# Set world of camera
# We have to set this after because the world has to be created after the camera
variables.camera.location.world = world

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    # RENDER
    render.render_world(variables.camera, world)
    world.tick()

    
    variables.camera.move_towards(world.pickaxe.location.position.y)
    
    pygame.display.flip()

    clock.tick(FPS)
    if variables.DEBUG:
        print(clock.get_fps())

pygame.quit()