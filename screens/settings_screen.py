# settings_screen.py
import pygame
from base_screen import BaseScreen
from constants import GameState, SCREEN_WIDTH, SCREEN_HEIGHT, Colors
from typing import Any


TITLE_FONT_SIZE = 48
LABEL_FONT_SIZE = 32
OPTION_FONT_SIZE = 28

BACKGROUND_COLOR = Colors.BLACK.value
TEXT_COLOR = Colors.CYAN.value
TEXT_HIGHLIGHT = Colors.WHITE.value
HIGHLIGHT_COLOR = Colors.ORANGE.value

FONT_PATH = "assets/fonts/BitcountPropSingle-Regular.ttf"

class SettingsScreen(BaseScreen):
    """Settings screen where players can adjust game options."""

    def __init__(self, screen):
        super().__init__(screen)
        self.title_font = pygame.font.Font(FONT_PATH, TITLE_FONT_SIZE)
        self.label_font = pygame.font.Font(FONT_PATH, LABEL_FONT_SIZE)
        self.option_font = pygame.font.Font(FONT_PATH, OPTION_FONT_SIZE)

        # Settings options
        self.options: list[dict[str, Any]] = [
            {"option": "Screen size", "values": ("800x600", "1280x720"), "current": 0},
            {"option": "FPS", "values": ("60", "30"), "current": 0},
        ]
        self.current_option = 0

    def handle_events(self, events) -> GameState:
        for event in events:
            if event.type == pygame.QUIT:
                return GameState.QUIT
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return GameState.MAIN_MENU
                if event.key == pygame.K_UP:
                    self.current_option = max(0, self.current_option - 1)
                
                elif event.key == pygame.K_DOWN:
                    self.current_option = min(len(self.options) - 1, self.current_option + 1)

                elif event.key == pygame.K_LEFT:
                    option = self.options[self.current_option]
                    option["current"] = max(0, option["current"] - 1)
                    print(f"Changed {option['option']} to {option['values'][option['current']]}.")

                elif event.key == pygame.K_RIGHT:
                    option = self.options[self.current_option]
                    option["current"] = min(len(option["values"]) - 1, option["current"] + 1)
                    print(f"Changed {option['option']} to {option['values'][option['current']]}.")

                elif event.key == pygame.K_RETURN:
                    option = self.options[self.current_option]["option"]
                    value = self.options[self.current_option]["values"][self.options[self.current_option]["current"]]
                    print(f"Setting {option} to {value}.")

        return GameState.STAY

    def update(self):
        pass  # No dynamic elements to update for now

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)

        # Draw title
        title_surface = self.title_font.render("SETTINGS", True, TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_surface, title_rect)

        # Draw options
        OPTIONS_TOP = 250
        OPTIONS_SPACING = 80
        VALUES_SPACING = 40
        for i, option in enumerate(self.options):
            label_surface = self.label_font.render(option["option"] + ":", True, TEXT_HIGHLIGHT)
            label_rect = label_surface.get_rect(midright=(SCREEN_WIDTH // 3, OPTIONS_TOP + i * OPTIONS_SPACING))
            self.screen.blit(label_surface, label_rect)

            # Draw values
            value_x = SCREEN_WIDTH // 3 + 20
            for j, value in enumerate(option["values"]):
                value_surface = self.option_font.render(value, True, TEXT_HIGHLIGHT if j == option["current"] else TEXT_COLOR)
                value_rect = value_surface.get_rect(midleft=(value_x, OPTIONS_TOP + i * OPTIONS_SPACING))
                value_x += value_surface.get_width() + VALUES_SPACING
                self.screen.blit(value_surface, value_rect)
                # Highlight current value
                if i == self.current_option and j == option["current"]:
                    pygame.draw.rect(
                        self.screen, 
                        HIGHLIGHT_COLOR, 
                        value_rect.inflate(10, 10).move(-3, 0), 
                        width=2, 
                        border_radius=5,
                    )


