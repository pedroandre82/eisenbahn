import pygame
from base_screen import BaseScreen
from constants import GAME_FPS, GameState


class SplashScreen(BaseScreen):
    """Splash screen shown at game start."""

    def __init__(self, screen):
        super().__init__(screen)
        self.splash_time = 4000  # ms
        self.ticks = 0
        self.skip = False

    def handle_events(self, events) -> GameState | None:
        for event in events:
            if event.type == pygame.QUIT:
                return GameState.QUIT
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE] or self.skip:  # Skip splash on ESC
            # print("Skipping splash screen")
            return GameState.MAIN_MENU
        return None

    def update(self):
        self.ticks += 1
        if self.ticks > self.splash_time / 1000 * GAME_FPS:
            self.skip = True  # Mark to skip on next event check

    def draw(self):
        BLUE = (0, 100, 200)
        WHITE = (255, 255, 255)
        SCREEN_WIDTH, SCREEN_HEIGHT = self.screen.get_size()

        # Fill background
        self.screen.fill(BLUE)

        # Draw splash text
        main_font = pygame.font.Font(None, 74)
        text = main_font.render("Eisenbahn", True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(text, text_rect)

        # Small subtitle
        small_font = pygame.font.Font(None, 36)
        subtitle = small_font.render("Press ESC to skip or wait...", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
        self.screen.blit(subtitle, subtitle_rect)
