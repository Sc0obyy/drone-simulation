import pygame
import numpy as np
import time
import math

# Constants
WIDTH, HEIGHT = 1600, 600
BACKGROUND_COLOR = (220, 220, 220)
DRONE_RADIUS = 1
DRONE_COLOR = (0, 0, 0)
PATH_COLOR = (255, 255, 0)
FPS = 30
PHOTO_COLOR = (255, 0, 0)
PHOTO_SIZE = 19
SIMULATION_SPEED = 5
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

VERTICE_1 = (-100, -10)
VERTICE_2 = (-10, -10)
VERTICE_3 = (-100, -80)
VERTICE_4 = (-10, -80)

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
        
    def to_screen_coords(sef, pos):
        return (int(pos[0] + CENTER_X), int(-pos[1] + CENTER_Y))

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

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)

        for point in self.path:
            pygame.draw.circle(self.screen, PATH_COLOR, self.to_screen_coords(point), 2)
        for photo in self.photos:
            surf = pygame.Surface((PHOTO_SIZE, PHOTO_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(surf, PHOTO_COLOR, (0, 0, PHOTO_SIZE, PHOTO_SIZE), 2)
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
        self.wait_for_exit()
        pygame.quit()
