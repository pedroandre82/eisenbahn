# hex_grid.py
import math
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


class GridManager:
    def __init__(self, grid_size: tuple[int, int]):
        self.grid_size = grid_size
        self.grid: list[list[HexTile]] = [[HexTile(col, row) for row in range(grid_size[1])] for col in range(grid_size[0])]

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
