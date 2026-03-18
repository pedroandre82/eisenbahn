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
        self.built_tracks: set[frozenset[int]] = set()  # set of (from_dir, to_dir)
        self.lights: list[LightState] = [LightState.RED] * 6  # Initialize all edges with red lights

    def add_track(self, dir1: int, dir2: int) -> bool:
        """Add a track from from_dir to to_dir. Returns True if successful, False if it would overlap."""
        dir1 = dir1 % 6
        dir2 = dir2 % 6
        if dir1 == dir2:
            raise ValueError("from_dir and to_dir cannot be the same")
        track = frozenset({dir1, dir2})
        if track in self.built_tracks:
            return False  # Track already exists, can't build here
        self.built_tracks.add(track)
    
        # Update light states for the involved edges
        self._update_lights_for_new_track(dir1, dir2)

        return True

    def _update_lights_for_new_track(self, dir1: int, dir2: int) -> None:
        self.lights[dir1] = LightState.GREEN
        self.lights[dir2] = LightState.GREEN

    def set_light(self, dir: int, state: LightState) -> None:
        self.lights[dir % 6] = state
