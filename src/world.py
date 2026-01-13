from math import ceil
import random
from chunk import Chunk
from block import Block
from components.rigidbody import RigidBody
from entities.pickaxe import Pickaxe
from entities.tnt import TNT
from entity import Entity
from material import Material
from pygame import Vector2
from location import Location
from particles.particles import ParticleManager, ParticleType
import physics
import random
import variables
tick = 0
class World:
    def __init__(self, chunk_size: tuple[int, int]):
        self.particle_manager = ParticleManager()
        self.chunk_size = chunk_size
        self.chunks: list[Chunk] = []
        self.chunks.append(Chunk(Location(self, Vector2(0, 0)), chunk_size))
        self.entities: list[Entity] = []
        self.entities_to_remove: list[Entity] = []
        self.chunks_to_remove: list[Chunk] = []

        self.pickaxe = self.add_entity(Pickaxe(Location(self, Vector2(0, 10))))


    def tick(self):
        global tick
        tick += 1
        if tick % 100 == 0:
            tnt = self.add_entity(TNT(Location(self, Vector2(self.pickaxe.location.position.x, self.pickaxe.location.position.y + 3))))
            rb = tnt.get_component(RigidBody)
            if rb != None:
                rb.body.angle = random.uniform(0, 6.3)

        for entity in self.entities_to_remove:
            self.entities.remove(entity)
        for chunk in self.chunks_to_remove:
            self.chunks.remove(chunk)

        self.entities_to_remove = []
        self.chunks_to_remove = []

        physics.physicsManager.tick()
        self.load_chunks()
        self.unload_chunks()
        for chunk in self.chunks:
            chunk.tick()
        for entity in self.entities:
            entity.tick()

        self.particle_manager.tick()
        self.particle_manager.render()

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
    
    def add_entity(self, entity: Entity):
        self.entities.append(entity)
        return entity

    def remove_entity(self, entity: Entity):
        self.entities_to_remove.append(entity)

    def get_surounding_blocks(self, location: Location) -> list[Block]:
        # Return all blocks in surrounding chunks
        chunk = self.get_chunk_at_position(location.position)
        top = self.get_chunk_at_position(Vector2(location.position.x, location.position.y + self.chunk_size[1] + 0.1))
        bottom = self.get_chunk_at_position(Vector2(location.position.x, location.position.y - self.chunk_size[1] - 0.1))
        blocks = []
        if chunk != None:
            blocks.extend(chunk.blocks)
        if top != None:
            blocks.extend(top.blocks)
        if bottom != None:
            blocks.extend(bottom.blocks)
        return blocks
    
    def create_explosion(self, location: Location, size: float, strength: float):
        blocks = self.get_surounding_blocks(location)
        for block in blocks:
            dist = location.position.distance_to(block.location.position)
            if dist < size:
                damage = strength - strength * (dist / size)
                block.damage(damage)

    def load_chunks(self):
        location: Location = variables.camera.location
        if not isinstance(location, Location):
            return
        min: int = round((location.position.y - variables.RENDER_DISTANCE) / self.chunk_size[1])
        max: int = round(location.position.y / self.chunk_size[1])
        for i in range(min, max + 1, 1):
            chunk = self.get_chunk_at_position(Vector2(0, i * self.chunk_size[1]))
            if chunk == None:
                self.chunks.append(Chunk(Location(self, Vector2(0, i * self.chunk_size[1])), self.chunk_size))


    def unload_chunks(self):
        location: Location = self.pickaxe.location
        for chunk in self.chunks:
            dist = location.position.distance_to(chunk.location.position)
            if dist > variables.RENDER_DISTANCE and chunk.location.position.y > location.position.y:
                chunk.remove()

    