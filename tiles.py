# tiles.py

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
    c = Vector2(size * math.sqrt(3) / 2, 0).rotate(direction * 60)
    pygame.draw.line(surface, COLOR_BASE, center - c, center + c, size // 2)
    pygame.draw.line(surface, COLOR_TRACK, center - c, center + c, size // 4)


def curved_track(surface, center: Vector2, size, direction):
    center_point = center + Vector2(0, size).rotate(60) + Vector2(0, size)
    center_point.rotate_ip(direction * 60)
    start_angle = 330 + direction * 60
    end_angle = 270 + direction * 60
    radius = 3 * size // 2
    draw_arc(surface, center_point, radius, start_angle, end_angle, COLOR_BASE, size // 2)
    draw_arc(surface, center_point, radius, start_angle, end_angle, COLOR_TRACK, size // 4)
