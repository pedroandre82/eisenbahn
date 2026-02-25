import pygame
import sys
from constants import GAME_FPS, GameState, SCREEN_WIDTH, SCREEN_HEIGHT
from screens.splash_screen import SplashScreen


# Initialize Pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Eisenbahn")
clock = pygame.time.Clock()

# State manager; Start with splash screen
current_state = SplashScreen(screen)
    

running = True
while running:
    events = pygame.event.get()
    next_state = current_state.handle_events(events)
    if next_state == GameState.QUIT:
        running = False
    elif next_state != GameState.STAY:
        # Here we would normally switch to the new state, e.g.:
        # if next_state == GameState.MAIN_MENU:
        #     current_state = MainMenuScreen(screen)
        running = False  # For now, exit after splash

    current_state.update()
    current_state.draw()
    pygame.display.flip()
    clock.tick(GAME_FPS)


pygame.quit()
sys.exit()
