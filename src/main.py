import pygame
import pymunk.pygame_util
from location import Location
from physics import PhysicsManager
import physics
import render
from camera import Camera
from world import World
from material import *
from pygame import Vector2
import variables
import pymunk
import math


DEBUG = True

FPS = 60
WIDTH, HEIGHT = 700,1300
CHUNK_SIZE = (16, 9)
BLOCK_SIZE = 1
CAMERA_SIZE = 16


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

# Physics Manager
physics_manager = PhysicsManager()

# Load sprites
variables.load_sprites()

# Game camera
variables.camera = Camera(screen, Location(None, Vector2(0, 0)), CAMERA_SIZE)
# Game world
world = World(CHUNK_SIZE)

# Set world of camera
# We have to set this after because the world has to be created after the camera
variables.camera.location.world = world

draw_options = pymunk.pygame_util.DrawOptions(screen)
draw_options.transform = pymunk.Transform(
    a=1, b=0, c=0, d=-1, tx=WIDTH / 2, ty=HEIGHT / 2
)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    # RENDER
    render.render_world(variables.camera, world, BLOCK_SIZE)
    #physics.physicsManager.space.debug_draw(draw_options)
    world.tick()

    
    variables.camera.move_towards(world.pickaxe.location.position.y)
    
    pygame.display.flip()

    clock.tick(FPS)
    if DEBUG:
        print(clock.get_fps())

pygame.quit()