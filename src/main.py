import pygame
from location import Location
import render
from camera import Camera
from world import World
from material import *
from position import Position

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

# Game world
world = World(CHUNK_SIZE)
# Game camera
camera = Camera(screen, Location(world, Position(0, 8)), CAMERA_SIZE)
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
    render.render_world(camera, material_data, world, BLOCK_SIZE)
    camera.location.move(0, -0.05)
    world.tick()

    pygame.display.flip()

    clock.tick(FPS)
    if DEBUG:
        print(clock.get_fps())

pygame.quit()