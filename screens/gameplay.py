# screens/gameplay.py

import pygame
from base_screen import BaseScreen
from constants import Colors, GameState, SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE
from tracks import curved_cursor, curved_track, draw_hex, straight_cursor, straight_track
from hex_grid import HEX_SIZE, GRID_COLS, GRID_ROWS, oddr_to_pixel, pixel_to_oddr, GridManager
from .pause_menu import PauseMenu


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

        self.pause = False
        self.pause_menu = PauseMenu(self.screen)

        self.grid_manager = GridManager((GRID_COLS, GRID_ROWS))

    def handle_events(self, events) -> GameState:
        mouse_pos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.QUIT:
                return GameState.QUIT
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                print("Pausing game" if not self.pause else "Resuming game")
                self.pause = not self.pause
                
            if self.pause:
                result = self.pause_menu.handle_events(events, mouse_pos)
                if result == GameState.GAMEPLAY:
                    self.pause = False
                elif result != GameState.STAY:
                    return result
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.pause:
                    continue  # Ignore mouse clicks when paused

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
                            self.selected_track_type,
                            self.selected_track_direction
                        )
                
                if event.button == 3:  # Right click
                    if inside_grid and self.selected_track_type:
                        self.selected_track_direction = (self.selected_track_direction + 1)
                        self.selected_track_direction %= 6 if self.selected_track_type == 'curved' else 3
                
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

        # # Draw mouse position
        # mouse_pos = pygame.mouse.get_pos()
        # mouse_text = self.text_font.render(f"Mouse: {mouse_pos}", True, Colors.WHITE.value)
        # self.screen.blit(mouse_text, (15, 70))
        
        # # Draw hex coordinates under mouse if within grid
        # hex_coords = pixel_to_oddr(*mouse_pos)
        # within_grid = (0 <= hex_coords[0] < GRID_COLS and 0 <= hex_coords[1] < GRID_ROWS)
        # hex_text = self.text_font.render(f"Hex: {hex_coords if within_grid else 'None'}", True, Colors.WHITE.value)
        # self.screen.blit(hex_text, (15, 100))

        self.draw_buttons()
        
    def update(self):
        pass

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
                    track_type, dir = track
                    if track_type == 'straight':
                        straight_track(self.screen, center, HEX_SIZE, direction=dir)
                    else:
                        curved_track(self.screen, center, HEX_SIZE, direction=dir)

        self.draw_info_panel()
        
        if self.pause:
            self.pause_menu.draw()
            return
        
        mouse_pos = pygame.mouse.get_pos()
        hex_coords = pixel_to_oddr(*mouse_pos)
        inside_grid = (0 <= hex_coords[0] < GRID_COLS and 0 <= hex_coords[1] < GRID_ROWS)

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
