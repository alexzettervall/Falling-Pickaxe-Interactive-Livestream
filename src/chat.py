from __future__ import annotations
from queue import Queue
import time
from typing import TYPE_CHECKING
import threading

import game_data
from text import AlignmentType, render_text
if TYPE_CHECKING:
    from world import World

class Chat():
    def __init__(self, world: World) -> None:
        self.world: World = world
        self.chat_message_queue: Queue[tuple[str, str]] = Queue()
        self._displayed_messages: list[tuple[str, float]] = []

    def send_chat_messages(self, chat_messages: list[tuple[str, str]]):
        for chat_message in chat_messages:
            self.send_chat_message(chat_message)

    def send_chat_message(self, chat_message: tuple[str, str]):
        self.chat_message_queue.put(chat_message)

    # Execute one message per call
    def _execute_messages(self):
        if self.chat_message_queue.empty():
            return
        chat_message = self.chat_message_queue.get()
        
        user: str = chat_message[0]
        message: str = chat_message[1].lower()
        if "tnt" in message:
            self.world.spawn_tnt(user)
        elif "avalanche" in message:
            self.world.spawn_avalanche(user)
        elif "fast" in message:
            threading.Thread(target = self.world.speed_fast, args = [user]).start()
        elif "slow" in message:
            threading.Thread(target = self.world.speed_slow, args = [user]).start()
        elif "big" in message:
            threading.Thread(target = self.world.size_big, args = [user]).start()
        elif "small" in message:
            threading.Thread(target = self.world.size_small, args = [user]).start()
        elif "wood" in message:
            self.world.set_pickaxe_type(user, "wood")
        elif "stone" in message:
            self.world.set_pickaxe_type(user, "stone")
        elif "copper" in message:
            self.world.set_pickaxe_type(user, "copper")
        elif "iron" in message:
            self.world.set_pickaxe_type(user, "iron")
        elif "gold" in message:
            self.world.set_pickaxe_type(user, "gold")
        elif "diamond" in message:
            self.world.set_pickaxe_type(user, "diamond")
        elif "netherite" in message:
            self.world.set_pickaxe_type(user, "netherite")
        
    def add_displayed_message(self, message: str):
        self._displayed_messages.append((message, time.time()))

    def _render(self):
        config = game_data.config
        text = ""
        messages: int = 0
        max_displayed_messages = config.chat_max_displayed_messages
        for i in range(len(self._displayed_messages) - 1, -1, -1):
            display_message = self._displayed_messages[i]
            text += display_message[0] + '\n'
            messages += 1
            if messages >= max_displayed_messages:
                break
        render_text(game_data.FONTS[config.chat_font], text, config.chat_position, config.chat_alignment_type, config.chat_color, True, lines_go_down = False)
        
    def _update_displayed_messages(self):
        to_remove = []
        for display_message in self._displayed_messages:
            if time.time() - display_message[1] > game_data.config.chat_message_time:
                to_remove.append(display_message)
        for remove in to_remove:
            self._displayed_messages.remove(remove)

    def tick(self):
        self._execute_messages()
        self._update_displayed_messages()
        self._render()
