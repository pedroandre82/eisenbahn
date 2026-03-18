# tracks.py

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
                       

def draw_hex(surface, center: Vector2, size, color, line_width=1):
    points = []
    point_vector = pygame.math.Vector2(1, 0).rotate(30) * size  # Start at 30 degrees for pointy-top hex
    for _ in range(6):
        points.append(center + point_vector)
        point_vector.rotate_ip(60)
    pygame.draw.polygon(surface, color, points, line_width)


def straight_track(surface, center: Vector2, size, direction):
    # Vector along the line
    c = Vector2(size * math.sqrt(3) / 2, 0).rotate(direction * 60)

    # Endpoints of the line
    p1 = center - c
    p2 = center + c

    # Unit perpendicular vector
    perp = c.rotate(90).normalize()

    # First polygon (outer/base)
    half_width = size // 4  # since line width was size//2
    offset = perp * half_width
    points_base = [p1 - offset, p1 + offset, p2 + offset, p2 - offset]
    pygame.draw.polygon(surface, COLOR_BASE, points_base)

    # Second polygon (inner/track)
    half_width = size // 8  # since line width was size//4
    offset = perp * half_width
    points_track = [p1 - offset, p1 + offset, p2 + offset, p2 - offset]
    pygame.draw.polygon(surface, COLOR_TRACK, points_track)


def curved_track(surface, center: Vector2, size, direction):
    center_vector = Vector2(0, size).rotate(60) + Vector2(0, size)
    center_vector.rotate_ip(direction * 60)
    start_angle = 330 + direction * 60
    end_angle = 270 + direction * 60
    radius = 3 * size // 2
    draw_arc(surface, center + center_vector, radius, start_angle, end_angle, COLOR_BASE, size // 2)
    draw_arc(surface, center + center_vector, radius, start_angle, end_angle, COLOR_TRACK, size // 4)


def straight_cursor(surface, center: Vector2, size, direction):
    c = Vector2(size * math.sqrt(3) / 2, 0).rotate(direction * 60)
    pygame.draw.line(surface, COLOR_SIDE, center - c, center + c, 4)


def curved_cursor(surface, center: Vector2, size, direction):
    center_vector = Vector2(0, size).rotate(60) + Vector2(0, size)
    center_vector.rotate_ip(direction * 60)
    start_angle = 330 + direction * 60
    end_angle = 270 + direction * 60
    radius = 3 * size // 2
    draw_arc(surface, center + center_vector, radius, start_angle, end_angle, COLOR_SIDE, 4)

