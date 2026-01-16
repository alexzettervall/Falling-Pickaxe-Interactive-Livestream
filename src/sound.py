import random
from pygame.mixer import Sound
import pygame
import time

from game_data import SOUND_DATA
from sound_data import SoundData

class SoundManager():
    def __init__(self) -> None:
        self.sound_last_play_time: dict[str, float] = {}
    
    def play_sound(self, sound_name: str):
        sound_data: SoundData = SOUND_DATA[sound_name]

        last_play_time: float = 0.0
        if sound_name in self.sound_last_play_time:
            last_play_time = self.sound_last_play_time[sound_name]
        if time.time() - last_play_time < 1 / sound_data.max_play_frequency:
            return
        self.sound_last_play_time[sound_name] = time.time()

        sound = sound_data.sounds[random.randint(0, len(sound_data.sounds) - 1)]
        sound.set_volume(sound_data.volume)
        sound.play()
    
    