import pygame

class Paddle:
    def __init__(self, x, y, width, height):
        self.original_x = x # Store original position for reset
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 7

    def move(self, dy, screen_height):
        # Move the paddle vertically
        self.y += dy
        # Clamp the position so the paddle stays within screen bounds
        self.y = max(0, min(self.y, screen_height - self.height))

    def reset_position(self, screen_height):
        """Resets the paddle to its starting vertical position."""
        # Center vertically
        self.y = screen_height // 2 - self.height // 2 
        
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def auto_track(self, ball, screen_height):
        # Simple AI that tracks the ball's Y position
        if ball.y < self.y:
            self.move(-self.speed, screen_height)
        elif ball.y > self.y + self.height:
            self.move(self.speed, screen_height)
