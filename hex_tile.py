# hex_tile.py

from enum import Enum


class LightState(Enum):
    GREEN = 'green'
    RED = 'red'
    ORANGE = 'orange'


class HexTile:
    def __init__(self, q: int, r: int):
        self.q = q
        self.r = r
        self.built_tracks: set[tuple[str, int]] = set()  # set of (type, dir)
        self.lights: list[LightState] = [LightState.RED] * 6  # Initialize all edges with red lights

    def add_track(self, track_type: str, dir: int) -> bool:
        """Add a track. Returns True if successful, False if it would overlap."""
        if dir < 0 or dir >= 6:
            raise ValueError(f"Direction must be between 0 and 5, got {dir}")
        track = (track_type, dir)
        if track in self.built_tracks:
            return False  # Track already exists, can't build here
        self.built_tracks.add(track)
    
        # Update light states for the involved edges
        self._update_lights_for_new_track(track_type, dir)

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
