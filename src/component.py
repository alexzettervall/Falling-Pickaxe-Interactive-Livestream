class Component():
    def __init__(self, entity) -> None:
        from entity import Entity
        self.entity: Entity = entity

    def tick(self):
        pass

    def on_remove(self):
        pass