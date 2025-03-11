-- Lua Script for Drone Survey Mission

-- Constants
local BOUNDARY_CENTER_X = 100
local BOUNDARY_CENTER_Y = 0
local BOUNDARY_RADIUS = 130
local FLIGHT_DURATION = 480 -- 8 minutes in seconds
local PHOTO_INTERVAL = 5 -- Capture a photo every 5 seconds
local DRONE_SPEED = 4 -- Speed in meters per second
local GRID_SPACING = 19 -- Distance between survey lines
local SAFE_MARGIN = 5 -- Buffer to avoid exceeding the boundary

-- Function to check if the drone is within boundaries
local function is_within_boundary(x, y)
    local distance = math.sqrt((x - BOUNDARY_CENTER_X)^2 + (y - BOUNDARY_CENTER_Y)^2)
    return distance <= (BOUNDARY_RADIUS - SAFE_MARGIN)
end

-- Function to get a valid compass heading
local function get_valid_heading()
    local heading = get_compass_heading()
    while heading == 200 do
        pause_script_execution(0.5) -- Retry delay
        heading = get_compass_heading()
    end
    return heading
end

-- Initialize flight parameters
local start_x = get_x_coordinate()
local start_y = get_y_coordinate()

-- Define survey pattern (zigzag pattern with boundary check)
local function perform_survey()
    local x, y = start_x, start_y
    local moving_east = true
    local start_time = os.time()
    
    while os.time() - start_time < FLIGHT_DURATION do
        if not is_within_boundary(x, y) then
            break
        end
        
        -- Move in straight line until near boundary
        local travel_distance = math.min(GRID_SPACING, BOUNDARY_RADIUS - math.abs(x - BOUNDARY_CENTER_X) - SAFE_MARGIN)
        local travel_time = travel_distance / DRONE_SPEED
        
        local x_velocity = moving_east and DRONE_SPEED or -DRONE_SPEED
        adjust_flight_parameters(x_velocity, 0, 0)
        pause_script_execution(travel_time)
        
        -- Capture a photo
        take_photo()
        pause_script_execution(PHOTO_INTERVAL)
        
        -- Update position estimate
        x = x + (moving_east and travel_distance or -travel_distance)
        
        -- Change direction if necessary
        if not is_within_boundary(x + (moving_east and GRID_SPACING or -GRID_SPACING), y) then
            -- Move south to the next survey line if possible
            if is_within_boundary(x, y - GRID_SPACING) then
                adjust_flight_parameters(0, -DRONE_SPEED, 0)
                pause_script_execution(GRID_SPACING / DRONE_SPEED)
                
                -- Capture a photo
                take_photo()
                pause_script_execution(PHOTO_INTERVAL)
                
                -- Update position estimate
                y = y - GRID_SPACING
                
                -- Reverse direction
                moving_east = not moving_east
            else
                break -- Stop if no more space for movement
            end
        end
    end
end

-- Start survey
perform_survey()

-- End flight
end_flight()
