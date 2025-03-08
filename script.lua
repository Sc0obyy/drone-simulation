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