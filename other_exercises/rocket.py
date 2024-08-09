import pygame

class Rocket:
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        self.screen = ai_game.screen # Lấy màn hình từ trò chơi.
        self.screen_rect = ai_game.screen.get_rect() # Lấy hình chữ nhật của màn hình để dễ dàng định vị.

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/space-rocket-icon.bmp')
        self.rect = self.image.get_rect()

        self.rocket_speed = 5
        self.rect.center = self.screen_rect.center

        # Store a float for the rocket's exact horizontal position.
        self.x = float(self.rect.x)
        # Store a float for the rocket's exact horizontal position.
        self.y = float(self.rect.y)

        # Movement flag; start with a ship that's not moving.
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False


    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect) # Vẽ hình ảnh tàu lên màn hình tại vị trí xác định bởi hình chữ nhật của tàu.

    def update(self):
        """Update the ship's position based on the movement flag."""

        #Update the ship's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.rocket_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.rocket_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.rocket_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.rocket_speed

        #Update rect object from self.x.
        self.rect.x = self.x
        self.rect.y = self.y