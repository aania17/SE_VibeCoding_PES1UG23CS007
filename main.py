import pygame
import sys 
from game.game_engine import GameEngine

# Initialize pygame/Start application
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game loop
# Start with a default best-of-5 setting (score limit 5)
engine = GameEngine(WIDTH, HEIGHT, 5) 

def main():
    running = True

    while running:
        SCREEN.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Replay Input Handler: Check for key press only when the game is over
            if not engine.game_active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    # Best of 3
                    engine.reset_game(3) 
                elif event.key == pygame.K_5:
                    # Best of 5
                    engine.reset_game(5)
                elif event.key == pygame.K_7:
                    # Best of 7
                    engine.reset_game(7)
                elif event.key == pygame.K_ESCAPE:
                    # Exit the game
                    running = False

        # Handle user paddle input (only active if engine.game_active is True)
        engine.handle_input()
        # Update game state (movement, scoring, collision)
        engine.update()
        # Draw everything to the screen
        engine.render(SCREEN)
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit() # Ensure the script exits cleanly

if __name__ == "__main__":
    main()
