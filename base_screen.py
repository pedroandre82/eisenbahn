# from abc import ABC, abstractmethod
import pygame
from constants import GameState


class BaseScreen:
    """Base class for all game screens."""

    def __init__(self, screen):
        self.screen = screen
    
    # @abstractmethod
    def handle_events(self, events) -> GameState:
        """Process events and return next GameState if changing, else None."""
        for event in events:
            if event.type == pygame.QUIT:
                return GameState.QUIT
        return GameState.STAY  # Indicate no state change by default
    
    # @abstractmethod
    def update(self):
        """Update screen logic (e.g., timers). Return next state or None."""
        pass
    
    # @abstractmethod
    def draw(self):
        """Draw to self.screen."""
        pass
