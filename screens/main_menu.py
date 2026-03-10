# screens/main_menu.py

import pygame
from base_screen import BaseScreen
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, GameState, MainMenuOption, Colors


BACKGROUND_COLOR = Colors.BLACK.value
BUTTON_COLOR = Colors.GREEN.value
BUTTON_HOVER_COLOR = Colors.CYAN.value
TEXT_COLOR = Colors.WHITE.value
TEXT_HIGHLIGHT_COLOR = Colors.CYAN.value

FONT_PATH = "assets/fonts/BitcountPropSingle-Regular.ttf"
FONT_SIZE = 36
BUTTON_HEIGHT = 50
BUTTON_WIDTH = 250
BUTTON_SPACING = 20


class MainMenuScreen(BaseScreen):
    """Main menu screen with options to start game, settings, credits, etc."""

    def __init__(self, screen):
        super().__init__(screen)
        self.selected_index = 0  # Start game is selected by default
        
        # define buttons rectangles for click detection
        self.buttons = []
        self._create_buttons()

    def _create_buttons(self):
        total_height = len(list(MainMenuOption)) * (BUTTON_HEIGHT + BUTTON_SPACING) - BUTTON_SPACING
        start_y = (SCREEN_HEIGHT - total_height) // 2
        
        for i, option in enumerate(list(MainMenuOption)):
            x = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
            y = start_y + i * (BUTTON_HEIGHT + BUTTON_SPACING)
            rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
            self.buttons.append((option, rect))

    def handle_events(self, events) -> GameState:
        for event in events:
            if event.type == pygame.QUIT:
                return GameState.QUIT
            
            # Keyboard navigation
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.buttons)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.buttons)
                elif event.key == pygame.K_RETURN:
                    selected_option = self.buttons[self.selected_index][0]
                    print(f"Selected {selected_option}")
                    if selected_option == MainMenuOption.START_GAME:
                        return GameState.GAMEPLAY
                    elif selected_option == MainMenuOption.SETTINGS:
                        return GameState.SETTINGS
                    elif selected_option == MainMenuOption.CREDITS:
                        return GameState.CREDITS
                    elif selected_option == MainMenuOption.QUIT:
                        return GameState.QUIT
                elif event.key == pygame.K_ESCAPE:
                    print(f"ESC pressed, quitting game.")
                    return GameState.QUIT
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                mouse_pos = event.pos
                for option, rect in self.buttons:
                    if rect.collidepoint(mouse_pos):
                        print(f"Clicked on {option}")
                        if option == MainMenuOption.START_GAME:
                            return GameState.GAMEPLAY
                        elif option == MainMenuOption.SETTINGS:
                            return GameState.SETTINGS
                        elif option == MainMenuOption.CREDITS:
                            return GameState.CREDITS
                        elif option == MainMenuOption.QUIT:
                            return GameState.QUIT

        return GameState.STAY  # No state change
    
    def update(self):
        # Select button on hover
        mouse_pos = pygame.mouse.get_pos()
        for i, (_, rect) in enumerate(self.buttons):
            if rect.collidepoint(mouse_pos):
                self.selected_index = i
                break

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        font = pygame.font.Font(FONT_PATH, FONT_SIZE)

        for i, (option, rect) in enumerate(self.buttons):
            pygame.draw.rect(self.screen, BUTTON_COLOR, rect, border_radius=10)
            if i == self.selected_index:
                pygame.draw.rect(self.screen, BUTTON_HOVER_COLOR, rect, width=2, border_radius=10)
            text = font.render(option.value, True, TEXT_COLOR if i != self.selected_index else TEXT_HIGHLIGHT_COLOR)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
