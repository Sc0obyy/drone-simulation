from lupa import LuaRuntime
import time
from old.simulation import DroneSimulator, SIMULATION_SPEED, VERTICE_1, VERTICE_2, VERTICE_3, VERTICE_4


# Initialize Lua runtime
lua = LuaRuntime(unpack_returned_tuples=True)

# Initialize Drone simulation instance
# sim = DroneSimulator('rectangle', {'v1': VERTICE_1, 'v2': VERTICE_2, 'v3': VERTICE_3, 'v4': VERTICE_4})
sim = DroneSimulator('circle', {'radius': 130, 'x': 100, 'y': 0})

# API functions called by Lua script
def adjust_flight_parameters(xVelocity, yVelocity, yaw):
    sim.adjust_flight_parameters(xVelocity, yVelocity, yaw)
    print("xVelocity: {}, yVelocity: {}, yaw:{}".format(xVelocity, yVelocity, yaw))
  
def pause_script_execution(duration):
    start_time = time.time()
    last_time = start_time
    
    while time.time() - start_time < duration / SIMULATION_SPEED:
        delta_time = (time.time() - last_time) * SIMULATION_SPEED
        last_time = time.time()

        sim.update(delta_time)
        sim.draw()

    print("Paused for {} seconds".format(duration))

def get_distance_to_origin():
    return sim.get_distance_to_origin()

def get_x_coordinate():
    return sim.get_x_coordinate()

def get_y_coordinate():
    return sim.get_y_coordinate()

def get_compass_heading():
    return sim.get_compass_heading()

def take_photo():
    return sim.take_photo()

def end_flight():
    return sim.end_flight()

# Make python functions available to lua
lua.globals().adjust_flight_parameters = adjust_flight_parameters
lua.globals().pause_script_execution = pause_script_execution
lua.globals().get_distance_to_origin = get_distance_to_origin
lua.globals().get_x_coordinate = get_x_coordinate
lua.globals().get_y_coordinate = get_y_coordinate
lua.globals().get_compass_heading = get_compass_heading
lua.globals().take_photo = take_photo
lua.globals().end_flight = end_flight

# Lua scripts
lua_code = """
-- Drone Survey Mission Lua Script

-- Constants
local MAX_RADIUS = 100  -- Maximum flight boundary
local FLIGHT_DURATION = 600  -- 10 minutes in seconds
local DRONE_SPEED = 5  -- meters per second
local PHOTO_INTERVAL = 10  -- seconds between each photo
local GRID_SPACING = 20  -- Distance between survey lines
local ALTITUDE = 20  -- Fixed flight altitude

-- Utility Functions
local function get_valid_compass_heading()
    local heading = get_compass_heading()
    if heading == 200 then  -- Error retrieving heading
        pause_script_execution(1)  -- Wait and retry
        heading = get_compass_heading()
    end
    return heading
end

local function within_boundary(x, y)
    return math.sqrt(x^2 + y^2) <= MAX_RADIUS
end

-- Survey Flight Pattern (Grid-based approach)
local function survey_area()
    local start_x, start_y = get_x_coordinate(), get_y_coordinate()
    local x, y = -MAX_RADIUS + GRID_SPACING / 2, -MAX_RADIUS + GRID_SPACING / 2
    local direction = 1  -- 1 for right, -1 for left
    local start_time = os.time()
    
    while os.time() - start_time < FLIGHT_DURATION do
        if within_boundary(x, y) then
            adjust_flight_parameters(DRONE_SPEED * direction, 0, 0)
            pause_script_execution(GRID_SPACING / DRONE_SPEED)
            take_photo()
        end
        
        x = x + (GRID_SPACING * direction)
        if math.abs(x) >= MAX_RADIUS then  -- Reached boundary, move up
            direction = -direction
            adjust_flight_parameters(0, DRONE_SPEED, 0)
            pause_script_execution(GRID_SPACING / DRONE_SPEED)
            take_photo()
            y = y + GRID_SPACING
            if y >= MAX_RADIUS then  -- Reached top boundary
                break
            end
        end
    end
end

-- Start Survey
survey_area()

-- End Flight
end_flight()

"""

lua_code_offset_circle = """
-- Drone Survey Mission Lua Script

-- Constants
local MAX_RADIUS = 130  -- Maximum allowed radius from (100,0)
local MAX_FLIGHT_TIME = 480  -- Maximum flight time in seconds (8 minutes)
local VELOCITY = 3  -- Speed of the drone in m/s
local PHOTO_INTERVAL = 10  -- Time interval between photos in seconds
local GRID_SPACING = 20  -- Distance between survey lines
local CENTER_X, CENTER_Y = 100, 0  -- Center of the circular boundary
local COMPASS_RETRY_LIMIT = 3  -- Max retries for compass heading retrieval

-- Function to check if the drone is within the boundary
local function is_within_boundary()
    local x, y = get_x_coordinate(), get_y_coordinate()
    local distance = math.sqrt((x - CENTER_X)^2 + (y - CENTER_Y)^2)
    return distance <= MAX_RADIUS
end

-- Function to retrieve a valid compass heading
local function get_valid_compass_heading()
    for i = 1, COMPASS_RETRY_LIMIT do
        local heading = get_compass_heading()
        if heading ~= 200 then
            return heading
        end
        pause_script_execution(0.5)  -- Brief pause before retrying
    end
    return nil  -- Indicate failure after retries
end

-- Function to execute a grid-based survey pattern
local function execute_survey()
    local flight_time = 0
    local x_direction = 1  -- 1 for east, -1 for west
    local y_position = -MAX_RADIUS
    
    while flight_time < MAX_FLIGHT_TIME do
        -- Move horizontally
        adjust_flight_parameters(VELOCITY * x_direction, 0, 0)
        local move_duration = (2 * MAX_RADIUS) / VELOCITY
        pause_script_execution(move_duration)
        flight_time = flight_time + move_duration
        take_photo()
        
        if flight_time >= MAX_FLIGHT_TIME then break end
        
        -- Move forward in the grid pattern
        adjust_flight_parameters(0, VELOCITY, 0)
        pause_script_execution(GRID_SPACING / VELOCITY)
        flight_time = flight_time + (GRID_SPACING / VELOCITY)
        take_photo()
        
        -- Reverse horizontal movement direction
        x_direction = -x_direction
    end
    print(flight_time)
end

-- Main Script Execution
if not is_within_boundary() then
    end_flight()
    return
end

execute_survey()
end_flight()
"""

