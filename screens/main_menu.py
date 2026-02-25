import pygame
from base_screen import BaseScreen
from constants import GameState


class MainMenuScreen(BaseScreen):
    """Main menu screen with options to start game, settings, credits, etc."""

    def __init__(self, screen):
        super().__init__(screen)

    