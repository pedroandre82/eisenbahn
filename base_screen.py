# from abc import ABC, abstractmethod
import pygame
from constants import GameState


class BaseScreen:
    """Base class for all game screens."""

    def __init__(self, screen):
        self.screen = screen
    
    # @abstractmethod
    def handle_events(self, events) -> GameState | None:
        """Process events and return next GameState if changing, else None."""
        for event in events:
            if event.type == pygame.QUIT:
                return GameState.QUIT
        return None
    
    # @abstractmethod
    def update(self) -> GameState | None:
        """Update screen logic (e.g., timers). Return next state or None."""
        return None
    
    # @abstractmethod
    def draw(self):
        """Draw to self.screen."""
        pass
