import sys #Thư viện quản lý ops
from time import sleep

import pygame
import pyodbc

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
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

        self.showing_top_scores = False  # Thêm biến trạng thái

        # Tạo một cửa sổ hiển thị với kích thước lấy từ cài đặt.
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))


        pygame.display.set_caption("Alien Invasion") # Đặt tiêu đề cho cửa sổ trò chơi.

        # Load sound effects
        self.bullet_sound = pygame.mixer.Sound('sounds/bullet.wav')
        self.hit_sound = pygame.mixer.Sound('sounds/hit.wav')

        # Create an instance to store game statistics,
        #   and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self) # Tạo một đối tượng tàu và truyền tham chiếu của trò chơi vào đó.
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # Start Alien Invasion in an inactive state.
        self.game_active = False

        self.player_name = ""  # Lưu tên người chơi
        self.name_input_active = False  # Trạng thái nhập tên

        # Khởi tạo nút "Play"
        self.play_button = Button(self, "Play")

        # Khởi tạo nút "Top Scores" và đặt vị trí cho nó
        self.top_scores_button = Button(self, "Top Scores")
        self.top_scores_button.rect.top = self.play_button.rect.bottom + 20
        self.top_scores_button.msg_image_rect.center = self.top_scores_button.rect.center

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events.
            self._check_events()
            #Check ship remain
            if self.game_active:
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
                # Lưu điểm trước khi thoát
                self.stats.save_score(self.player_name)
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if not self.showing_top_scores:
                    self._check_play_button(mouse_pos)
                    self._check_top_scores_button(mouse_pos)
                else:
                    self.showing_top_scores = False

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)  # Đổ màu nền lên màn hình.
        # Update bullet to the screen.
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()  # Vẽ tàu ở vị trí hiện tại của nó.
        self.aliens.draw(self.screen)  # Create aliens into the screen

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if self.showing_top_scores:
            self.show_top_scores_screen()
        elif not self.game_active:
            self.play_button.draw_button()
            self.top_scores_button.draw_button()

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
            self.stats.save_score(self.player_name)
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
            self.bullet_sound.play()  # Play bullet sound

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

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.hit_sound.play()  # Play hit sound
            self.sb.prep_score()
            self.sb.check_high_score()

        # Create a new fleet if there is no fleet remain.
        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width and one alien height.
        """Create the fleet of aliens if not already created."""
        if len(self.aliens) == 0:
            alien = Alien(self)
            alien_width, alien_height = alien.rect.size
            current_x, current_y = alien_width, alien_height

            while current_y < (self.settings.screen_height - 3 * alien_height):
                while current_x < (self.settings.screen_width - 2 * alien_width):
                    self._create_alien(current_x, current_y)
                    current_x += 2 * alien_width
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

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

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
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause
            sleep(0.5)
        else:
            self.stats.save_score(self.player_name)
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Bắt đầu nhập tên
            self.name_input_active = True
            self.player_name = ""  # Đặt lại tên người chơi
            self.get_player_name()

            # Reset the game settings.
            self.settings.initialize_dynamic_settings()

            #Reset the game statistics.
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            self.game_active = True

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_top_scores_button(self, mouse_pos):
        """Show the top 10 scores when the player clicks the Top Scores button."""
        button_clicked = self.top_scores_button.rect.collidepoint(mouse_pos)
        if button_clicked:
            self.showing_top_scores = True
            # Đoạn bên dưới sẽ hiển thị điểm số cao nhất trong cơ sở dữ liệu dưới màng hình console.
            # top_scores = self.get_top_scores()
            # for rank, (player_name, score) in enumerate(top_scores, start=1):
            #     print(f"{rank}. {player_name}: {score}")

    def get_player_name(self):
        """Hiển thị hộp thoại để người chơi nhập tên."""
        font = pygame.font.SysFont(None, 48)
        input_box = pygame.Rect(400, 300, 400, 50)
        color_active = pygame.Color('dodgerblue2')
        color_inactive = pygame.Color('gray15')
        color = color_inactive

        active = True
        player_name = ""

        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if player_name:
                            self.player_name = player_name
                            active = False
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        player_name += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not input_box.collidepoint(event.pos):
                        active = False

            # Hiển thị hộp thoại nhập tên
            self.screen.fill(self.settings.bg_color)
            txt_surface = font.render("Enter Your Name: " + player_name, True, pygame.Color('white'))
            width = max(400, txt_surface.get_width() + 10)
            input_box.w = width

            self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(self.screen, color_active if active else color_inactive, input_box, 2)
            pygame.display.flip()
            self.clock.tick(30)

        # Khi kết thúc, bắt đầu trò chơi
        self.start_new_game()

    def get_top_scores(self):
        """Fetch the top 10 scores from the database."""
        try:
            conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=HIEU_DATA;'
                'DATABASE=alien_invasion;'
                'Trusted_Connection=yes'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT TOP 10 player_name, score FROM PlayerScores ORDER BY score DESC")
            top_scores = cursor.fetchall()
            conn.close()
            return [(row.player_name, row.score) for row in top_scores]  # Trả về danh sách tuple
        except pyodbc.Error as e:
            print("Error fetching top scores:", e)
            return []

    def start_new_game(self):
        """Khởi động trò chơi sau khi nhập tên."""
        self.settings.initialize_dynamic_settings()

        # Reset lại các thông số thống kê trò chơi.
        self.stats.reset_stats()
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        self.game_active = True

        # Xóa các viên đạn và người ngoài hành tinh còn lại.
        self.bullets.empty()
        self.aliens.empty()

        # Tạo một đội quân mới và đặt lại tàu về giữa màn hình.
        self._create_fleet()
        self.ship.center_ship()

        # Ẩn con trỏ chuột.
        pygame.mouse.set_visible(False)

    def show_top_scores_screen(self):
        """Display the top scores on a new screen."""
        self.screen.fill((0, 0, 0))  # Màu nền đen

        # Lấy danh sách top scores từ cơ sở dữ liệu
        top_scores = self.get_top_scores()

        # Đặt font và màu sắc
        font = pygame.font.SysFont(None, 48)
        title = font.render("Top Scores", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen.get_rect().centerx, 50))
        self.screen.blit(title, title_rect)

        # Hiển thị từng điểm số
        for rank, (player_name, score) in enumerate(top_scores, start=1):
            score_text = f"{rank}. {player_name}: {score}"
            score_image = font.render(score_text, True, (255, 255, 255))
            score_rect = score_image.get_rect()
            score_rect.top = 100 + rank * 40
            score_rect.centerx = self.screen.get_rect().centerx
            self.screen.blit(score_image, score_rect)

        # Cập nhật màn hình
        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance (đối tượng), and run the game.
    ai = AlienInvasion()
    ai.run_game()