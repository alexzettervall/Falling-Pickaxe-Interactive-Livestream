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
                 default_break_speed: float,
                 normal_speed: float,
                 fast_speed: float,
                 slow_speed: float,
                 speed_change_duration: float,
                 normal_pickaxe_size: float,
                 big_pickaxe_size: float,
                 small_pickaxe_size: float,
                 pickaxe_size_change_duration: float
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
        self.default_break_speed = default_break_speed
        self.normal_speed = normal_speed
        self.fast_speed = fast_speed
        self.slow_speed = slow_speed
        self.speed_change_duration = speed_change_duration
        self.normal_pickaxe_size = normal_pickaxe_size
        self.big_pickaxe_size = big_pickaxe_size
        self.small_pickaxe_size = small_pickaxe_size
        self.pickaxe_size_changee_duration = pickaxe_size_change_duration

