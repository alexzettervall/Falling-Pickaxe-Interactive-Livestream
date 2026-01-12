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

        self.add_entity(TNT(Location(self, Vector2(0, 15))))

        block = self.get_block_at_position(Vector2(0, 0))
        if block != None:
            block.material = Material.BEDROCK

    def tick(self):
        global tick
        tick += 1
        if tick % 100 == 0:
            self.add_entity(TNT(Location(self, Vector2(random.randint(-10, 10), 15))))

        physics.physicsManager.tick()
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
        self.entities.remove(entity)

    