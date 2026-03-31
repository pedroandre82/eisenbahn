# hex_grid.py
import math

import pygame
from constants import Colors
from hex_tile import HexTile

HEX_SIZE = 36          # radius (center to corner)
GRID_ORIGIN_X = 340    # left border of hex area
GRID_ORIGIN_Y = 0      # top border of hex area

GRID_COLS = 15
GRID_ROWS = 13

def oddr_to_pixel(col, row):
    """
    Odd-r horizontal layout (pointy-top).
    (0,0) is top-left hex.
    """
    size = HEX_SIZE
    w = math.sqrt(3) * size      # horizontal distance between columns
    h = 1.5 * size               # vertical distance between rows

    x = GRID_ORIGIN_X + size * math.sqrt(3) * (col + 0.5 * (row & 1))
    y = GRID_ORIGIN_Y + size * (1 + 1.5 * row)
    return x, y

def pixel_to_oddr(px, py):
    """
    pixel -> (col,row) in odd-r.
    """
    size = HEX_SIZE
    # shift into grid space
    x = px - GRID_ORIGIN_X
    y = py - (GRID_ORIGIN_Y + size)

    # axial estimate
    q = (math.sqrt(3)/3 * x - 1.0/3 * y) / size
    r = (2.0/3 * y) / size

    # cube rounding
    col_ax, row_ax = axial_round(q, r)

    # convert axial (q,r) to odd-r row/col
    col = col_ax + (row_ax - (row_ax & 1)) // 2
    row = row_ax
    return col, row

def axial_round(q, r):
    s = -q - r
    rq = round(q)
    rr = round(r)
    rs = round(s)

    dq = abs(rq - q)
    dr = abs(rr - r)
    ds = abs(rs - s)

    if dq > dr and dq > ds:
        rq = -rr - rs
    elif dr > ds:
        rr = -rq - rs
    else:
        rs = -rq - rr

    return int(rq), int(rr)


def draw_hex(surface, center: pygame.math.Vector2, size, color: Colors, line_width=1):
    points = []
    point_vector = pygame.math.Vector2(1, 0).rotate(30) * size  # Start at 30 degrees for pointy-top hex
    for _ in range(6):
        points.append(center + point_vector)
        point_vector.rotate_ip(60)
    pygame.draw.polygon(surface, color.value, points, line_width)


class GridManager:
    def __init__(self, grid_size: tuple[int, int]):
        self.grid_size = grid_size
        self.grid: list[list[HexTile]] = [[HexTile() for row in range(grid_size[1])] for col in range(grid_size[0])]
        
        self.city_tiles: set[tuple[int, int]] = set()
        self._set_city_tiles()
            
            
    def _set_city_tiles(self):
        for coord in [(0, row) for row in range(0, 13, 2)]:
            self.city_tiles.add(coord)
        for coord in [(14, row) for row in range(1, 13, 2)]:
            self.city_tiles.add(coord)

    def tile_is_city(self, col: int, row: int) -> bool:
        return (col, row) in self.city_tiles
        

    def get_tile(self, col: int, row: int) -> HexTile:
        if 0 <= col < self.grid_size[0] and 0 <= row < self.grid_size[1]:
            return self.grid[col][row]
        else:
            raise IndexError(f"Tile coordinates out of bounds {col=}, {row=}")
        
    def set_tile(self, col: int, row: int, tile: HexTile):
        if 0 <= col < self.grid_size[0] and 0 <= row < self.grid_size[1]:
            self.grid[col][row] = tile
        else:
            raise IndexError(f"Tile coordinates out of bounds {col=}, {row=}")

    def neighbor_in_direction(self, col: int, row: int, direction: int) -> tuple[int, int] | None:
        if row & 1:  # odd row
            dirs = [(-1, 0), (0, -1), (+1, -1), (+1, 0), (+1, +1), (0, +1)]
        else:        # even row
            dirs = [(-1, 0), (-1, -1), (0, -1), (+1, 0), (0, +1), (-1, +1)]

        dc, dr = dirs[direction % 6]
        nc, nr = col + dc, row + dr
        if 0 <= nc < GRID_COLS and 0 <= nr < GRID_ROWS:
            return nc, nr
        return None
    
    def draw_grid(self, surface: pygame.Surface, color: Colors = Colors.CYAN):
        for col in range(GRID_COLS):
            for row in range(GRID_ROWS):
                cx, cy = oddr_to_pixel(col, row)
                center = pygame.math.Vector2(cx, cy)
                draw_hex(surface, center, HEX_SIZE, color)

    def draw_tracks(self, surface: pygame.Surface):
        for col in range(GRID_COLS):
            for row in range(GRID_ROWS):
                tile = self.get_tile(col, row)
                cx, cy = oddr_to_pixel(col, row)
                center = pygame.math.Vector2(cx, cy)
                tile.draw_tracks(surface, center, HEX_SIZE)

    def highlight_tile(self, surface: pygame.Surface, col: int, row: int, color: Colors = Colors.ORANGE, line_width: int = 2):
        cx, cy = oddr_to_pixel(col, row)
        center = pygame.math.Vector2(cx, cy)
        draw_hex(surface, center, HEX_SIZE, color, line_width=line_width)

