import numpy as np
import time
import settings

class DroneFlight:
    def __init__(self):
        self.position = np.array((0, 0), dtype=float)
        self.velocity = np.array([0, 0], dtype=float)
        self.yaw = 0
        self.path = []
        self.photos = []
        self.running = True
        self.start_time = time.time()
        self.flight_time = 0

    def adjust_flight_parameters(self, xVelocity: float, yVelocity: float, yaw: float) -> None:
        self.velocity = np.array([xVelocity, yVelocity], dtype=float)
        self.yaw += yaw

    def update(self, delta_time: float) -> None:
        self.position += self.velocity * delta_time
        self.path.append(tuple(self.position.copy()))

    def take_photo(self) -> None:
        print(f"Photo taken at ({self.position[0]}, {self.position[1]})")
        self.photos.append([tuple(self.position.copy()), self.yaw])

    def end_flight(self) -> None:
        self.velocity = np.array([0, 0])
        self.running = False
        self.flight_time = (time.time() - self.start_time) * settings.SIMULATION_SPEED

    def get_distance_to_origin(self) -> float:
        return np.linalg.norm(self.position)
    
    def get_x_coordinate(self) -> float:
        print("x:", self.position[0])
        return self.position[0]

    def get_y_coordinate(self) -> float:
        print("y:", self.position[1])
        return self.position[1]
    
    def get_compass_heading(self) -> float:
        print("compass:", self.yaw)
        return self.yaw if -180 <= self.yaw <= 180 else 200