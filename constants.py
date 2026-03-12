# constants.py

from enum import Enum

GAME_TITLE = "EISENBAHN"

# WINDOW SIZE
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

GAME_FPS = 60


class Colors(Enum):
    BLACK = "#04151F"  # INK_BLACK
    GREEN = "#183A37"  # DARK GREEN
    WHITE = "#EFD6AC"  # WHEAT
    ORANGE = "#C44900"
    CYAN = "#62929E"  # PACIFIC_CYAN


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
