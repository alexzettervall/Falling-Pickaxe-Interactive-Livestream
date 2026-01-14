from pygame.mixer import Sound

class SoundData():
    def __init__(self, sounds: list[Sound], volume: float) -> None:
        self.sounds: list[Sound] = sounds
        self.volume: float = volume