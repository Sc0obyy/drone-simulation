import numpy as np
import matplotlib.pyplot as plt
import settings

def rotate_point(x: float, y: float, cx: float, cy: float, angle: float) -> (int, int):
    """
    Rotate a point (x, y) around a center (cx, cy) by angle (in degrees).
    """
    theta = np.radians(angle)
    cos_t, sin_t = np.cos(theta), np.sin(theta)
    x_shifted, y_shifted = x - cx, y - cy
    x_rot = cos_t * x_shifted - sin_t * y_shifted + cx
    y_rot = sin_t * x_shifted + cos_t * y_shifted + cy
    return int(round(x_rot)), int(round(y_rot))

def value_to_color(value: float, cmap_name: str = "plasma", alpha: int = 255) -> tuple:
    """
    Map a numeric value to an RGBA color using a matplotlib colormap.
    """
    norm = (value * 10) / 100 if value > 0 else value / 100
    norm = np.clip(norm, 0, 1)
    cmap = plt.get_cmap(cmap_name)
    r, g, b, _ = cmap(norm)
    return (int(r * 255), int(g * 255), int(b * 255), alpha)

def to_screen_coords(pos: tuple) -> tuple:
    return (int(pos[0] + settings.CENTER_X), int(-pos[1] + settings.CENTER_Y))

def to_world_coords(pos: tuple) -> tuple:
    return (int(pos[0] + settings.CENTER_X), int(pos[1] + settings.CENTER_Y))