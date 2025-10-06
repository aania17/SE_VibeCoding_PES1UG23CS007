import pygame
import random
# Initialize pygame.mixer as requested
pygame.mixer.init()

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

        # Load sound effects 
        try:
            # NOTE: Update these paths if your .wav files are located elsewhere!
            self.paddle_hit_sound = pygame.mixer.Sound("assets/paddle_hit.wav")
            self.wall_bounce_sound = pygame.mixer.Sound("assets/wall_bounce.wav")
            self.score_sound = pygame.mixer.Sound("assets/score.wav") 
        except pygame.error as e:
            print(f"Warning: Could not load one or more sound files. Error: {e}. Check asset paths.")
            self.paddle_hit_sound = None
            self.wall_bounce_sound = None
            self.score_sound = None

    def move(self):
        # Update ball position
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Wall collision (top/bottom): reverse Y direction
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            if self.wall_bounce_sound:
                self.wall_bounce_sound.play()
            self.velocity_y *= -1

    def check_collision(self, player, ai):
        # Get the Rect objects for collision check
        ball_rect = self.rect()
        player_rect = player.rect()
        ai_rect = ai.rect()
        
        # Check collision with player paddle (left side)
        if ball_rect.colliderect(player_rect):
            # ONLY reverse if the ball is moving towards the paddle (leftwards)
            if self.velocity_x < 0:
                self.velocity_x *= -1
                if self.paddle_hit_sound:
                    self.paddle_hit_sound.play()
                
        # Check collision with AI paddle (right side)
        elif ball_rect.colliderect(ai_rect):
            # ONLY reverse if the ball is moving towards the paddle (rightwards)
            if self.velocity_x > 0:
                self.velocity_x *= -1
                if self.paddle_hit_sound:
                    self.paddle_hit_sound.play()

    def reset(self):
        """Resets the ball position to center and gives it a random vertical velocity."""
        self.x = self.original_x
        self.y = self.original_y
        # Reverse X velocity to serve back to the player who just scored
        self.velocity_x *= -1 
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def play_score_sound(self):
        """Plays the score sound effect. Designed to be called by GameEngine."""
        if self.score_sound:
            self.score_sound.play()
