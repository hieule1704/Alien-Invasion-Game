import sys #Thư viện quản lý ops
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init() # Khởi tạo tất cả các mô-đun Pygame.
        self.clock = pygame.time.Clock() # Tạo một đối tượng đồng hồ để kiểm soát tốc độ khung hình.
        self.settings = Settings()  # Tạo một đối tượng Settings để lưu trữ các cài đặt trò chơi.

        #Create an attribute to manage full screen or default screen mode
        self.screen_mode = False
        # Tạo một cửa sổ hiển thị với kích thước lấy từ cài đặt.
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))


        pygame.display.set_caption("Alien Invasion") # Đặt tiêu đề cho cửa sổ trò chơi.

        # Create an instance to store game statistics.
        self.stats = GameStats(self)

        self.ship = Ship(self) # Tạo một đối tượng tàu và truyền tham chiếu của trò chơi vào đó.
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events.
            self._check_events()
            #Chuyển động ship qua lại tùy thuộc vào bàn phím K_RIGHT hay K_LEFT
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
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
        self.screen.fill(self.settings.bg_color)  # Đổ màu nền lên màn hình.
        #Update bullet to the screen.
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()  # Vẽ tàu ở vị trí hiện tại của nó.
        self.aliens.draw(self.screen) #Create aliens into the screen

        # Make the most recently drawn screen visible.
        pygame.display.flip()  # Cập nhật màn hình để hiển thị các thay đổi vừa thực hiện.

    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        #press Q/q to quit game
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_F11:
            #Change screen mode
            self.screen_mode = not self.screen_mode
            if self.screen_mode:
                # Create a window with fullscreen mode.
                self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                self.settings.screen_width = self.screen.get_rect().width
                self.settings.screen_height = self.screen.get_rect().height
            else:
                # Back to default screen mode default value is (1200, 800).
                self.screen = pygame.display.set_mode((1200, 800))
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        else:
            print("This is not a function key",event.key)

    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)  # print(len(self.bullets))#Show how many bullet is currently exist in the game.

        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        # Create a new fleet if there is no fleet remain.
        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size #rect.size return a tuple value link this (x, y)

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position,  y_position):
        """Create an alien and place it in the fleet."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        #Drop
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        #Change direction 1 = right and -1 = left
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        # Decrement ships_left.
        self.stats.ships_left -= 1

        # Get rid of any remaining bullets and aliens.
        self.bullets.empty()
        self.aliens.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.center_ship()

        #Pause
        sleep(0.5)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break


if __name__ == '__main__':
    # Make a game instance (đối tượng), and run the game.
    ai = AlienInvasion()
    ai.run_game()