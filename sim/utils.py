import numpy as np
import matplotlib.pyplot as plt
import settings

def rotate_point(x: float, y: float, cx: float, cy: float, angle: float) -> tuple:
    """
    Rotate a point (x, y) around a center (cx, cy) by a given angle.

    Parameters:
    x (float): The x-coordinate of the point to rotate.
    y (float): The y-coordinate of the point to rotate.
    cx (float): The x-coordinate of the center of rotation.
    cy (float): The y-coordinate of the center of rotation.
    angle (float): The angle in degrees to rotate the point.

    Returns:
    tuple: The new coordinates of the rotated point as (x_rot, y_rot).
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

    Parameters:
    value (float): The numeric value to map to a color.
    cmap_name (str): The name of the colormap to use. Default is "plasma".
    alpha (int): The alpha value for the color. Default is 255.

    Returns:
    tuple: The RGBA color as a tuple (r, g, b, a).
    """
    norm = (value * 10) / 100 if value > 0 else value / 100
    norm = np.clip(norm, 0, 1)
    cmap = plt.get_cmap(cmap_name)
    r, g, b, _ = cmap(norm)
    return (int(r * 255), int(g * 255), int(b * 255), alpha)

def to_screen_coords(pos: tuple) -> tuple:
    """
    Convert simulation coordinates to screen coordinates.

    Parameters:
    pos (tuple): The position in simulation coordinates as (x, y).

    Returns:
    tuple: The position in screen coordinates as (x_screen, y_screen).
    """
    return (int(pos[0] + settings.CENTER_X), int(-pos[1] + settings.CENTER_Y))

def custom_print(*args, **kwargs):
    """
    Custom print function that prints output based on a setting.

    Parameters:
    *args: Variable length argument list to pass to the print function.
    **kwargs: Arbitrary keyword arguments to pass to the print function.
    """
    if settings.PRINT_OUTPUT:
        print(*args, **kwargs)
