# screens/splash_screen.py

import pygame  # type: ignore
from base_screen import BaseScreen
from constants import GAME_FPS, GAME_TITLE, GameState, Colors

BACKGROUND_COLOR = Colors.BLACK.value
TEXT_COLOR = Colors.CYAN.value

TITLE_FONT_PATH = "assets/fonts/Frijole-Regular.ttf"
SUBTITLE_FONT_PATH = "assets/fonts/RubikMonoOne-Regular.ttf"


class SplashScreen(BaseScreen):
    """Splash screen shown at game start."""

    def __init__(self, screen):
        super().__init__(screen)
        self.splash_time = 10_000  # ms
        self.ticks = 0
        self.skip = False

    def handle_events(self, events) -> GameState:
        for event in events:
            if event.type == pygame.QUIT:
                print("Quit event received in splash screen")
                return GameState.QUIT
        if self.skip:
            return GameState.MAIN_MENU
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:  # Skip splash on ESC
            print("Skipping splash screen")
            self.skip = True
        return GameState.STAY  # No state change

    def update(self):
        if self.skip:
            return
        self.ticks += 1
        if self.ticks > self.splash_time / 1000 * GAME_FPS:
            print("Splash time expired")
            self.skip = True  # Mark to skip on next event check

    def draw(self):
        SCREEN_WIDTH, SCREEN_HEIGHT = self.screen.get_size()

        # Fill background
        self.screen.fill(BACKGROUND_COLOR)

        # Draw splash text
        main_font = pygame.font.Font(TITLE_FONT_PATH, 96)
        text = main_font.render(GAME_TITLE, True, TEXT_COLOR)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
        self.screen.blit(text, text_rect)

        # Small subtitle
        small_font = pygame.font.Font(SUBTITLE_FONT_PATH, 24)
        subtitle = small_font.render("Press ESC to skip or wait...", True, TEXT_COLOR)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
        self.screen.blit(subtitle, subtitle_rect)
