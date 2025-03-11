import pygame
import settings
from sim.utils import value_to_color, to_screen_coords
from sim.coverage import Coverage

class DroneRenderer:
    """
    A class to render the drone simulation using Pygame.
    
    Attributes:
        flight (DroneFlight): The flight object controlling the drone, containing photos, path, and position.
        screen: The Pygame display surface.
        boundary_shape: The shape of the boundary (circle or rectangle).
        boundary_params: The parameters defining the boundary.
        coverage: The coverage object to calculate coverage and overlap.
    """
    def __init__(self, flight):
        """
        Initializes the DroneRenderer with flight data and Pygame settings.
        
        Args:
            flight (DroneFlight): The flight object controlling the drone, containing photos, path, and position.
        """
        self.flight = flight
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption("Drone Simulation")
        self.boundary_shape = settings.BOUNDARY_SHAPE
        self.boundary_params = settings.BOUNDARY_PARAMS
        self.coverage = Coverage()
    
    def draw(self) -> None:
        """
        Draws the entire simulation including photos, path, drone, and boundary.
        """
        self.screen.fill(settings.BACKGROUND_COLOR)
        self.draw_photos()
        self.draw_path()
        self.draw_drone()
        self.draw_boundary()
        pygame.display.update()

    def draw_photos(self) -> None:
        """
        Draws the photos taken by the drone on the screen.
        """
        for photo in self.flight.photos:
            surf = pygame.Surface((settings.PHOTO_SIZE, settings.PHOTO_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(surf, settings.PHOTO_COLOR, (0, 0, settings.PHOTO_SIZE, settings.PHOTO_SIZE))
            rot_surf = pygame.transform.rotate(surf, photo[1] * -1)
            rot_rect = rot_surf.get_rect(center=to_screen_coords(photo[0]))
            self.screen.blit(rot_surf, rot_rect.topleft)

    def draw_path(self) -> None:
        """
        Draws the path of the drone on the screen.
        """
        for point in self.flight.path:
            pygame.draw.circle(self.screen, settings.PATH_COLOR, to_screen_coords(point), 1)

    def draw_drone(self) -> None:
        """
        Draws the current position of the drone on the screen.
        """
        pygame.draw.circle(self.screen, (0, 0, 0), to_screen_coords(self.flight.position), 1)

    def draw_boundary(self) -> None:
        """
        Draws the boundary of the simulation area on the screen.
        """
        if self.boundary_shape == 'circle':
            self.draw_circle_boundary()
        elif self.boundary_shape == 'rectangle':
            self.draw_rectangle_boundary()

    def draw_circle_boundary(self) -> None:
        """
        Draws a circular boundary on the screen and updates the coverage map.
        """
        circle_center = to_screen_coords((self.boundary_params.get('x'), self.boundary_params.get('y')))
        circle_radius = self.boundary_params.get('radius')
        pygame.draw.circle(self.screen, (255, 0, 0), circle_center, circle_radius, 1)
        self.coverage.add_circle_boundary_to_coverage_map_n(self.boundary_params.get('x'),
                                                       self.boundary_params.get('y'),
                                                       circle_radius)
        
    def draw_rectangle_boundary(self) -> None:
        """
        Draws a rectangular boundary on the screen and updates the coverage map.
        """
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
        self.coverage.add_rectangle_boundary_to_coverage_map_n(min_x, max_x, min_y, max_y)

    def draw_colorbar(self, x: int, y: int, width: int, height: int, min_val: int = 1, max_val: int = 10, cmap_name: str = "plasma") -> None:
        """
        Draws a colorbar on the screen to represent image count.
        
        Args:
            x: The x-coordinate of the colorbar.
            y: The y-coordinate of the colorbar.
            width: The width of the colorbar.
            height: The height of the colorbar.
            min_val: The minimum value of the colorbar.
            max_val: The maximum value of the colorbar.
            cmap_name: The name of the colormap to use.
        """
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

    def print_info(self) -> None:
        """
        Prints the flight information and calculates coverage and overlap.
        """
        minutes = int(self.flight.flight_time // 60)
        seconds = int(self.flight.flight_time % 60)
        print("\n################################\n")
        print(f"Total flight time: {minutes} Minutes, {seconds} Seconds")
        self.coverage.add_photos_to_coverage_map_n(self.flight.photos)
        self.coverage.calculate_coverage_n(self.screen)
        self.coverage.calculate_overlap_n()
        print("\n################################\n")

    def wait_for_exit(self) -> None:
        """
        Waits for the user to press any key to exit the simulation.
        """
        print("Simulation complete. Press any key to exit...")
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
