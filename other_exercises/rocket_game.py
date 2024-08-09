import sys #Thư viện quản lý ops
import pygame

from rocket import Rocket
from settings import Settings
from bullet import Bullet
class RocketGame:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()  # Khởi tạo tất cả các mô-đun Pygame.
        self.clock = pygame.time.Clock()  # Tạo một đối tượng đồng hồ để kiểm soát tốc độ khung hình.
        self.settings = Settings()  # Tạo một đối tượng Settings để lưu trữ các cài đặt trò chơi.

        # Tạo một cửa sổ hiển thị với kích thước lấy từ cài đặt.
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption("Alien Invasion")  # Đặt tiêu đề cho cửa sổ trò chơi.

        self.rocket = Rocket(self)  # Tạo một đối tượng tàu và truyền tham chiếu của trò chơi vào đó.
        self.bullets = pygame.sprite.Group()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events.
            self._check_events()
            #Chuyển động ship qua lại tùy thuộc vào bàn phím K_RIGHT hay K_LEFT
            self.rocket.update()
            self._update_bullets()
            # Redraw the screen during each pass through the loop in _check_events() method.
            self._update_screen()
            self.clock.tick(60) # Giới hạn tốc độ khung hình của trò chơi ở 60 FPS.



    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit() # Thoát trò chơi nếu sự kiện QUIT được kích hoạt.
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill((230, 230, 230))  # Đổ màu nền lên màn hình.
        self.rocket.blitme()  # Vẽ tàu ở vị trí hiện tại của nó.

        # Update bullet to the screen.
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # Make the most recently drawn screen visible.
        pygame.display.flip()  # Cập nhật màn hình để hiển thị các thay đổi vừa thực hiện.

    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.rocket.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.rocket.moving_left = True
        elif event.key == pygame.K_UP:
            self.rocket.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.rocket.moving_down = True
        #press Q/q to quit game
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        else:
            print("This is not a function key",event.key)

    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.rocket.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.rocket.moving_left = False
        elif event.key == pygame.K_UP:
            self.rocket.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.rocket.moving_down = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.right >= self.settings.screen_width :
                self.bullets.remove(bullet)
        # print(len(self.bullets))#Show how many bullet is currently exist in the game.


if __name__ == '__main__':
    # Make a game instance (đối tượng), and run the game.
    ai = RocketGame()
    ai.run_game()