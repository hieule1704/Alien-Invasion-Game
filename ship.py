import pygame

class Ship:
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        self.screen = ai_game.screen # Lấy màn hình từ trò chơi.
        self.screen_rect = ai_game.screen.get_rect() # Lấy hình chữ nhật của màn hình để dễ dàng định vị.

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect) # Vẽ hình ảnh tàu lên màn hình tại vị trí xác định bởi hình chữ nhật của tàu.