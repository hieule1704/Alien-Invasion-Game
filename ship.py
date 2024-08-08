import pygame

class Ship:
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        self.screen = ai_game.screen # Lấy màn hình từ trò chơi.
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect() # Lấy hình chữ nhật của màn hình để dễ dàng định vị.

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a float for the ship's exact horizontal position.
        self.x = float(self.rect.x)

        # Movement flag; start with a ship that's not moving.
        self.moving_right = False
        self.moving_left = False


    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect) # Vẽ hình ảnh tàu lên màn hình tại vị trí xác định bởi hình chữ nhật của tàu.

    def update(self):
        """Update the ship's position based on the movement flag."""

        #Update the ship's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        #Update rect object from self.x.
        self.rect.x = self.x