from math import ceil
import math
import time
from typing import TypeVar
from numpy import isin
from chat import Chat
from chunk import Chunk
from data import config
from entities.block import BlockBreaker
from components.health import Health
from entities.background import Background
from entities.block import Block
from components.rigidbody import RigidBody
from entities.nuke import Nuke
from entities.pickaxe import Pickaxe
from entities.tnt import TNT
from entities.entity import Entity
from pygame import Vector2
from location import Location
from particles.particles import ParticleManager, ParticleType
import physics
import random
import game_data
from pickaxe_size import PickaxeSize
from sound import SoundManager
from time_speed import TimeSpeed
from copy import deepcopy
tick = 0

E = TypeVar("E", bound = Entity)

class World:
    def __init__(self, chunk_size: tuple[int, int]):
        self.sound_manager: SoundManager = SoundManager()
        self.physics_manager: physics.PhysicsManager = physics.PhysicsManager(self)
        self.particle_manager = ParticleManager()
        self.chunk_size = chunk_size
        self.chunks: list[Chunk] = []
        self.chunks.append(Chunk(Location(self, Vector2(0, chunk_size[1])), chunk_size))
        self.chunks.append(Chunk(Location(self, Vector2(0, 0)), chunk_size))
        self.entities: list[Entity] = []
        self.entities_to_remove: list[Entity] = []
        self.chunks_to_remove: list[Chunk] = []
        self.pickaxe: Pickaxe = self.add_entity(Pickaxe(Location(self, Vector2(0, 10))))
        self.background = Background()
        self.chat = Chat(self)
        self.time_speed = TimeSpeed.NORMAL
        self.xp: float = 0.0


    def tick(self):
        global tick
        if self.xp >= game_data.config.nuke_xp:
            self.spawn_nuke()
            self.xp = 0
        for entity in self.entities_to_remove:
            if entity in self.entities:
                self.entities.remove(entity)
            else:
                for chunk in self.chunks:
                    if entity in chunk.blocks:
                        chunk.blocks_to_remove.append(entity)
        for chunk in self.chunks_to_remove:
            self.chunks.remove(chunk)

        self.entities_to_remove = []
        self.chunks_to_remove = []

        self.physics_manager.tick()
        self.load_chunks()
        self.unload_chunks()
        for chunk in self.chunks:
            chunk.tick()
        for entity in self.entities:
            entity.tick()

        self.particle_manager.tick()
        self.particle_manager.render()
        game_data.DISPLAY.tick(self)
        self.chat.tick()
        self.update_delta_time()
        self.sound_manager.tick()

    def update_delta_time(self):
        config = game_data.config
        normal_delta_time = 1 / config.fps
        if self.time_speed == TimeSpeed.NORMAL:
            config.delta_time = normal_delta_time * config.normal_speed
        elif self.time_speed == TimeSpeed.FAST:
            config.delta_time = normal_delta_time * config.fast_speed
        elif self.time_speed == TimeSpeed.SLOW:
            config.delta_time = normal_delta_time * config.slow_speed

    def get_block_at_position(self, position: Vector2, block_size: float = 1) -> Block | None:
        chunk = self.get_chunk_at_position(position, block_size)
        if chunk == None:
            return None
        return chunk.get_block_at_position(position, block_size)
    
    def get_chunk_at_position(self, position: Vector2, block_size: float = 1):
        for chunk in self.chunks:
            intersects_x = abs(position.x - chunk.location.position.x) <= self.chunk_size[0] / 2
            intersects_y = abs(position.y - chunk.location.position.y) <= self.chunk_size[1] / 2
            if intersects_x and intersects_y:
                return chunk
        return None
    
    def add_entity(self, entity: E) -> E:
        self.entities.append(entity)
        return entity

    def remove_entity(self, entity: Entity):
        self.entities_to_remove.append(entity)

    def get_blocks_in_range(self, location: Location, range: float) -> list[Block]:
        blocks: list[Block] = []
        entities: list[Entity] = self.physics_manager.point_query((location.position.x, location.position.y), range)
        for entity in entities:
            if isinstance(entity, Block):
                blocks.append(entity)
        return blocks
    
    def create_explosion(self, location: Location, size: float, strength: float):
        blocks = self.get_blocks_in_range(location, size)
        for block in blocks:
            dist = location.position.distance_to(block.location.position)
            if dist < size:
                damage = strength / max(0.001, (dist ** 2))
                block_health = block.get_component(Health)
                if block_health == None:
                    continue
                block_health.damage(damage)
                block.dislodge()
                if isinstance(block, TNT):
                    block.fuse = random.uniform(0.5, 1)
        self.particle_manager.emit(ParticleType.EXPLOSION, location, 10)
        self.sound_manager.play_sound("explosion")

    def load_chunks(self):
        location: Location = game_data.camera.location
        if not isinstance(location, Location):
            return
        min: int = round((location.position.y - game_data.config.render_distance) / self.chunk_size[1])
        max: int = round(location.position.y / self.chunk_size[1])
        for i in range(max, min, -1):
            chunk = self.get_chunk_at_position(Vector2(0, i * self.chunk_size[1]))
            if chunk == None:
                self.chunks.append(Chunk(Location(self, Vector2(0, i * self.chunk_size[1])), self.chunk_size))


    def unload_chunks(self):
        location: Location = self.pickaxe.location
        for chunk in self.chunks:
            dist = location.position.distance_to(chunk.location.position)
            if dist > game_data.config.render_distance and chunk.location.position.y > location.position.y:
                chunk.remove()

    # Command implementations

    # World commands
    def spawn_nuke(self):
        nuke = self.add_entity(Nuke(location = Location(self, Vector2(self.pickaxe.location.position.x, self.pickaxe.location.position.y + 3))))
        nuke.ignite()

    # User commands
    def spawn_tnt(self, user: str):
        tnt = self.add_entity(TNT(chunk = None, location = Location(self, Vector2(self.pickaxe.location.position.x, self.pickaxe.location.position.y + 3)), user = user))
        tnt.ignite()
        self.chat.add_displayed_message(f"{user} spawned a tnt!")

    def spawn_avalanche(self, user: str):
        blocks = self.get_blocks_in_range(self.pickaxe.location.clone(), 8)
        for block in blocks:
            if block.material != "bedrock":
                block.dislodge()
        self.chat.add_displayed_message(f"{user} spawned a avalanche!")
        self.sound_manager.play_sound("avalanche")

    def speed_fast(self, user: str):
        if self.time_speed != TimeSpeed.NORMAL:
            return
        self.time_speed = TimeSpeed.FAST
        self.chat.add_displayed_message(f"{user} sped up time!")
        time.sleep(game_data.config.speed_change_duration)
        self.time_speed = TimeSpeed.NORMAL

    def speed_slow(self, user: str):
        if self.time_speed != TimeSpeed.NORMAL:
            return
        self.time_speed = TimeSpeed.SLOW
        self.chat.add_displayed_message(f"{user} slowed down time!")
        time.sleep(game_data.config.speed_change_duration)
        self.time_speed = TimeSpeed.NORMAL

    def size_big(self, user: str):
        if self.pickaxe.get_pickaxe_size() != PickaxeSize.NORMAL:
            return
        self.pickaxe.set_pickaxe_size(PickaxeSize.BIG)
        self.chat.add_displayed_message(f"{user} made the pickaxe big!")
        time.sleep(game_data.config.pickaxe_size_changee_duration)
        self.pickaxe.set_pickaxe_size(PickaxeSize.NORMAL)

    def size_small(self, user: str):
        if self.pickaxe.get_pickaxe_size() != PickaxeSize.NORMAL:
            return
        self.pickaxe.set_pickaxe_size(PickaxeSize.SMALL)
        self.chat.add_displayed_message(f"{user} made the pickaxe small!")
        time.sleep(game_data.config.pickaxe_size_changee_duration)
        self.pickaxe.set_pickaxe_size(PickaxeSize.NORMAL)

    def set_pickaxe_type(self, user: str, pickaxe_type: str):
        self.pickaxe.set_pickaxe_type(pickaxe_type)
        self.chat.add_displayed_message(f"{user} set pickaxe type to {pickaxe_type}!")

    def clone_pickaxe(self, user: str):
        location: Location = self.pickaxe.location.clone()
        location.position.y += game_data.config.clone_y_offset
        cloned_pickaxe = Pickaxe(location, user)
        cloned_pickaxe.set_pickaxe_type(self.pickaxe.get_pickaxe_type())
        cloned_pickaxe.set_pickaxe_size(self.pickaxe.get_pickaxe_size())
        self.add_entity(cloned_pickaxe)
        cloned_pickaxe.remove(time = game_data.config.clone_lifetime)
        self.chat.add_displayed_message(f"{user} cloned the pickaxe!")
        self.sound_manager.play_sound("clone")
