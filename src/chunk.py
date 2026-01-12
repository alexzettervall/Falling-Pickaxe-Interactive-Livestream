from block import Block
from material import Material
from location import Location
from pygame import Vector2

class Chunk:
    def __init__(self, location: Location, size: tuple[int, int]):
        self.size = size
        self.location = location # Chunk position is in the center of the chunk and blocks are generated around it
        self.blocks: list[Block] = self.generate_blocks(size)

    # Generate blocks and returns a list of lists containing them. 
    # The outer list contains each x segment of blocks.
    # Each segment contains a list of vertically alligned blocks.
    # Verticle blocks are ordered by y position. 0 = lowers, 1 = higher
    def generate_blocks(self, size: tuple[int, int]) -> list[Block]:
        blocks: list[Block] = []
        center_offset_x = -(size[0] - 1) / 2
        center_offset_y = -(size[1] - 1) / 2
        for x in range(size[0]):
            for y in range(size[1]):
                x_pos = x + center_offset_x + self.location.position.x
                y_pos = y + center_offset_y + self.location.position.y
                material = Material.STONE
                if y_pos > 0:
                    material = Material.GRASS
                blocks.append(Block(material, Location(self.location.world, Vector2(x_pos, y_pos))))
        return blocks
    
    def get_block_at_position(self, position: Vector2, block_size: float = 1) -> Block | None:
        for block in self.blocks:
            if block == None:
                continue
            intersects_x = abs(position.x - block.location.position.x) <= block_size / 2
            intersects_y = abs(position.y - block.location.position.y) <= block_size / 2
            if intersects_x and intersects_y:
                return block
                
        return None