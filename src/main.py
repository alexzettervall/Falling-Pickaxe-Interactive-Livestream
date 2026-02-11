from multiprocessing import Queue, Process
from console import Console, init_console
import sql


def init():
    sql.init_db()
    import pygame
    pygame.init()
    pygame.font.init()
    pygame.mixer.init(frequency=41000)
    pygame.mixer.set_num_channels(1000)
    pygame.display.set_mode((0, 1000))
    import game_data
    from location import Location
    from physics import PhysicsManager
    from camera import Camera
    from world import World
    from pygame import Vector2
    import threading
    import youtube
    from render import Renderer
    import os

    # Start listening to chat messages
    if game_data.config.listen_to_stream:
        def listen_to_chat():
            youtube.init(game_data.config.stream_url)
        threading.Thread(target=listen_to_chat, daemon=True).start()

    screen = pygame.display.set_mode((game_data.config.screen_width, game_data.config.screen_height))
    clock = pygame.time.Clock()
    running = True

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

    game_data.renderer = Renderer(world)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")

        
        game_data.camera.move_towards(world.pickaxe.location.position.y - 1)
        world.tick()

        # Send livestream messages to the world chat
        world.chat.send_chat_messages(youtube.chat_messages)
        youtube.chat_messages = []

        # Sent console messages to the world chat
        if not from_console.empty():
            msg = from_console.get()
            world.chat.send_chat_message(msg)
        
        game_data.renderer.tick()

        pygame.display.flip()

        clock.tick(game_data.config.fps)
        pygame.display.set_caption(str(clock.get_fps()))


    pygame.quit()
    
if __name__ == '__main__':
    init()