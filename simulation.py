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
PHOTO_SIZE = 35
SIMULATION_SPEED = 20
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

# Drone Simulation Object
class DroneSimulator:
    def __init__(self, starting_pos=(0, 0)):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Drone Simulation")

        self.position = np.array(starting_pos, dtype=float)
        self.velocity = np.array([0, 0], dtype=float)
        self.yaw = 0
        self.path = []
        self.photos = []
        self.running = True

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
        self.photos.append(tuple(self.position.copy()))

    def end_flight(self):
        self.velocity = np.array([0, 0])
        self.running = False

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

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)

        for point in self.path:
            pygame.draw.circle(self.screen, PATH_COLOR, self.to_screen_coords(point), 2)
        for photo in self.photos:
            pygame.draw.rect(self.screen, PHOTO_COLOR, ((self.to_screen_coords(photo)[0] - PHOTO_SIZE // 2), (self.to_screen_coords(photo)[1] - PHOTO_SIZE // 2), PHOTO_SIZE, PHOTO_SIZE), 2)

        pygame.draw.circle(self.screen, DRONE_COLOR, self.to_screen_coords(self.position), DRONE_RADIUS)

        pygame.draw.circle(self.screen, (255, 0, 0), self.to_screen_coords((100, 0)), 130, 1)
        
        pygame.display.update()

    def wait_for_exit(self):
        print("Simulation complete. Press any key to exit...")

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            delta_time = (clock.tick(FPS) / 1000.0) * SIMULATION_SPEED

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.update(delta_time)
            self.draw()

        self.wait_for_exit()
        pygame.quit()
