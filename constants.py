from enum import Enum


# WINDOW SIZE
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

GAME_FPS = 60


class GameState(Enum):
    """Game screen states matching our flowchart."""
    SPLASH = "splash"
    MAIN_MENU = "main_menu"
    SETTINGS = "settings"
    CREDITS = "credits"
    GAMEPLAY = "gameplay"
    PAUSE = "pause"
    WIN = "win"
    LOSE = "lose"
    QUIT = "quit"
    STAY = "stay"  # Special state to indicate no change


class MainMenuOption(Enum):
    """Options in the main menu."""
    START_GAME = "Start Game"
    SETTINGS = "Settings"
    CREDITS = "Credits"
    QUIT = "Quit"
