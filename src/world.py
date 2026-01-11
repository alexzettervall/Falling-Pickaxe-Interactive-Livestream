from chunk import Chunk
from block import Block
from entity import Entity
from material import Material
from position import Position
from location import Location

class World:
    def __init__(self, chunk_size: tuple[int, int]):
        self.chunk_size = chunk_size
        self.chunks: list[Chunk] = []
        self.chunks.append(Chunk(Location(self, Position(0, 0)), chunk_size))
        self.entities: list[Entity] = []

        self.entities.append(Entity(Location(self, Position(0, 15))))

        block = self.get_block_at_position(Position(0, 0))
        if block != None:
            block.material = Material.BEDROCK

    def tick(self):
        for entity in self.entities:
            entity.tick()

    def get_block_at_position(self, position: Position, block_size: float = 1) -> Block | None:
        for chunk in self.chunks:
            intersects_x = abs(position.x - chunk.location.position.x) <= self.chunk_size[0] / 2
            intersects_y = abs(position.y - chunk.location.position.x) <= self.chunk_size[1] / 2
            if intersects_x and intersects_y:
                return chunk.get_block_at_position(position, block_size)
        
        return None

    