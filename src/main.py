import pygame
from location import Location
from physics import PhysicsManager
import render
from camera import Camera
from world import World
from material import *
from pygame import Vector2
import variables
import pymunk


DEBUG = True

FPS = 60
WIDTH, HEIGHT = 720, 1280
CHUNK_SIZE = (16, 16)
BLOCK_SIZE = 1
CAMERA_SIZE = 18


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

# Physics Manager
physics_manager = PhysicsManager()

# Load sprites
variables.load_sprites()

# Game camera
variables.camera = Camera(screen, Location(None, Vector2(0, 8)), CAMERA_SIZE)
# Game world
world = World(CHUNK_SIZE)

# Set world of camera
# We have to set this after because the world has to be created after the camera
variables.camera.location.world = world

# Material Data
material_data: dict[Material, MaterialData]  = dict()

material_data[Material.BEDROCK] = MaterialData(pygame.image.load("..//sprites//blocks//bedrock.png"))
material_data[Material.GRASS] = MaterialData(pygame.image.load("..//sprites//blocks//grass.png"))
material_data[Material.STONE] = MaterialData(pygame.image.load("..//sprites//blocks//stone.png"))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    # RENDER
    render.render_world(variables.camera, material_data, world, BLOCK_SIZE)
    world.tick()

    pygame.display.flip()

    clock.tick(FPS)
    if DEBUG:
        print(clock.get_fps())

pygame.quit()