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
from multiprocessing import Queue, Process, freeze_support
from console import Console, init_console


def init():
    # Start listening to chat messages
    if game_data.config.listen_to_stream:
        def listen_to_chat():
            youtube.init(game_data.config.stream_url)
        threading.Thread(target=listen_to_chat, daemon=True).start()

    pygame.init()
    pygame.font.init()
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

    # Start the console on a different process
    to_console: Queue = Queue()
    from_console: Queue = Queue()
    console = Process(target = init_console, args = (to_console, from_console), daemon = True)
    console.start()

    font_name = "arial"
    #font = pygame.font.SysFont(font_name, 300)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")

        # RENDER
        render.render_world(game_data.camera, world)
        world.tick()

        # Send livestream messages to the world chat
        world.chat.send_chat_messages(youtube.chat_messages)
        youtube.chat_messages = []

        # Sent console messages to the world chat
        if not from_console.empty():
            msg = from_console.get()
            world.chat.send_chat_message(msg)

        #test = font.render("test", False, "white")
        #print(test)
        #game_data.camera.surface.blit(test, Rect(0, 0, 1000, 1).center)
        
        game_data.camera.move_towards(world.pickaxe.location.position.y)
        
        pygame.display.flip()

        clock.tick(game_data.config.fps)
        pygame.display.set_caption(str(clock.get_fps()))

    pygame.quit()
    
if __name__ == '__main__':
    init()