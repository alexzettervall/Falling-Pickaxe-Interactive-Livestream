from pygame import Vector2

from text import AlignmentType
from typing import Any


class Config():
    def __init__(self,
                 screen_width: int, 
                 screen_height: int, 
                 chunk_size: tuple[int, int], 
                 camera_size: int, 
                 fps: float,
                 debug: bool, 
                 delta_time: float, 
                 render_distance: float, 

                 tnt_fuse_time: float, 
                 tnt_flash_interval: float, 
                 tnt_radius: float,
                 tnt_damage: float,

                 nuke_radius: float,
                 nuke_damage: float,
                 nuke_xp: float,

                 block_size: Vector2, 
                 default_break_speed: float,
                 normal_speed: float,
                 fast_speed: float,
                 slow_speed: float,
                 speed_change_duration: float,
                 normal_pickaxe_size: float,
                 big_pickaxe_size: float,
                 small_pickaxe_size: float,
                 pickaxe_size_change_duration: float,

                 clone_lifetime: float,
                 clone_y_offset: float,

                 chat_message_time: float,
                 chat_color: str,
                 chat_font: str,
                 chat_max_displayed_messages: int,
                 chat_position: tuple[int, int],
                 chat_alignment_type: AlignmentType,

                 auto_commands: dict[str, Any],

                 physics: dict[str, Any]
    ) -> None:
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.chunk_size = chunk_size
        self.camera_size = camera_size
        self.fps = fps
        self.debug = debug
        self.delta_time = delta_time
        self.render_distance = render_distance

        self.tnt_fuse_time = tnt_fuse_time
        self.tnt_flash_interval = tnt_flash_interval
        self.tnt_radius = tnt_radius
        self.tnt_damage = tnt_damage

        self.nuke_radius = nuke_radius
        self.nuke_damage = nuke_damage
        self.nuke_xp = nuke_xp

        self.block_size = block_size
        self.default_break_speed = default_break_speed
        self.normal_speed = normal_speed
        self.fast_speed = fast_speed
        self.slow_speed = slow_speed
        self.speed_change_duration = speed_change_duration
        self.normal_pickaxe_size = normal_pickaxe_size
        self.big_pickaxe_size = big_pickaxe_size
        self.small_pickaxe_size = small_pickaxe_size
        self.pickaxe_size_changee_duration = pickaxe_size_change_duration

        self.clone_lifetime = clone_lifetime
        self.clone_y_offset = clone_y_offset

        self.chat_message_time = chat_message_time
        self.chat_color = chat_color
        self.chat_font = chat_font
        self.chat_max_displayed_messages = chat_max_displayed_messages
        self.chat_position = chat_position
        self.chat_alignment_type = chat_alignment_type
        self.auto_commands = auto_commands
        self.physics = physics

