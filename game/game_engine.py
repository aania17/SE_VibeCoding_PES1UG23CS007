import pygame
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height, initial_score_limit):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        # Initialize game objects
        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        # Score and Limit
        self.player_score = 0
        self.ai_score = 0
        self.score_limit = initial_score_limit # Dynamic score limit
        
        # Fonts for display
        self.font = pygame.font.SysFont("Arial", 36, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 24)
        self.medium_font = pygame.font.SysFont("Arial", 30)
        
        # State Management
        self.game_active = True
        self.winner = None

    def handle_input(self):
        # Only allow movement input if the game is active
        if self.game_active:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.player.move(-10, self.height)
            if keys[pygame.K_s]:
                self.player.move(10, self.height)

    def update(self):
        # Only process core game logic if the game is active
        if self.game_active:
            self.ball.move()
            self.ball.check_collision(self.player, self.ai)
            
            # Check for scoring
            scored = False
            if self.ball.x <= 0:
                self.ai_score += 1
                scored = True
            elif self.ball.x >= self.width:
                self.player_score += 1
                scored = True
            
            if scored:
                self.ball.reset()
                
            # Check for Game Over condition using the dynamic limit
            if self.player_score >= self.score_limit:
                self.game_active = False
                self.winner = "Player"
            elif self.ai_score >= self.score_limit:
                self.game_active = False
                self.winner = "AI"

            # AI movement (AI continues to move only if game is active)
            self.ai.auto_track(self.ball, self.height)
            
    def reset_game(self, new_limit):
        """Resets the scores and state, and sets a new score limit."""
        self.player_score = 0
        self.ai_score = 0
        self.score_limit = new_limit
        self.game_active = True
        self.winner = None
        self.ball.reset()
        self.player.reset_position(self.height)
        self.ai.reset_position(self.height)
        
    def render(self, screen):
        # 1. Draw essential court elements
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # 2. Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4 - player_text.get_width()//2, 20))
        screen.blit(ai_text, (self.width * 3//4 - ai_text.get_width()//2, 20))
        
        # 3. Draw Game Over screen if game is inactive
        if not self.game_active:
            # Draw translucent background
            s = pygame.Surface((450, 200)) 
            s.set_alpha(150)               
            s.fill((50, 50, 50))           
            
            bg_x = self.width // 2 - s.get_width() // 2
            bg_y = self.height // 2 - s.get_height() // 2
            screen.blit(s, (bg_x, bg_y))
            
            # Winner text
            winner_text_str = f"{self.winner} Wins Best-of-{self.score_limit}!"
            winner_text = self.font.render(winner_text_str, True, WHITE)
            text_x = self.width // 2 - winner_text.get_width() // 2
            text_y = bg_y + 20
            screen.blit(winner_text, (text_x, text_y))
            
            # Replay options title
            options_str = "Choose New Match Limit:"
            options_text = self.medium_font.render(options_str, True, WHITE)
            options_x = self.width // 2 - options_text.get_width() // 2
            screen.blit(options_text, (options_x, text_y + 50))
            
            # Key bindings
            keys_str = " (3) Best of 3 \n (5) Best of 5 \n (7) Best of 7 \n (ESC) Exit"
            keys_text = self.small_font.render(keys_str, True, WHITE)
            keys_x = self.width // 2 - keys_text.get_width() // 2
            screen.blit(keys_text, (keys_x, text_y + 90))
