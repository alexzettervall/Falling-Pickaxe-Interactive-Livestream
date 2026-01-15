from __future__ import annotations
import random
from typing import TYPE_CHECKING
from pygame import Vector2
from components.rigidbody import RigidBody
from entities.tnt import TNT
from location import Location
if TYPE_CHECKING:
    from world import World

class Chat():
    def __init__(self, world: World) -> None:
        self.world: World = world
        self.chat_messages: list[tuple[str, str]] = []

    def send_chat_messages(self, chat_messages: list[tuple[str, str]]):
        for chat_message in chat_messages:
            self.send_chat_message(chat_message)

    def send_chat_message(self, chat_message: tuple[str, str]):
        self.chat_messages.append(chat_message)

    def execute_messages(self):
        for chat_message in self.chat_messages:
            user: str = chat_message[0]
            message: str = chat_message[1].lower()
            if "tnt" in message:
                pickaxe = self.world.pickaxe
                tnt = self.world.add_entity(TNT(Location(self.world, Vector2(pickaxe.location.position.x, pickaxe.location.position.y + 3))))
                rb = tnt.get_component(RigidBody)
                if rb != None:
                    rb.rotate_degrees(random.uniform(0, 360))
        self.chat_messages = []