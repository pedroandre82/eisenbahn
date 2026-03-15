# screens/gameplay.py

import pygame
from base_screen import BaseScreen
from constants import Colors, GameState, SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE
from tracks import curved_track, draw_hex, straight_track
from hex_grid import HEX_SIZE, GRID_COLS, GRID_ROWS, oddr_to_pixel, pixel_to_oddr


FONT_PATH = "assets/fonts/BitcountPropSingle-Regular.ttf"
TITLE_FONT_PATH = "assets/fonts/Frijole-Regular.ttf"
TEXT_FONT_PATH = "assets/fonts/RubikMonoOne-Regular.ttf"


class GameplayScreen(BaseScreen):
    """Main gameplay screen."""
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self.screen = screen
        self._title_font = pygame.font.Font(TITLE_FONT_PATH, 30)
        self.title_text = self._title_font.render(GAME_TITLE, True, Colors.WHITE.value)
        self.text_font = pygame.font.Font(TEXT_FONT_PATH, 16)
        self.pause = False
        self.pause_option = 0  # 0: Resume, 1: Main Menu

    def draw_pause_menu(self):
        # Draw a semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        overlay.set_alpha(192)  # Semi-transparent
        overlay.fill(Colors.BLACK.value)
        self.screen.blit(overlay, (SCREEN_WIDTH // 2 - overlay.get_width() // 2, SCREEN_HEIGHT // 2 - overlay.get_height() // 2))

        # Draw pause text
        font = pygame.font.Font(FONT_PATH, 72)
        title = font.render("PAUSED", True, Colors.WHITE.value)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(title, title_rect)
        
        # Draw menu
        resume_font = pygame.font.Font(FONT_PATH, 28)
        resume_color = Colors.CYAN.value if self.pause_option == 0 else Colors.GREEN.value
        resume_text = resume_font.render("Resume Game", True, resume_color)
        resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        self.screen.blit(resume_text, resume_rect)

        menu_color = Colors.CYAN.value if self.pause_option == 1 else Colors.GREEN.value
        menu_text = resume_font.render("Main Menu", True, menu_color)
        menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        self.screen.blit(menu_text, menu_rect)

    def handle_events(self, events) -> GameState:
        for event in events:
            if event.type == pygame.QUIT:
                return GameState.QUIT
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Pausing game" if not self.pause else "Resuming game")
                    self.pause = not self.pause
                
                if self.pause:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.pause_option = (self.pause_option + 1) % 2
                        print(f"Pause menu option changed to {self.pause_option}")
                    elif event.key == pygame.K_RETURN:
                        if self.pause_option == 0:  # Resume
                            print("Resuming game from pause menu")
                            self.pause = False
                        elif self.pause_option == 1:  # Main Menu
                            print("Returning to main menu from pause menu")
                            return GameState.MAIN_MENU
                
        return GameState.STAY
        
    def draw_info_panel(self):
        pygame.draw.rect(self.screen, Colors.CYAN.value, (5, 5, 295, SCREEN_HEIGHT - 10), width=4, border_radius=15)
        # Draw title
        title_rect = self.title_text.get_rect(center=(150, 30))
        self.screen.blit(self.title_text, title_rect)
        # Draw mouse position
        mouse_pos = pygame.mouse.get_pos()
        mouse_text = self.text_font.render(f"Mouse: {mouse_pos}", True, Colors.WHITE.value)
        self.screen.blit(mouse_text, (15, 70))
        # Draw hex coordinates under mouse if within grid
        hex_coords = pixel_to_oddr(*mouse_pos)
        within_grid = (0 <= hex_coords[0] < GRID_COLS and 0 <= hex_coords[1] < GRID_ROWS)
        hex_text = self.text_font.render(f"Hex: {hex_coords if within_grid else 'None'}", True, Colors.WHITE.value)
        self.screen.blit(hex_text, (15, 100))

    def update(self):
        pass

    def draw(self):
        if self.pause:
            self.draw_pause_menu()
            return

        self.screen.fill(Colors.BLACK.value)
        self.draw_info_panel()

        # Draw hex grid
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                cx, cy = oddr_to_pixel(col, row)
                center = pygame.math.Vector2(cx, cy)
                draw_hex(self.screen, center, HEX_SIZE, Colors.CYAN.value)

        # Highlight hex under mouse
        mouse_pos = pygame.mouse.get_pos()
        hex_coords = pixel_to_oddr(*mouse_pos)
        if 0 <= hex_coords[0] < GRID_COLS and 0 <= hex_coords[1] < GRID_ROWS:
            cx, cy = oddr_to_pixel(*hex_coords)
            center = pygame.math.Vector2(cx, cy)
            draw_hex(self.screen, center, HEX_SIZE, Colors.ORANGE.value, line_width=2)
