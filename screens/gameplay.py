# screens/gameplay.py

import pygame
from base_screen import BaseScreen
from constants import Colors, GameState, SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE
from tracks import curved_cursor, curved_track, draw_hex, straight_cursor, straight_track
from hex_grid import HEX_SIZE, GRID_COLS, GRID_ROWS, oddr_to_pixel, pixel_to_oddr, GridManager


FONT_PATH = "assets/fonts/BitcountPropSingle-Regular.ttf"
TITLE_FONT_PATH = "assets/fonts/Frijole-Regular.ttf"
TEXT_FONT_PATH = "assets/fonts/RubikMonoOne-Regular.ttf"

STRAIGHT_TRACK_BUTTON_CENTER = pygame.Vector2(85, 250)
CURVED_TRACK_BUTTON_CENTER = pygame.Vector2(215, 250)
TRACK_BUTTON_SIZE = 48
BUTTON_BORDER_COLOR = Colors.GREEN.value
BUTTON_HIGHLIGHT_COLOR = Colors.WHITE.value
BUTTON_SELECTED_COLOR = Colors.ORANGE.value

PAUSE_OPTIONS = ["Resume Game", "Main Menu", "Quit Game"]


class GameplayScreen(BaseScreen):
    """Main gameplay screen."""
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self.screen = screen

        # Side panel setup        
        self._title_font = pygame.font.Font(TITLE_FONT_PATH, 30)
        self.title_text = self._title_font.render(GAME_TITLE, True, Colors.WHITE.value)
        self.text_font = pygame.font.Font(TEXT_FONT_PATH, 16)
        
        self.selected_track_type = None  # 'straight' or 'curved'
        self.selected_track_direction = 0  # 0-5 for hex directions

        # Pause menu state
        self.pause = False
        self.pause_option = 0  # 0: Resume, 1: Main Menu, etc.

        # Pre-render pause menu surfaces
        self.pause_overlay = pygame.Surface((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.pause_overlay.set_alpha(192)
        self.pause_overlay.fill(Colors.BLACK.value)

        self.pause_font_title = pygame.font.Font(FONT_PATH, 72)
        self.pause_title_surf = self.pause_font_title.render("PAUSED", True, Colors.WHITE.value)
        self.pause_title_rect = self.pause_title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.pause_overlay.blit(self.pause_title_surf, self.pause_title_rect)

        self.pause_font_item = pygame.font.Font(FONT_PATH, 28)
        self.pause_option_rects = []
        for i, option in enumerate(PAUSE_OPTIONS):
            color = Colors.CYAN.value if i == self.pause_option else Colors.GREEN.value
            option_surf = self.pause_font_item.render(option, True, color)
            option_rect = option_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 40))
            self.pause_option_rects.append(option_rect)
            # self.pause_overlay.blit(option_surf, option_rect)

        self.grid_manager = GridManager((GRID_COLS, GRID_ROWS))

    def draw_pause_menu(self):
        self.screen.blit(self.pause_overlay, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4))
        # Draw menu options
        for i, option in enumerate(PAUSE_OPTIONS):
            color = Colors.CYAN.value if i == self.pause_option else Colors.GREEN.value
            option_surf = self.pause_font_item.render(option, True, color)
            option_rect = option_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 40))
            self.screen.blit(option_surf, option_rect)

    def handle_events(self, events) -> GameState:
        for event in events:
            if event.type == pygame.QUIT:
                return GameState.QUIT
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Pausing game" if not self.pause else "Resuming game")
                    self.pause = not self.pause
                
                if self.pause:
                    if event.key == pygame.K_UP:
                        self.pause_option = (self.pause_option - 1) % len(PAUSE_OPTIONS)
                        print(f"Pause menu option changed to {self.pause_option}")
                    elif event.key == pygame.K_DOWN:
                        self.pause_option = (self.pause_option + 1) % len(PAUSE_OPTIONS)
                        print(f"Pause menu option changed to {self.pause_option}")
                    elif event.key == pygame.K_RETURN:
                        if self.pause_option == 0:  # Resume
                            print("Resuming game from pause menu")
                            self.pause = False
                        elif self.pause_option == 1:  # Main Menu
                            print("Returning to main menu from pause menu")
                            return GameState.MAIN_MENU
                        elif self.pause_option == 2:  # Quit Game
                            print("Quitting game from pause menu")
                            return GameState.QUIT
                    continue  # Skip other key handling when paused
                        
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.pause:
                    continue  # Ignore mouse clicks when paused

                mouse_pos = pygame.mouse.get_pos()
                hex_coords = pixel_to_oddr(*mouse_pos)
                inside_grid = (0 <= hex_coords[0] < GRID_COLS and 0 <= hex_coords[1] < GRID_ROWS)
                inside_straight_button = (STRAIGHT_TRACK_BUTTON_CENTER - mouse_pos).length() < TRACK_BUTTON_SIZE
                inside_curved_button = (CURVED_TRACK_BUTTON_CENTER - mouse_pos).length() < TRACK_BUTTON_SIZE
                
                if event.button == 1:  # Left click
                    if inside_straight_button:
                        self.selected_track_type = 'straight' if self.selected_track_type != 'straight' else None
                    elif inside_curved_button:
                        self.selected_track_type = 'curved' if self.selected_track_type != 'curved' else None
                    elif not inside_grid:
                        self.selected_track_type = None  # Deselect track type if clicking outside grid and buttons
                    elif inside_grid and self.selected_track_type:
                        tile = self.grid_manager.get_tile(*hex_coords)
                        tile.add_track(
                            self.selected_track_direction, 
                            (self.selected_track_direction + (3 if self.selected_track_type == 'straight' else 2)) % 6
                        )
                
                if event.button == 3:  # Right click
                    if inside_grid and self.selected_track_type:
                        self.selected_track_direction = (self.selected_track_direction + 1) % 6
                
        return GameState.STAY
    
    def draw_buttons(self):
        straight_track(self.screen, STRAIGHT_TRACK_BUTTON_CENTER, TRACK_BUTTON_SIZE, direction=0)
        curved_track(self.screen, CURVED_TRACK_BUTTON_CENTER, TRACK_BUTTON_SIZE, direction=0)

        # Check mouse hover for buttons
        mouse_pos = pygame.mouse.get_pos()

        color = BUTTON_HIGHLIGHT_COLOR if (STRAIGHT_TRACK_BUTTON_CENTER - mouse_pos).length() < TRACK_BUTTON_SIZE else BUTTON_BORDER_COLOR
        if self.selected_track_type == 'straight':
            color = BUTTON_SELECTED_COLOR
        draw_hex(self.screen, STRAIGHT_TRACK_BUTTON_CENTER, TRACK_BUTTON_SIZE, color, line_width=2)

        color = BUTTON_HIGHLIGHT_COLOR if (CURVED_TRACK_BUTTON_CENTER - mouse_pos).length() < TRACK_BUTTON_SIZE else BUTTON_BORDER_COLOR
        if self.selected_track_type == 'curved':
            color = BUTTON_SELECTED_COLOR
        draw_hex(self.screen, CURVED_TRACK_BUTTON_CENTER, TRACK_BUTTON_SIZE, color, line_width=2)

        
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

        self.draw_buttons()
        
    def update(self):
        if self.pause:
            mouse_pos = pygame.mouse.get_pos()
            for i, option_rect in enumerate(self.pause_option_rects):
                if option_rect.collidepoint(mouse_pos):
                    self.pause_option = i

    def draw(self):
        self.screen.fill(Colors.BLACK.value)
        # Draw hex grid
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                cx, cy = oddr_to_pixel(col, row)
                center = pygame.math.Vector2(cx, cy)
                draw_hex(self.screen, center, HEX_SIZE, Colors.CYAN.value)
                tile = self.grid_manager.get_tile(col, row)
                for track in tile.built_tracks:
                    dir1, dir2 = track
                    if (dir1 - dir2) % 6 == 3:  # Straight track
                        straight_track(self.screen, center, HEX_SIZE, direction=dir1)
                    else:  # Curved track
                        curved_track(self.screen, center, HEX_SIZE, direction=dir1)

        if self.pause:
            self.draw_pause_menu()
            return
        
        mouse_pos = pygame.mouse.get_pos()
        hex_coords = pixel_to_oddr(*mouse_pos)
        inside_grid = (0 <= hex_coords[0] < GRID_COLS and 0 <= hex_coords[1] < GRID_ROWS)

        self.draw_info_panel()

        # Highlight hex under mouse
        if 0 <= hex_coords[0] < GRID_COLS and 0 <= hex_coords[1] < GRID_ROWS:
            cx, cy = oddr_to_pixel(*hex_coords)
            center = pygame.math.Vector2(cx, cy)
            draw_hex(self.screen, center, HEX_SIZE, Colors.ORANGE.value, line_width=2)

        if inside_grid and self.selected_track_type:
            pygame.mouse.set_visible(False)
            center = pygame.math.Vector2(*oddr_to_pixel(*hex_coords))
            if self.selected_track_type == 'straight':
                straight_cursor(self.screen, center, HEX_SIZE, self.selected_track_direction)
            else:
                curved_cursor(self.screen, center, HEX_SIZE, self.selected_track_direction)
        else:
            pygame.mouse.set_visible(True)
