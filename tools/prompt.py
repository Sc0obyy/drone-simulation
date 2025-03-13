from settings import *
import importlib.util

"""
This file is used to make generating a prompt easier by providing global variables that can be changed to change the prompt.
"""

def load_settings(settings_file="settings.py"):
    """
    Load settings from a specified settings file.

    Args:
        settings_file (str): The path to the settings file. Defaults to "settings.py".

    Returns:
        module: The loaded settings module.
    """
    spec = importlib.util.spec_from_file_location("settings", settings_file)
    settings = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(settings)
    return settings

def create_prompt(settings_file=None, output_file="prompt.txt", lua_file=None):
    """
    Create a prompt for generating a Lua script with ChatGPT (DroneGPT) for a drone survey mission.

    Args:
        settings_file (str, optional): The path to the settings file. Defaults to None, which uses "settings.py".
        output_file (str): The path to the output file where the prompt will be saved. Defaults to "prompt.txt".
        lua_file (str, optional): The path to the existing Lua script file to be improved. Defaults to None.

    Returns:
        None
    """

    settings = load_settings(settings_file if settings_file else "settings.py")

    BP = BOUNDARY_PARAMS # Shorten code below
    if BOUNDARY_SHAPE == 'circle':
        areaDescription = f"circle with radius of {BP.get('radius', 0)} meters and center at the following coordinates ({BP.get('x', 0)}, {BP.get('y', 0)})"#.format(BP.get('radius', 0), BP.get('x', 0), BP.get('y', 0))
    elif BOUNDARY_SHAPE == 'rectangle':
        areaDescription = f"rectangle with vertices at the following coordinates {BP.get('v1', (0, 0))}, {BP.get('v2', (0, 0))}, {BP.get('v3', (0, 0))}, and {BP.get('v4', (0, 0))}"
    else:
        print("Wrong boundary shape!")
        quit()

    prompt = f"""
Imagine you are a drone operator and your job is to develop a Lua script to control a drone during a survey mission over a designated area. The script must be complete and ready for immediate execution, with no adjustments needed post-delivery. The mission requires the drone to stay within defined boundaries and take photographs for analysis.

Note: All functions listed below are already implemented. You should call these functions directly in your script.

Coordinate System:
The coordinate system used is a Cartesian plane with the x-axis oriented east (positive) to west (negative) and the y-axis oriented north (positive) to south (negative). The origin of the coordinate system is the drone's starting location. All coordinates are measured in meters.

Flight Objective:
Thoroughly survey the designated area and capture photographs periodically to ensure adequate area coverage without unnecessary overlap.

Drone Flight Constraints:
- The drone must stay within designated boundaries, which for this task is a {areaDescription}
- The total flight duration must not exceed {FLIGHT_DURATION} minutes.
- The drone will maintain a constant height of {FLIGHT_HEIGHT} meters, has a gimbal with a pitch angle of {GIMBAL_ANGLE} degrees and a {CAMERA_FOV} FOV camera, which influence the frequency of photo captures.
Note that the camera FOV of {CAMERA_FOV} refers only to the horizontal FOV. The drone can only capture images in an aspect ratio of 16:9. The resulting photos should be square, thus cropping the edges. The Photo will cover roughly 19x19m of area.

Functions:
- `adjust_flight_parameters(xVelocity, yVelocity, yaw)`: controls the drone's flight direction. `xVelocity` with value range [{MIN_PITCH_ROLL_VALUE}, {MAX_PITCH_ROLL_VALUE}] controls velocity along the x-axis (positive values move the drone east, negative west), and `yVelocity` with value range [{MIN_PITCH_ROLL_VALUE}, {MAX_PITCH_ROLL_VALUE}] controls velocity along the y-axis (positive values move the drone north, negative south). `yaw` with value range [{MIN_YAW_VALUE}, {MAX_YAW_VALUE}] changes the drone's angular velocity (positive values rotate the drone clockwise, negative counterclockwise)
`xVelocity` and `yVelocity` are both in meters/s and yaw is in degrees/s. The drone maintains these flight parameters until they are changed by another call to this function. 
- `pause_script_execution(duration)`: pauses the script execution for a specified duration in seconds. This function is typically used after setting flight parameters to maintain the drone’s current direction and speed for the specified period before the next script command is executed.
- `get_distance_to_origin()`: retrieves the distance in meters from the drone’s current location to the origin of the coordinate system.
- `get_x_coordinate()`, `get_y_coordinate()`: retrieves the x-coordinate and y-coordinate in meters of the drone's current location.
- `get_compass_heading()`: retrieves the compass heading as double. The north is 0 degrees, the east is 90 degrees. The value range is [-180,180]. Returns 200 when compass heading value couldn't be retrieved.
- `take_photo()`: instructs the drone to capture and save a photograph. The script should plan these captures to balance coverage with storage limitations
- `end_flight()`: instructs the drone to return to its starting point and terminate the flight.

Instructions:
Develop the Lua script to ensure the drone remains within the boundary throughout the flight. Select an efficient and effective pattern for surveying the designated area. Implement error handling for failed compass heading retrievals by attempting a retry before any critical operations. The script should respect the {FLIGHT_DURATION} minute flight duration limit, utilizing the pause_script_execution function to control the timing of flight adjustments.
"""
    
    if lua_file:
        with open(lua_file, "r") as file:
            lua_code = file.read()
        prompt +="""
Your task is to improve the existing Lua script by optimizing the flight path to ensure complete coverage of the designated area while minimizing unnecessary overlap in the captured photographs. You should also enhance the script to handle any potential errors that may arise during execution, such as failed compass heading retrievals. The script should be efficient, reliable, and capable of completing the survey mission within the specified time frame."""
        prompt += lua_code

    with open(output_file, "w") as file:
        file.write(prompt)

    print(f"Created '{output_file}'")
