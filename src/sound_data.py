from pygame.mixer import Sound

class SoundData():
    def __init__(self, sounds: list[Sound], volume: float, max_play_frequency: float) -> None:
        self.sounds: list[Sound] = sounds
        self.volume: float = volume
        self.max_play_frequency: float = max_play_frequency