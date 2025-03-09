-- Define survey parameters
local velocity = 6       -- Increased speed to reduce flight time
local flight_time = 8 * 60  -- Total flight time in seconds
local max_x, min_x = 85, -85  -- Reduced boundaries to ensure staying inside
local max_y, min_y = 85, -85

-- Function to get valid compass heading
function get_valid_heading()
    local heading = get_compass_heading()
    local retries = 3
    while heading == 200 and retries > 0 do
        pause_script_execution(0.5)
        heading = get_compass_heading()
        retries = retries - 1
    end
    return heading
end

-- Move to the starting corner (bottom-left) precisely
adjust_flight_parameters(-velocity, -velocity, 0)
while get_x_coordinate() > min_x + 5 or get_y_coordinate() > min_y + 5 do
    pause_script_execution(1)
end
adjust_flight_parameters(0, 0, 0)
pause_script_execution(1)

-- Start surveying in a structured pattern
local x, y = min_x, min_y
local y_direction = 1  -- 1 for north, -1 for south

local start_time = os.time()
while os.time() - start_time < flight_time and x <= max_x do
    if y_direction == 1 then y = max_y - 5 else y = min_y + 5 end  -- Added buffer to stay inside
    adjust_flight_parameters(0, velocity * y_direction, 0)
    while (y_direction == 1 and get_y_coordinate() < max_y - 10) or (y_direction == -1 and get_y_coordinate() > min_y + 10) do
        take_photo()
        pause_script_execution(3.0)  -- Adjusted for smoother transitions
    end
    adjust_flight_parameters(0, 0, 0)
    pause_script_execution(1)
    
    x = x + 16  -- Adjusted spacing to cover the rightmost area effectively
    if x > max_x then break end  -- Prevent extra passes
    
    adjust_flight_parameters(velocity, 0, 0)
    while get_x_coordinate() < x - 5 do
        pause_script_execution(1)
    end
    adjust_flight_parameters(0, 0, 0)
    pause_script_execution(1)
    
    y_direction = -y_direction  -- Switch direction
end

-- Ensure return flight remains inside boundaries
adjust_flight_parameters(0, 0, 0)
pause_script_execution(1)
local return_x = -get_x_coordinate()
local return_y = -get_y_coordinate()
local return_distance = get_distance_to_origin()
if return_distance > 0 then
    local norm_x = return_x / return_distance * velocity
    local norm_y = return_y / return_distance * velocity
    if get_x_coordinate() < min_x then norm_x = math.abs(norm_x) end
    if get_x_coordinate() > max_x then norm_x = -math.abs(norm_x) end
    if get_y_coordinate() < min_y then norm_y = math.abs(norm_y) end
    if get_y_coordinate() > max_y then norm_y = -math.abs(norm_y) end
    adjust_flight_parameters(norm_x, norm_y, 0)
    pause_script_execution(return_distance / velocity)
end
adjust_flight_parameters(0, 0, 0)
end_flight()