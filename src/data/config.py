from dataclasses import dataclass

from pygame import Vector2

from text import AlignmentType
from typing import Any

@dataclass(slots=True)
class PhysicsConfig:
    scale: float
    iterations: int
    gravity: float
    default_elasticity: float
    default_friction: float

@dataclass(slots=True)
class TNTConfig:
    fuse_time: float
    flash_interval: float
    radius: float
    damage: float

@dataclass(slots=True)
class Config:
    screen_width: int
    screen_height: int
    chunk_size: tuple[int, int]
    camera_size: int
    fps: float
    debug: bool
    delta_time: float
    render_distance: float
    
    tnt: TNTConfig
    
    nuke_radius: float
    nuke_damage: float
    nuke_xp: float
    
    block_size: Vector2
    default_break_speed: float
    normal_speed: float
    fast_speed: float
    slow_speed: float
    speed_change_duration: float
    normal_pickaxe_size: Vector2
    big_pickaxe_size: Vector2
    small_pickaxe_size: Vector2
    pickaxe_size_change_duration: float
    
    clone_lifetime: float
    clone_y_offset: float
    
    chat_message_time: float
    chat_color: Any
    chat_font: Any
    chat_max_displayed_messages: int
    chat_position: tuple[int, int]
    chat_alignment_type: AlignmentType
    auto_commands: list
    physics: PhysicsConfig
