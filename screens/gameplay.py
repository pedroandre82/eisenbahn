# simple bouncing circle mockup

import pygame
from base_screen import BaseScreen
from constants import Colors, GameState, SCREEN_WIDTH, SCREEN_HEIGHT
from tiles import curved_track, draw_hex, straight_track

FONT_PATH = "assets/fonts/BitcountPropSingle-Regular.ttf"


class BouncingBall(BaseScreen):
    """Gameplay screen with a bouncing circle."""

    def __init__(self, screen):
        super().__init__(screen)
        self.circle_pos = pygame.math.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.circle_vel = pygame.math.Vector2(3, 2)  # Velocity vector
        self.circle_radius = 30
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
                print("Quit event received in gameplay screen")
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

    def update(self):
        if self.pause:
            return  # Skip updating positions when paused
        
        # Move circle
        self.circle_pos += self.circle_vel

        # Bounce off walls
        if self.circle_pos.x - self.circle_radius <= 0 or self.circle_pos.x + self.circle_radius >= SCREEN_WIDTH:
            self.circle_vel.x *= -1
            print("Bounced horizontally")
        if self.circle_pos.y - self.circle_radius <= 0 or self.circle_pos.y + self.circle_radius >= SCREEN_HEIGHT:
            self.circle_vel.y *= -1
            print("Bounced vertically")

    def draw(self):
        # Fill background
        self.screen.fill(Colors.GREEN.value)

        # Draw bouncing circle
        pygame.draw.circle(self.screen, Colors.WHITE.value, (int(self.circle_pos.x), int(self.circle_pos.y)), self.circle_radius)

        # If paused, draw pause menu overlay
        if self.pause:
            self.draw_pause_menu()

        
class HexTile(BaseScreen):
    """Placeholder for hex tile rendering."""
    def __init__(self, screen):
        super().__init__(screen)

    def handle_events(self, events) -> GameState:
        for event in events:
            if event.type == pygame.QUIT:
                return GameState.QUIT
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return GameState.MAIN_MENU
                
        return GameState.STAY

    def update(self):
        pass

    def draw(self):
        self.screen.fill(Colors.BLACK.value)
        # Example hex tiles width increasing sizes to test drawing functions
        for i in range(1, 8):
            tile_size = 12 * i
            center = pygame.math.Vector2(50 + i * tile_size, SCREEN_HEIGHT // 2)
            draw_hex(self.screen, center, tile_size, Colors.CYAN.value)
            straight_track(self.screen, center, tile_size)
            curved_track(self.screen, center, tile_size, 0)
        # tile_size = 24
        # draw_hex(self.screen, pygame.math.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), tile_size, Colors.CYAN.value)
        # straight_track(self.screen, pygame.math.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), tile_size)
        # curved_track(self.screen, pygame.math.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), tile_size, 0)


    