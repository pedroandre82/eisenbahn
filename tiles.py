import math
import pygame
from pygame.math import Vector2

COLOR_BASE = "#CCCCCC"
COLOR_SIDE = "#C83737"
COLOR_TRACK = "#483e37"


def draw_arc(surface, center: Vector2, radius, start_angle, end_angle, color, line_width):
    """Translate start_angle and end_angle from degrees to radians and adjust for pygame's coordinate system."""

    start_rad = math.radians(-start_angle)
    end_rad = math.radians(-end_angle)
    rect = pygame.Rect(0, 0, radius * 2 + line_width, radius * 2 + line_width)
    rect.center = center
    pygame.draw.arc(surface, color, rect, start_rad, end_rad, line_width)
                       

def draw_hex(surface, center: Vector2, size, color):
    points = []
    point_vector = pygame.math.Vector2(1, 0).rotate(30) * size  # Start at 30 degrees for pointy-top hex
    for _ in range(6):
        points.append(center + point_vector)
        point_vector.rotate_ip(60)
    pygame.draw.polygon(surface, color, points, 1)


def straight_track(surface, center: Vector2, size):
    c = Vector2(size, 0).rotate(30)
    
    color = COLOR_BASE
    base_width = size // 2  # 12
    x = Vector2(c.x, 0)
    pygame.draw.line(surface, color, center - x, center + x, base_width)

    color = COLOR_SIDE
    side_width = size // 12  # 2
    offset = base_width // 2 - side_width // 2
    x1 = Vector2(-c.x, offset)
    x2 = Vector2(c.x, offset)
    pygame.draw.line(surface, color, center + x1, center + x2, side_width)
    pygame.draw.line(surface, color, center - x2, center - x1, side_width)

    color = COLOR_TRACK
    track_width = size // 4  # 6
    pygame.draw.line(surface, color, center - x, center + x, track_width)


def curved_track(surface, center: Vector2, size, direction):
    center_point = center + Vector2(0, size).rotate(60) + Vector2(0, size)
    start_angle = 330 + direction * 60
    end_angle = 270 + direction * 60
    
    side_width = size // 9
    track_width = size // 2  - side_width // 2
    base_width = size // 18

    color = COLOR_TRACK
    track_radius = 3 * size // 2
    draw_arc(surface, center_point, track_radius, start_angle, end_angle, color, track_width)

    color = COLOR_SIDE
    inner_side_radius = track_radius - track_width // 2 + side_width // 2
    draw_arc(surface, center_point, inner_side_radius, start_angle, end_angle, color, side_width)
    outter_side_radius = inner_side_radius + track_width
    draw_arc(surface, center_point, outter_side_radius, start_angle, end_angle, color, side_width)

    color = COLOR_BASE
    inner_base_radius = inner_side_radius + side_width // 2
    draw_arc(surface, center_point, inner_base_radius, start_angle, end_angle, color, base_width)
    outter_base_radius = outter_side_radius - side_width // 2
    draw_arc(surface, center_point, outter_base_radius, start_angle, end_angle, color, base_width)
    
