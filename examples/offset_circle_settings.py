# Screen and simulation settings
WIDTH = 1600
HEIGHT = 600
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2
BACKGROUND_COLOR = (220, 220, 220)
FPS = 60
SIMULATION_SPEED = 50
LUA_SCRIPT_PATH = "examples/offset_square.lua"

# Drone photo and path settings
PHOTO_COLOR = (200, 200, 200)
PHOTO_SIZE = 19
PATH_COLOR = (255, 255, 0, 0.1)

# Shape and size of area
BOUNDARY_SHAPE = 'circle'
BOUNDARY_PARAMS = {
    "x": 100,
    "y": 0,
    "radius": 130
}

# Prompt settings
FLIGHT_DURATION = 8
FLIGHT_HEIGHT = 20
GIMBAL_ANGLE = -90
CAMERA_FOV = 82.1
MIN_PITCH_ROLL_VALUE = -6
MAX_PITCH_ROLL_VALUE = 6
MIN_YAW_VALUE = -100
MAX_YAW_VALUE = 100

# Debug settings
PRINT_OUTPUT = True