lua_code_offset_circle_new = """
-- Drone Survey Mission Lua Script

-- Constants
local MAX_RADIUS = 130  -- Maximum allowed radius from (100,0)
local MAX_FLIGHT_TIME = 480  -- Maximum flight time in seconds (8 minutes)
local VELOCITY = 5  -- Increased speed of the drone in m/s
local PHOTO_INTERVAL_DISTANCE = 15  -- Take a photo every 15 meters
local CENTER_X, CENTER_Y = 100, 0  -- Center of the circular boundary
local COMPASS_RETRY_LIMIT = 3  -- Max retries for compass heading retrieval
local CIRCLE_POINTS = 16  -- Increased number of points per circular layer for better coverage
local LAYERS = 4  -- Increased number of concentric survey circles

-- Function to check if the drone is within the boundary
local function is_within_boundary()
    local x, y = get_x_coordinate(), get_y_coordinate()
    local distance = math.sqrt((x - CENTER_X)^2 + (y - CENTER_Y)^2)
    return distance <= MAX_RADIUS
end

-- Function to retrieve a valid compass heading
local function get_valid_compass_heading()
    for i = 1, COMPASS_RETRY_LIMIT do
        local heading = get_compass_heading()
        if heading ~= 200 then
            return heading
        end
        pause_script_execution(0.5)  -- Brief pause before retrying
    end
    return nil  -- Indicate failure after retries
end

-- Function to execute a multi-layer circular survey pattern
local function execute_survey()
    local flight_time = 0
    local layer_step = MAX_RADIUS / LAYERS
    
    for layer = 1, LAYERS do
        local radius = layer * layer_step
        local angle_step = 360 / CIRCLE_POINTS
        
        for i = 0, CIRCLE_POINTS - 1 do
            if flight_time >= MAX_FLIGHT_TIME then break end
            
            local angle_rad = math.rad(i * angle_step)
            local target_x = CENTER_X + radius * math.cos(angle_rad)
            local target_y = CENTER_Y + radius * math.sin(angle_rad)
            
            local move_x = target_x - get_x_coordinate()
            local move_y = target_y - get_y_coordinate()
            
            local distance = math.sqrt(move_x^2 + move_y^2)
            local move_duration = distance / VELOCITY
            adjust_flight_parameters(move_x / move_duration, move_y / move_duration, 0)
            pause_script_execution(move_duration)
            flight_time = flight_time + move_duration
            
            -- Ensure more frequent photo captures based on distance traveled
            local num_photos = math.max(1, math.floor(distance / PHOTO_INTERVAL_DISTANCE))
            for _ = 1, num_photos do
                take_photo()
            end
        end
    end
    print(flight_time)
end

-- Main Script Execution
if not is_within_boundary() then
    end_flight()
    return
end

execute_survey()
end_flight()


"""

lua_code_test = """
-- Constants
local MAX_VELOCITY = 6  -- meters per second
local FLIGHT_RADIUS = 130  -- meters
local CENTER_X, CENTER_Y = 100, 0
local ALTITUDE = 20  -- meters
local MAX_FLIGHT_TIME = 480  -- seconds (8 minutes)
local PHOTO_INTERVAL = 5  -- seconds between photos

-- Functions
local function within_boundaries(x, y)
    local distance = math.sqrt((x - CENTER_X)^2 + (y - CENTER_Y)^2)
    return distance <= FLIGHT_RADIUS
end

local function valid_compass_heading()
    local heading = get_compass_heading()
    while heading == 200 do  -- Retry if the value is invalid
        pause_script_execution(1)
        heading = get_compass_heading()
    end
    return heading
end

-- Flight Pattern
local function survey_area()
    local start_time = os.time()
    local direction = 1  -- 1 for east, -1 for west
    local step_size = 20  -- Distance per survey line
    local x, y = get_x_coordinate(), get_y_coordinate()
    local y_step = 0

    while os.time() - start_time < MAX_FLIGHT_TIME do
        if not within_boundaries(x, y) then
            break  -- End if out of bounds
        end
        
        -- Move in x direction
        adjust_flight_parameters(direction * MAX_VELOCITY, 0, 0)
        local move_time = step_size / MAX_VELOCITY
        pause_script_execution(move_time)
        take_photo()

        -- Update position
        x = get_x_coordinate()
        y = get_y_coordinate()
        
        -- Check if still within boundaries
        if not within_boundaries(x, y) then
            break
        end
        
        -- Move in y direction (north or south)
        y_step = y_step + step_size
        if y_step > FLIGHT_RADIUS then
            break  -- Stop if max range is reached
        end

        adjust_flight_parameters(0, MAX_VELOCITY, 0)
        pause_script_execution(move_time)
        take_photo()

        -- Update position
        x = get_x_coordinate()
        y = get_y_coordinate()

        -- Reverse direction for next row
        direction = -direction
    end
end

-- Start mission
survey_area()
end_flight()

"""

# Execute Lua script and run Simulation
lua.execute(lua_code_offset_circle_new)
sim.run()