import pymunk
from pymunk import Body, Shape

from variables import DELTA_TIME

class PhysicsManager():
    def __init__(self) -> None:
        self.space = pymunk.Space()
        self.space.gravity = (0, -40)

    def add_body(self, body: Body):
        self.space.add(body)
        for shape in body.shapes:
            self.space.add(shape)

    def remove_body(self, body: Body):
        self.space.remove(body)
        for shape in body.shapes:
            self.space.remove(shape)

    def tick(self):
        self.space.step(DELTA_TIME)



physicsManager = PhysicsManager()

    


