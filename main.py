# main.py

import pygame
import sys
from constants import GAME_FPS, GameState, SCREEN_WIDTH, SCREEN_HEIGHT
from screens.main_menu import MainMenuScreen
from screens.splash_screen import SplashScreen
from screens.settings_screen import SettingsScreen
from screens.gameplay import BouncingBall, HexTile, GameplayScreen


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
        if next_state == GameState.MAIN_MENU:  
            current_state = MainMenuScreen(screen)
        elif next_state == GameState.GAMEPLAY:
            # current_state = BouncingBall(screen)
            # current_state = HexTile(screen)
            current_state = GameplayScreen(screen)
        elif next_state == GameState.SETTINGS:
            current_state = SettingsScreen(screen)
        elif next_state == GameState.CREDITS:
            # Placeholder for credits screen
            current_state = SplashScreen(screen)


    current_state.update()
    current_state.draw()
    pygame.display.flip()
    clock.tick(GAME_FPS)

print("Exiting game...")
pygame.quit()
sys.exit()
