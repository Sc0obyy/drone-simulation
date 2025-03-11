import numpy as np
import time
import settings
from sim.utils import custom_print

class DroneFlight:
    """
    A class to represent a drone flight simulation.
    """

    def __init__(self):
        """
        Initialize the drone flight with default parameters.
        """
        self.position = np.array((0, 0), dtype=float)
        self.velocity = np.array([0, 0], dtype=float)
        self.yaw = 0
        self.path = []
        self.photos = []
        self.running = True
        self.start_time = time.time()
        self.flight_time = 0

    def adjust_flight_parameters(self, xVelocity: float, yVelocity: float, yaw: float) -> None:
        """
        Adjust the flight parameters of the drone.

        Parameters:
        xVelocity (float): The velocity in the x direction.
        yVelocity (float): The velocity in the y direction.
        yaw (float): The yaw angle adjustment.
        """
        self.velocity = np.array([xVelocity, yVelocity], dtype=float)
        self.yaw += yaw
        custom_print(f"Adjusted flight parameters to x_vel: {self.velocity[0]}, y_vel: {self.velocity[1]}, yaw: {self.yaw}")

    def update(self, delta_time: float) -> None:
        """
        Update the drone's position based on the velocity and time elapsed.

        Parameters:
        delta_time (float): The time elapsed since the last update.
        """
        self.position += self.velocity * delta_time
        self.path.append(tuple(self.position.copy()))

    def take_photo(self) -> None:
        """
        Simulate taking a photo at the drone's current position.
        """
        custom_print(f"Photo taken at ({self.position[0]}, {self.position[1]})")
        self.photos.append([tuple(self.position.copy()), self.yaw])

    def end_flight(self) -> None:
        """
        End the drone flight and calculate the total flight time.
        """
        self.velocity = np.array([0, 0])
        self.running = False
        self.flight_time = (time.time() - self.start_time) * settings.SIMULATION_SPEED
        custom_print("Ended flight")

    def get_distance_to_origin(self) -> float:
        """
        Get the distance of the drone from the origin.

        Returns:
        float: The distance to the origin.
        """
        distance = np.linalg.norm(self.position)
        custom_print("Got distance to origin:", distance)
        return distance
    
    def get_x_coordinate(self) -> float:
        """
        Get the x coordinate of the drone's position.

        Returns:
        float: The x coordinate.
        """
        custom_print("Got 'x' coordinate:", self.position[0])
        return self.position[0]

    def get_y_coordinate(self) -> float:
        """
        Get the y coordinate of the drone's position.

        Returns:
        float: The y coordinate.
        """
        custom_print("Got 'y' coordinate:", self.position[1])
        return self.position[1]
    
    def get_compass_heading(self) -> float:
        """
        Get the compass heading (yaw) of the drone.

        Returns:
        float: The compass heading.
        """
        custom_print("compass heading:", self.yaw)
        return self.yaw if -180 <= self.yaw <= 180 else 200
