from pygame.mixer import Sound

class SoundData():
    def __init__(self, sounds: list[Sound], volume: float, max_play_frequency: float, queue_rate_limited_sounds: bool) -> None:
        self.sounds: list[Sound] = sounds
        self.volume: float = volume
        self.max_play_frequency: float = max_play_frequency
        self.queue_rate_limited_sounds: bool = queue_rate_limited_sounds