from pygame import Vector2


class Config():
    def __init__(self, 
                 stream_url: str,
                 listen_to_stream: bool,
                 screen_width: int, 
                 screen_height: int, 
                 chunk_size: tuple[int, int], 
                 camera_size: int, 
                 fps: float,
                 debug: bool, 
                 delta_time: float, 
                 physics_scale: float, 
                 render_distance: float, 
                 tnt_fuse_time: float, 
                 tnt_flash_interval: float, 
                 tnt_radius: float,
                 tnt_damage: float,
                 block_size: Vector2, 
                 pickaxe_break_delay: float,
                 normal_speed: float,
                 fast_speed: float,
                 slow_speed: float,
                 speed_change_duration: float
    ) -> None:
        self.stream_url = stream_url
        self.listen_to_stream = listen_to_stream
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.chunk_size = chunk_size
        self.camera_size = camera_size
        self.fps = fps
        self.debug = debug
        self.delta_time = delta_time
        self.physics_scale = physics_scale
        self.render_distance = render_distance
        self.tnt_fuse_time = tnt_fuse_time
        self.tnt_flash_interval = tnt_flash_interval
        self.tnt_radius = tnt_radius
        self.tnt_damage = tnt_damage
        self.block_size = block_size
        self.pickaxe_break_delay = pickaxe_break_delay
        self.normal_speed = normal_speed
        self.fast_speed = fast_speed
        self.slow_speed = slow_speed
        self.speed_change_duration = speed_change_duration

