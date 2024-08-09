class Settings:
    """A class to store all settings for Alien Invasion."""
    def __init__(self):
        """Initialize the game's settings."""
        # Screen settings
        self.screen_width = 1200  #Chiều rộng của màn hình.
        self.screen_height = 800 # Chiều cao của màn hình.
        self.bg_color = (230, 230, 230)  # Màu nền của màn hình (màu xám nhạt).
        self.ship_speed = 3

        # Bullet settings
        self.bullet_speed = 5
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3