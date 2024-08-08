import pygame
import sys


class Character:
    """Lớp để quản lý nhân vật trò chơi."""

    def __init__(self, screen):
        """Khởi tạo nhân vật và đặt vị trí bắt đầu."""
        self.screen = screen

        # Tải hình ảnh nhân vật và lấy rect của nó
        self.image = pygame.image.load('../images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Đặt nhân vật ở trung tâm màn hình
        self.rect.center = self.screen_rect.center

    def blitme(self):
        """Vẽ nhân vật ở vị trí hiện tại của nó."""
        self.screen.blit(self.image, self.rect)


def run_game():
    # Khởi tạo Pygame
    pygame.init()

    # Thiết lập kích thước màn hình
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Game Character")

    # Đặt màu nền
    bg_color = (135, 206, 250)

    # Tạo một nhân vật
    character = Character(screen)

    while True:
        # Kiểm tra các sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Vẽ nền
        screen.fill(bg_color)

        # Vẽ nhân vật
        character.blitme()

        # Cập nhật màn hình
        pygame.display.flip()


if __name__ == '__main__':
    run_game()
