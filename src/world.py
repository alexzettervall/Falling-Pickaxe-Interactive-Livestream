from math import ceil
import random
from chunk import Chunk
from block import Block
from entities.tnt import TNT
from entity import Entity
from material import Material
from pygame import Vector2
from location import Location
import physics
tick = 0
class World:
    def __init__(self, chunk_size: tuple[int, int]):
        self.chunk_size = chunk_size
        self.chunks: list[Chunk] = []
        self.chunks.append(Chunk(Location(self, Vector2(0, 0)), chunk_size))
        self.entities: list[Entity] = []
        self.entities_to_remove: list[Entity] = []

        self.add_entity(TNT(Location(self, Vector2(0, 20))))

        block = self.get_block_at_position(Vector2(0, 0))
        if block != None:
            block.material = Material.BEDROCK

    def tick(self):
        global tick
        tick += 1
        if tick % 100 == 0:
            self.add_entity(TNT(Location(self, Vector2(random.randint(-80, 80) / 10, 20))))

        for entity in self.entities_to_remove:
            self.entities.remove(entity)
        self.entities_to_remove = []

        physics.physicsManager.tick()
        for chunk in self.chunks:
            chunk.tick()
        for entity in self.entities:
            entity.tick()

    def get_block_at_position(self, position: Vector2, block_size: float = 1) -> Block | None:
        for chunk in self.chunks:
            intersects_x = abs(position.x - chunk.location.position.x) <= self.chunk_size[0] / 2
            intersects_y = abs(position.y - chunk.location.position.x) <= self.chunk_size[1] / 2
            if intersects_x and intersects_y:
                return chunk.get_block_at_position(position, block_size)
        
        return None
    
    def add_entity(self, entity: Entity):
        self.entities.append(entity)

    def remove_entity(self, entity: Entity):
        self.entities_to_remove.append(entity)

    def get_blocks_in_range(self, location: Location, range: int) -> list[Block]:
        return self.chunks[0].blocks
    
    def create_explosion(self, location: Location, size: float, strength: float):
        blocks = self.get_blocks_in_range(location, ceil(size))
        for block in blocks:
            dist = location.position.distance_to(block.location.position)
            if dist < size:
                damage = strength - strength * (dist / size)
                block.damage(damage)

    