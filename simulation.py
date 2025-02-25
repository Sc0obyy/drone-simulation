import pygame
import numpy as np
import time
import math
import matplotlib.pyplot as plt

import scipy.ndimage

np.set_printoptions(threshold=np.inf)

# Constants
WIDTH, HEIGHT = 1600, 600
BACKGROUND_COLOR = (220, 220, 220)
DRONE_RADIUS = 1
DRONE_COLOR = (0, 0, 0)
PATH_COLOR = (255, 255, 0)
FPS = 30
PHOTO_COLOR = (255, 0, 0, 25)
PHOTO_SIZE = 19
SIMULATION_SPEED = 50
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

VERTICE_1 = (-100, -100)
VERTICE_2 = (-100, 100)
VERTICE_3 = (100, -100)
VERTICE_4 = (100, 100)

# Drone Simulation Object
class DroneSimulator:
    def __init__(self, boundry_shape='circle', boundry_params=None):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Drone Simulation")

        self.position = np.array((0, 0), dtype=float)
        self.velocity = np.array([0, 0], dtype=float)
        self.yaw = 0
        self.path = []
        self.photos = []
        self.running = True
        self.start_time = time.time()
        self.flight_time = 0
        self.boundry_shape = boundry_shape
        self.boundry_params = boundry_params if boundry_params else {}

        self.coverage_map = np.empty([WIDTH, HEIGHT])
        self.coverage_map[:] = np.nan

    def adjust_flight_parameters(self, xVelocity, yVelocity, yaw):
        self.velocity = np.array([xVelocity, yVelocity], dtype=float)
        self.yaw += yaw 

    def pause_script_execution(self, duration):
        time.sleep(duration)

    def get_distance_to_origin(self):
        return np.linalg.norm(self.position)

    def get_x_coordinate(self):
        print("x: {}".format(self.position[0]))
        return self.position[0]

    def get_y_coordinate(self):
        print("y: {}".format(self.position[1]))
        return self.position[1]

    def get_compass_heading(self):
        print("compass: {}".format(self.yaw))
        return self.yaw if -180 <= self.yaw <= 180 else 200

    def take_photo(self):
        print(f"Photo taken at ({self.position[0]}, {self.position[1]})")
        self.photos.append([tuple(self.position.copy()), self.yaw])

    def end_flight(self):
        self.velocity = np.array([0, 0])
        self.running = False
        self.flight_time = (time.time() - self.start_time) * SIMULATION_SPEED

    def update(self, delta_time):
        self.position += self.velocity * delta_time
        self.path.append(tuple(self.position.copy()))  # Store position history
        
    def to_screen_coords(self, pos):
        return (int(pos[0] + CENTER_X), int(-pos[1] + CENTER_Y))
    
    def to_world_coords(self, pos):
        return (int(pos[0] + CENTER_X), int(pos[1] + CENTER_Y))

    # currently not in use
    def handle_input(self):
        keys = pygame.key.get_pressed()
        speed = 2

        self.velocity = np.array([0, 0], dtype=float)
        if keys[pygame.K_UP]: self.velocity[1] = speed
        if keys[pygame.K_DOWN]: self.velocity[1] = -speed
        if keys[pygame.K_LEFT]: self.velocity[0] = -speed
        if keys[pygame.K_RIGHT]: self.velocity[0] = speed

    def draw_boundry(self):
        if self.boundry_shape == 'circle':
            circle_center = self.to_screen_coords((self.boundry_params.get('x'), self.boundry_params.get('y')))
            circle_radius= self.boundry_params.get('radius')
            pygame.draw.circle(self.screen, (255, 0, 0), circle_center, circle_radius, 1)
        elif self.boundry_shape == 'rectangle':
            rectangle_vertices = [
                self.boundry_params.get('v1'),
                self.boundry_params.get('v2'),
                self.boundry_params.get('v3'),
                self.boundry_params.get('v4')
            ]
            screen_rect_vertices = [self.to_screen_coords(v) for v in rectangle_vertices]
            min_x = min(v[0] for v in screen_rect_vertices)
            max_y = max(v[1] for v in screen_rect_vertices)
            max_x = max(v[0] for v in screen_rect_vertices)
            min_y = min(v[1] for v in screen_rect_vertices)
            pygame.draw.rect(self.screen, (255, 0, 0), (min_x, min_y, (max_x - min_x), (max_y - min_y)), 1)
            self.add_rectangle_boundry_to_coverage_map(min_x, max_x, min_y, max_y)

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)

        for point in self.path:
            pygame.draw.circle(self.screen, PATH_COLOR, self.to_screen_coords(point), 1)
        for photo in self.photos:
            surf = pygame.Surface((PHOTO_SIZE, PHOTO_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(surf, PHOTO_COLOR, (0, 0, PHOTO_SIZE, PHOTO_SIZE), 0)
            rot_surf = pygame.transform.rotate(surf, photo[1] * -1)
            rot_rect = rot_surf.get_rect(center=self.to_screen_coords(photo[0]))
            self.screen.blit(rot_surf, rot_rect.topleft)

        pygame.draw.circle(self.screen, DRONE_COLOR, self.to_screen_coords(self.position), DRONE_RADIUS)

        self.draw_boundry()
        
        pygame.display.update()

    def wait_for_exit(self):
        print("Simulation complete. Press any key to exit...")

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False

    def print_info(self):
        minutes = int(self.flight_time // 60)
        seconds = int(self.flight_time % 60)
        print(f"Total flight time: {minutes} Minutes, {seconds} Seconds")

    def add_rectangle_boundry_to_coverage_map(self, min_x, max_x, min_y, max_y):

        for x in range(min_x, max_x + 1):
            for y in range( min_y, max_y + 1):
                self.coverage_map[int(x), int(y)] = 0

    def add_circle_boundry_to_coverage_map(self, x, y, radius):
        point = (x, y)
        point = self.to_world_coords(point)
        x, y = point
        
        for i in range(int(x - radius), int(x + radius) + 1):
            for j in range(int(y - radius), int(y + radius) + 1):
                # Check if the point is inside the circle
                if (i - x) ** 2 + (j - y) ** 2 <= radius ** 2:
                    self.coverage_map[int(i), int(j)] = 0

    def add_photos_to_coverage_map(self):
        for photo in self.photos:
            center = photo[0]
            half_size = PHOTO_SIZE // 2
            photo_array = np.empty((PHOTO_SIZE, PHOTO_SIZE), dtype=object)

            # Generate photos coordinate list
            for i in range(PHOTO_SIZE):
                for j in range(PHOTO_SIZE):
                    x = center[0] - half_size + i
                    y = center[1] - half_size + j
                    photo_array[i, j] = (x, y)
            
            # Rotate each coordinate in the photo with given angle
            angle = photo[1]
            rotated_photo = [rotate_point(x, y, center[0], center[1], angle) for x, y in photo_array.flat]

            # Update the coverage map
            for p in rotated_photo:
                p = self.to_world_coords(p)
                x, y = p
                if self.coverage_map[int(x), int(y)] >= 0:
                    self.coverage_map[int(x), int(y)] += 1

    def calculate_coverage(self):
        area = 0
        coverCount = 0

        for (i, j), value in np.ndenumerate(self.coverage_map):
            if value >= 0:
                area += 1
            if value > 0:
                coverCount += 1
        
        coverage = int((coverCount / area) * 100)
        print(f"Coverage: {coverage}%")

    def calculate_overlap(self):
        coveredArea = 0
        overlapCount = 0

        for (i, j), value in np.ndenumerate(self.coverage_map):
            if value == 1:
                coveredArea += 1
            if value > 1:
                overlapCount += 1
                color = value_to_color(value)
                pygame.draw.rect(self.screen, color, (i, j, 1, 1))

        overlap = int((coveredArea / overlapCount) * 100)
        print(f"Overlap: {overlap}%")
        pygame.display.update()

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            delta_time = (clock.tick(FPS) / 1000.0) * SIMULATION_SPEED

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.update(delta_time)
            self.draw()

        self.print_info()
        if self.boundry_shape == 'circle':
            self.add_circle_boundry_to_coverage_map(self.boundry_params.get('x'), self.boundry_params.get('y'), self.boundry_params.get('radius'))
        self.add_photos_to_coverage_map()

        zero_positions = np.argwhere(self.coverage_map > 0)
        for x, y in zero_positions:
            pygame.draw.circle(self.screen, (123, 123, 123), (x, y), 1)
        # pygame.display.update()

        self.calculate_coverage()
        self.calculate_overlap()
        for point in self.path:
            pygame.draw.circle(self.screen, PATH_COLOR, self.to_screen_coords(point), 1)
        pygame.display.update()
        self.wait_for_exit()
        pygame.quit()


# zero_positions = np.argwhere(self.coverage_map == 0)
#         for x, y in zero_positions:
#             pygame.draw.circle(self.screen, (123, 123, 123), (x, y), 1)
#         pygame.display.update()

def rotate_point(x, y, cx, cy, angle):
    theta = np.radians(angle)
    cos_t, sin_t = np.cos(theta), np.sin(theta)

    # Translate point to origin (centerd at cx, cy)
    x_shifted, y_shifted = x - cx, y - cy

    # Apply rotation matrix
    x_rot = cos_t * x_shifted - sin_t * y_shifted + cx
    y_rot = sin_t * x_shifted + cos_t * y_shifted + cy

    return int(round(x_rot)), int(round(y_rot))

def value_to_color(value, vmin=2, vmax=10, cmap_name="plasma", alpha=128):
    """ Maps a value to a color using a colormap (for values > 1) """
    norm = (value - vmin) / (vmax - vmin)  # Normalize between 0 and 1
    norm = np.clip(norm, 0, 1)  # Ensure values stay within 0-1 range
    cmap = plt.get_cmap(cmap_name)  # Get colormap
    r, g, b, _ = cmap(norm)  # Extract RGB (ignore alpha)
    return (int(r * 255), int(g * 255), int(b * 255), alpha)  # Convert to 0-255 RGB