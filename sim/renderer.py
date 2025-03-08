import pygame
import numpy as np
import matplotlib.pyplot as plt
import settings
from sim.utils import rotate_point, value_to_color, to_screen_coords, to_world_coords

class DroneRenderer:
    def __init__(self, flight):
        self.flight = flight
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption("Drone Simulation")
        self.boundary_shape = settings.BOUNDRY_SHAPE
        self.boundary_params = settings.BOUNDRY_PARAMS
        self.coverage_map = np.empty([settings.WIDTH, settings.HEIGHT])
        self.coverage_map[:] = np.nan

    # def to_screen_coords(self, pos: tuple) -> tuple:
    #     return (int(pos[0] + settings.CENTER_X), int(-pos[1] + settings.CENTER_Y))

    # def to_world_coords(self, pos: tuple) -> tuple:
    #     return (int(pos[0] + settings.CENTER_X), int(pos[1] + settings.CENTER_Y))
    
    def draw(self) -> None:
        self.screen.fill(settings.BACKGROUND_COLOR)
        self.draw_photos()
        self.draw_path()
        self.draw_drone()
        self.draw_boundary()
        pygame.display.update()

    def draw_photos(self) -> None:
        for photo in self.flight.photos:
            surf = pygame.Surface((settings.PHOTO_SIZE, settings.PHOTO_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(surf, settings.PHOTO_COLOR, (0, 0, settings.PHOTO_SIZE, settings.PHOTO_SIZE))
            rot_surf = pygame.transform.rotate(surf, photo[1] * -1)
            rot_rect = rot_surf.get_rect(center=to_screen_coords(photo[0]))
            self.screen.blit(rot_surf, rot_rect.topleft)

    def draw_path(self) -> None:
        for point in self.flight.path:
            pygame.draw.circle(self.screen, settings.PATH_COLOR, to_screen_coords(point), 1)

    def draw_drone(self) -> None:
        pygame.draw.circle(self.screen, (0, 0, 0), to_screen_coords(self.flight.position), 1)

    def draw_boundary(self) -> None:
        if self.boundary_shape == 'circle':
            self.draw_circle_boundary()
        elif self.boundary_shape == 'rectangle':
            self.draw_rectangle_boundary()

    def draw_circle_boundary(self) -> None:
        circle_center = to_screen_coords((self.boundary_params.get('x'), self.boundary_params.get('y')))
        circle_radius = self.boundary_params.get('radius')
        pygame.draw.circle(self.screen, (255, 0, 0), circle_center, circle_radius, 1)
        self.add_circle_boundary_to_coverage_map(self.boundary_params.get('x'),
                                                   self.boundary_params.get('y'),
                                                   circle_radius)
        
    def draw_rectangle_boundary(self) -> None:
        rectangle_vertices = [
            self.boundary_params.get('v1'),
            self.boundary_params.get('v2'),
            self.boundary_params.get('v3'),
            self.boundary_params.get('v4')
        ]
        screen_rect_vertices = [to_screen_coords(v) for v in rectangle_vertices]
        min_x = min(v[0] for v in screen_rect_vertices)
        max_y = max(v[1] for v in screen_rect_vertices)
        max_x = max(v[0] for v in screen_rect_vertices)
        min_y = min(v[1] for v in screen_rect_vertices)
        pygame.draw.rect(self.screen, (255, 0, 0), (min_x, min_y, (max_x - min_x), (max_y - min_y)), 1)
        self.add_rectangle_boundary_to_coverage_map(min_x, max_x, min_y, max_y)

    def add_rectangle_boundary_to_coverage_map(self, min_x: int, max_x: int, min_y: int, max_y: int) -> None:
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                self.coverage_map[int(x), int(y)] = 0

    def add_circle_boundary_to_coverage_map(self, x: float, y: float, radius: float) -> None:
        point = (x, y)
        point = to_world_coords(point)
        x, y = point
        for i in range(int(x - radius), int(x + radius) + 1):
            for j in range(int(y - radius), int(y + radius) + 1):
                if (i - x) ** 2 + (j - y) ** 2 <= radius ** 2:
                    self.coverage_map[int(i), int(j)] = 0

    def add_photos_to_coverage_map(self) -> None:
        for photo in self.flight.photos:
            center = photo[0]
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
                p = to_world_coords(p)
                x, y = p
                if self.coverage_map[int(x), int(y)] >= 0:
                    self.coverage_map[int(x), int(y)] += 1

    def calculate_coverage(self) -> None:
        area = 0
        coverCount = 0
        for (i, j), value in np.ndenumerate(self.coverage_map):
            if value >= 0:
                area += 1
            if value > 0:
                coverCount += 1
                color = value_to_color(value)
                pygame.draw.rect(self.screen, color, (i, j, 1, 1))
        coverage = int((coverCount / area) * 100)
        print(f"Coverage: {coverage}%")

    def draw_colorbar(self, x: int, y: int, width: int, height: int, min_val: int = 1, max_val: int = 10, cmap_name: str = "plasma") -> None:
        pygame.font.init()
        title = pygame.font.SysFont("Arial", 20).render("Image count", True, (0, 0, 0))
        self.screen.blit(title, (x, y - 25))
        ten = pygame.font.SysFont("Arial", 20).render(" - 10", True, (0, 0, 0))
        self.screen.blit(ten, (x + width, y))
        one = pygame.font.SysFont("Arial", 20).render(" - 1", True, (0, 0, 0))
        self.screen.blit(one, (x + width, y + height - 20))
        for j in range(height):
            value = min_val + ((height - j) / height) * (max_val - min_val)
            color = value_to_color(value, cmap_name)
            pygame.draw.line(self.screen, color, (x, y + j), (x + width, y + j))

    def calculate_overlap(self) -> None:
        coveredArea = 0
        overlapCount = 0
        for (i, j), value in np.ndenumerate(self.coverage_map):
            if value == 1:
                coveredArea += 1
            if value > 1:
                overlapCount += 1
        overlap = int((coveredArea / overlapCount) * 100) if overlapCount != 0 else 0
        print(f"Overlap: {overlap}%")
        pygame.display.update()

    def print_info(self) -> None:
        minutes = int(self.flight.flight_time // 60)
        seconds = int(self.flight.flight_time % 60)
        print(f"Total flight time: {minutes} Minutes, {seconds} Seconds")
        self.add_photos_to_coverage_map()
        self.calculate_coverage()
        self.calculate_overlap()

    def wait_for_exit(self) -> None:
        print("Simulation complete. Press any key to exit...")
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False