# hex_tile.py

import pygame
from enum import Enum
from tracks import straight_track, curved_track
from constants import Colors

class LightState(Enum):
    GREEN = 'green'
    RED = 'red'
    ORANGE = 'orange'


class HexTile:
    def __init__(self, q: int, r: int):
        self.q = q
        self.r = r
        self.tracks: list[tuple[str, int]] = []  # list of (type, dir)
        self.lights: list[LightState] = [LightState.RED] * 6  # Initialize all edges with red lights
        self.active_track: int = -1
        self.active_edges: set[tuple[int, int]] = set()

    def add_track(self, track_type: str, dir: int) -> bool:
        """Add a track. Returns True if successful, False if it would overlap."""
        if dir < 0 or dir >= 6:
            raise ValueError(f"Direction must be between 0 and 5, got {dir}")
        track = (track_type, dir)
        if track in self.tracks:
            return False  # Track already exists, can't build here
        self.tracks.append(track)
    
        # Update light states for the involved edges
        self._update_lights_for_new_track(track_type, dir)

        # Set new track as active
        self.active_track = len(self.tracks) - 1
        self.active_edges = {(dir, (dir + 3 if track_type == 'straight' else 2) % 6)}
        # TODO: Put tracks in the correct order

        return True

    def _update_lights_for_new_track(self, track_type: str, dir: int) -> None:
        self.lights[dir] = LightState.GREEN
        if track_type == 'straight':
            opposite_dir = (dir + 3) % 6
            self.lights[opposite_dir] = LightState.GREEN
        elif track_type == 'curved':
            next_dir = (dir + 2) % 6
            self.lights[next_dir] = LightState.GREEN
            
    def set_light(self, dir: int, state: LightState) -> None:
        self.lights[dir % 6] = state

    def get_light(self, dir: int) -> LightState:
        return self.lights[dir % 6]
    
    def cycle_track(self):
        if not self.tracks:
            return
        self.active_track = (self.active_track + 1) % len(self.tracks)
        track = self.tracks[self.active_track]
        self.active_edges = {(track[1], (track[1] + 3 if track[0] == 'straight' else 4) % 6)}

    def draw_tracks(self, surface: pygame.Surface, center: pygame.math.Vector2, size: int):
        """Draw the tracks on the hex tile. The active track is drawn last."""
        if not self.tracks:
            return
        for i in range(self.active_track + 1, len(self.tracks) + self.active_track + 1):
            track_type, dir = self.tracks[i % len(self.tracks)]
            if track_type == 'straight':
                straight_track(surface, center, size, dir)
            elif track_type == 'curved':
                curved_track(surface, center, size, dir)

    def draw_hex_border(self, surface: pygame.Surface, center: pygame.math.Vector2, size: int, color: Colors, line_width = 1):
        """Draw the border of the hex tile."""
        points = []
        point_vector = pygame.math.Vector2(1, 0).rotate(30) * size  # Start at 30 degrees for pointy-top hex
        for _ in range(6):
            points.append(center + point_vector)
            point_vector.rotate_ip(60)
        pygame.draw.polygon(surface, color.value, points, line_width)
