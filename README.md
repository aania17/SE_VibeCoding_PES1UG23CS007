Pygame Ping Pong (Classic Arcade Clone)
This is a two-player (Player vs. AI) implementation of the classic arcade game, Pong, built using the Pygame library in Python. The game features responsive controls, AI movement, and a complete game cycle including scoring, game over, and an interactive replay menu.

🚀 How to Run the Project
Prerequisites
Python 3.x

Pygame library (pip install pygame)

File Structure
The project assumes the following directory structure, which is critical for the sound effects to load correctly:

/ping_pong_project
|-- main.py
|-- game/
|   |-- __init__.py
|   |-- game_engine.py
|   |-- paddle.py
|   |-- ball.py
|-- assets/
|   |-- paddle_hit.wav
|   |-- wall_bounce.wav
|   |-- score.wav


Execution
Ensure you have your .wav files in the assets/ folder.

Run the main file from your terminal:

python main.py

✅ Project Evolution: Feature Log
This section details the development steps and the logic implemented for each new feature request.

1. Game Over Screen and Score Limit (Initial Implementation)
Goal: End the game at 5 points, display a winner message, and freeze the action for a clear game-over state.

Solution Approach:

Game State Management: A boolean variable, self.game_active, was introduced in GameEngine. All primary game logic (ball.move(), collision checks) were wrapped inside an if self.game_active: block in GameEngine.update().

Win Condition Check: The GameEngine.update() method was updated to check if self.player_score or self.ai_score reached the initial limit (5). If so, self.game_active was set to False, and self.winner was set.

Rendering the Message: The GameEngine.render() method was enhanced to check if not self.game_active. When the game is over, it uses Pygame's font.render() to draw the "Player Wins!" or "AI Wins!" message and a slightly transparent grey overlay to highlight the message.

2. Interactive Replay Feature
Goal: Replace the hard-coded exit delay with an interactive menu to start a new match with variable score limits (Best of 3/5/7) or exit.

Solution Approach:

Dynamic Score Limit: The GameEngine constructor was updated to accept initial_score_limit, making the winning score dynamic (self.score_limit).

The Replay Method: A new method, GameEngine.reset_game(new_limit), was created. This method handles resetting both scores to 0, resetting the ball's position, resetting the paddle positions (by calling a new paddle.reset_position() method), setting the new score_limit, and setting self.game_active = True.

Input Handling in main.py: The main game loop now explicitly checks keyboard events (pygame.K_3, pygame.K_5, pygame.K_7, pygame.K_ESCAPE) only when the game is inactive (if not engine.game_active).

If a limit key (3, 5, or 7) is pressed, it calls engine.reset_game(value).

If ESC is pressed, it quits the main loop.

UI Update: The GameEngine.render() function was updated to display the interactive menu options (e.g., (3) Best of 3) below the winner announcement when the game is inactive.

3. Sound Effects Integration
Goal: Add audio feedback for paddle hits, wall bounces, and scoring.

Solution Approach:

Initialization & Loading:

pygame.mixer.init() was called at the start of ball.py.

Sound objects were loaded in Ball.__init__ using pygame.mixer.Sound(), referencing files in the assets/ directory (e.g., "assets/paddle_hit.wav"). Robust error handling (try/except) was added for sound loading failures.

Paddle Hit and Wall Bounce: The sound playing logic was placed directly inside the Ball.move() and Ball.check_collision() methods:

When the ball hits the top/bottom wall and self.velocity_y is reversed, self.wall_bounce_sound.play() is called.

When the ball collides with a paddle and self.velocity_x is reversed, self.paddle_hit_sound.play() is called.

Scoring Sound:

A dedicated method, Ball.play_score_sound(), was created.

This method is called from the GameEngine.update() method immediately after a score is registered (i.e., when scored = True) and before the ball is reset.