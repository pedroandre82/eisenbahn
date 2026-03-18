# screens/pause_menu.py

import pygame
from constants import *

FONT_PATH = "assets/fonts/BitcountPropSingle-Regular.ttf"


class PauseMenu:
    def __init__(self, screen):
        self.screen = screen

        self.options = [
            ("Resume Game", GameState.GAMEPLAY), 
            ("Main Menu", GameState.MAIN_MENU), 
            ("Quit Game", GameState.QUIT),
        ]
        self.selected = 0
        
        w, h = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        self.overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        self.overlay.set_alpha(240)
        self.overlay.fill(Colors.BLACK.value)

        self.title_font = pygame.font.Font(FONT_PATH, 72)
        self.item_font = pygame.font.Font(FONT_PATH, 28)

        self.title_surf = self.title_font.render("PAUSED", True, Colors.WHITE.value)
        self.title_rect = self.title_surf.get_rect(center=(w // 2, h // 4))

    def draw(self):
        screen_rect = self.screen.get_rect()
        overlay_rect = self.overlay.get_rect(center=screen_rect.center)
        self.screen.blit(self.overlay, overlay_rect)
        
        self.screen.blit(self.title_surf, self.title_rect.move(overlay_rect.topleft))
        for i, (text, _) in enumerate(self.options):
            color = Colors.CYAN.value if i == self.selected else Colors.GREEN.value
            item_surf = self.item_font.render(text, True, color)
            item_rect = item_surf.get_rect(center=(overlay_rect.centerx, overlay_rect.centery + 50 + i * 40))
            self.screen.blit(item_surf, item_rect)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.selected][1]
        return GameState.STAY
    

