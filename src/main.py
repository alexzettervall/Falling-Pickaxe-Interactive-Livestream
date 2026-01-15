import pygame
import selenium.webdriver
pygame.mixer.init(frequency=41000)
pygame.mixer.set_num_channels(1000)
from entities.tnt import TNT
import game_data
from location import Location
from physics import PhysicsManager
import render
from camera import Camera
from world import World
from material import *
from pygame import Vector2
import threading
import youtube

# Start listening to chat messages
if game_data.config.listen_to_stream:
    def listen_to_chat():
        youtube.init(game_data.config.stream_url)
    threading.Thread(target=listen_to_chat, daemon=True).start()

def test():
    import console
threading.Thread(target=test, daemon=True).start()


pygame.init()
screen = pygame.display.set_mode((game_data.config.screen_width, game_data.config.screen_height))
clock = pygame.time.Clock()
running = True

# Physics Manager
physics_manager = PhysicsManager()

# Load sprites
game_data.load_sprites()

# Game world
world = World(game_data.config.chunk_size)
# Game camera
game_data.camera = Camera(screen, Location(world, Vector2(0, 0)), game_data.config.camera_size)

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


    for msg in youtube.chat_messages:
        print(str(msg))
        if "tnt" in msg[1]:
            world.add_entity(TNT(Location(world, Vector2(world.pickaxe.location.position.x, world.pickaxe.location.position.y + 3))))
        youtube.chat_messages = []


    
    game_data.camera.move_towards(world.pickaxe.location.position.y)
    
    pygame.display.flip()

    clock.tick(game_data.config.fps)
    pygame.display.set_caption(str(clock.get_fps()))

pygame.quit()