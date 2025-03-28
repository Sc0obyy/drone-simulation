import pygame
import numpy as np
import settings
from sim.utils import rotate_point, value_to_color, to_screen_coords

class Coverage:
    """
    Class to manage and calculate coverage and overlap on a 2D grid.
    """

    def __init__(self):
        """
        Initializes the coverage map with NaN values.
        """
        self.coverage_map = np.empty([settings.WIDTH, settings.HEIGHT])
        self.coverage_map[:] = np.nan

    def add_rectangle_boundary_to_coverage_map_n(self, min_x: int, max_x: int, min_y: int, max_y: int) -> None:
        """
        Adds a rectangular boundary to the coverage map.

        Args:
            min_x (int): Minimum x-coordinate of the rectangle.
            max_x (int): Maximum x-coordinate of the rectangle.
            min_y (int): Minimum y-coordinate of the rectangle.
            max_y (int): Maximum y-coordinate of the rectangle.
        """
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                self.coverage_map[int(x), int(y)] = 0

    def add_circle_boundary_to_coverage_map_n(self, x: float, y: float, radius: float) -> None:
        """
        Adds a circular boundary to the coverage map.

        Args:
            x (float): x-coordinate of the circle center.
            y (float): y-coordinate of the circle center.
            radius (float): Radius of the circle.
        """
        point = (x, y)
        point = to_screen_coords(point)
        x, y = point
        for i in range(int(x - radius), int(x + radius) + 1):
            for j in range(int(y - radius), int(y + radius) + 1):
                if (i - x) ** 2 + (j - y) ** 2 <= radius ** 2:
                    self.coverage_map[int(i), int(j)] = 0

    def add_photos_to_coverage_map_n(self, photos: list) -> None:
        """
        Adds photos to the coverage map.

        Args:
            photos (list): List of photos, each represented by a tuple (center, angle).
        """
        for photo in photos:
            center = photo[0]
            center = to_screen_coords(center)
            half_size = settings.PHOTO_SIZE // 2
            photo_array = np.empty((settings.PHOTO_SIZE, settings.PHOTO_SIZE), dtype=object)
            for i in range(settings.PHOTO_SIZE):
                for j in range(settings.PHOTO_SIZE):
                    x = center[0] - half_size + i
                    y = center[1] - half_size + j
                    photo_array[i, j] = (x, y)
            angle = photo[1]
            rotated_photo = [rotate_point(x, y, center[0], center[1], angle) for x, y in photo_array.flat]
            for p in rotated_photo:
                x, y = p
                if self.coverage_map[int(x), int(y)] >= 0:
                    self.coverage_map[int(x), int(y)] += 1

    def calculate_coverage_n(self, screen) -> None:
        """
        Calculates and displays the coverage percentage on the screen.

        Args:
            screen: Pygame screen object to draw the coverage.
        """
        area = 0
        coverCount = 0
        for (i, j), value in np.ndenumerate(self.coverage_map):
            if value >= 0:
                area += 1
            if value > 0:
                coverCount += 1
                color = value_to_color(value)
                pygame.draw.rect(screen, color, (i, j, 1, 1))
        coverage = int((coverCount / area) * 100)
        print(f"Coverage: {coverage}%")

    def calculate_overlap_n(self) -> None:
        """
        Calculates and displays the overlap percentage.
        """
        coveredArea = 0
        overlapCount = 0
        for (i, j), value in np.ndenumerate(self.coverage_map):
            if value == 1:
                coveredArea += 1
            if value > 1:
                coveredArea += 1
                overlapCount += 1
        overlap = int((overlapCount / coveredArea) * 100) if overlapCount != 0 else 0
        print(f"Overlap: {overlap}%")
        pygame.display.update()