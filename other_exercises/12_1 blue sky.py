import pygame
import sys


def run_game():
    # Khởi tạo Pygame
    pygame.init()

    # Thiết lập kích thước màn hình
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Blue Sky")

    # Đặt màu nền là màu xanh dương
    blue_color = (135, 206, 250)

    while True:
        # Kiểm tra các sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Vẽ nền màu xanh dương
        screen.fill(blue_color)

        # Cập nhật màn hình
        pygame.display.flip()


if __name__ == '__main__':
    run_game()
