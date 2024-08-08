import sys
import pygame

from settings import Settings
from ship import Ship

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init() # Khởi tạo tất cả các mô-đun Pygame.
        self.clock = pygame.time.Clock() # Tạo một đối tượng đồng hồ để kiểm soát tốc độ khung hình.
        self.settings = Settings()  # Tạo một đối tượng Settings để lưu trữ các cài đặt trò chơi.

        # Tạo một cửa sổ hiển thị với kích thước lấy từ cài đặt.
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion") # Đặt tiêu đề cho cửa sổ trò chơi.

        self.ship = Ship(self) # Tạo một đối tượng tàu và truyền tham chiếu của trò chơi vào đó.

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()  # Thoát trò chơi nếu sự kiện QUIT được kích hoạt.

            #Redraw the screen during each pass through the loop.
            self.screen.fill(self.settings.bg_color) # Đổ màu nền lên màn hình.
            self.ship.blitme() # Vẽ tàu ở vị trí hiện tại của nó.

            # Make the most recently drawn screen visible.
            pygame.display.flip() # Cập nhật màn hình để hiển thị các thay đổi vừa thực hiện.
            self.clock.tick(60) # Giới hạn tốc độ khung hình của trò chơi ở 60 FPS.


if __name__ == '__main__':
    # Make a game instance (đối tượng), and run the game.
    ai = AlienInvasion()
    ai.run_game()