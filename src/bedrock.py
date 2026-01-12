from typing import override
from block import Block

class Bedrock(Block):
    def __init__(self, chunk, material, location):
        super().__init__(chunk, material, location)

    @override
    def damage(self, damage: float):
        pass