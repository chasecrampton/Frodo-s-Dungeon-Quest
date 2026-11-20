
import numpy as np
from typing import Any
def _get_line_tiles(start_r: int, start_c: int, dir_r: int, dir_c: int, radius: int) -> list[tuple[int, int]]:
    """AI-assisted. Generates coordinates for a straight line attack."""
    return [(start_r + (dir_r * step), start_c + (dir_c * step)) for step in range(1, radius + 1)]

def _get_circle_tiles(start_r: int, start_c: int, radius: int) -> list[tuple[int, int]]:
    """AI-assisted. Generates coordinates for a radial burst attack using Manhattan distance."""
    affected = []
    for r in range(start_r - radius, start_r + radius + 1):
        for c in range(start_c - radius, start_c + radius + 1):
            if abs(start_r - r) + abs(start_c - c) <= radius: 
                affected.append((r, c))
    return affected

def _get_cone_tiles(start_r: int, start_c: int, dir_r: int, dir_c: int, radius: int) -> list[tuple[int, int]]:
    """AI-assisted. Generates coordinates for an expanding cone attack."""
    affected = []
    for step in range(1, radius + 1):
        center_r, center_c = start_r + (dir_r * step), start_c + (dir_c * step)
        affected.append((center_r, center_c))
        if dir_r != 0: 
            for width in range(1, step + 1):
                affected.extend([(center_r, center_c + width), (center_r, center_c - width)])
        else:          
            for width in range(1, step + 1):
                affected.extend([(center_r + width, center_c), (center_r - width, center_c)])
    return affected

def get_aoe_tiles(start_pos: np.ndarray, direction_vec: np.ndarray, area_type: str, radius: int, level_map: list[list[Any]]) -> list[tuple[int, int]]:
    """AI-assisted. Calculates affected tiles for cone, line, or circle spell shapes."""
    start_r, start_c = int(start_pos[0]), int(start_pos[1])
    dir_r, dir_c = int(direction_vec[0]), int(direction_vec[1])

    if area_type == "line":
        affected = _get_line_tiles(start_r, start_c, dir_r, dir_c, radius)
    elif area_type == "circle":
        affected = _get_circle_tiles(start_r, start_c, radius)
    elif area_type == "cone":
        affected = _get_cone_tiles(start_r, start_c, dir_r, dir_c, radius)
    else:
        affected = []

    # Filter out out-of-bounds tiles
    return [(r, c) for r, c in affected if 0 <= r < len(level_map) and 0 <= c < len(level_map[0])]