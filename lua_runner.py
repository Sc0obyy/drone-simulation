from lupa import LuaRuntime
import time
import settings

class LuaRunner:
    def __init__(self, flight, renderer):
        self.flight = flight
        self.renderer = renderer
        self.lua = LuaRuntime(unpack_returned_tuples=True)
        self.register_api_functions()
        self.load_lua_script()

    def register_api_functions(self) -> None:
        self.lua.globals().adjust_flight_parameters = self.flight.adjust_flight_parameters
        self.lua.globals().pause_script_execution = self.pause_script_execution
        self.lua.globals().get_distance_to_origin = self.flight.get_distance_to_origin
        self.lua.globals().get_x_coordinate = self.flight.get_x_coordinate
        self.lua.globals().get_y_coordinate = self.flight.get_y_coordinate
        self.lua.globals().get_compass_heading = self.flight.get_compass_heading
        self.lua.globals().take_photo = self.flight.take_photo
        self.lua.globals().end_flight = self.flight.end_flight

    def pause_script_execution(self, duration: float) -> None:
        start_time = time.time()
        last_time = start_time
        while time.time() - start_time < duration / settings.SIMULATION_SPEED:
            delta_time = (time.time() - last_time) * settings.SIMULATION_SPEED
            last_time = time.time()
            self.flight.update(delta_time)
            self.renderer.draw()
        print(f"Paused for {duration} seconds")

    def load_lua_script(self) -> None:
        with open(settings.LUA_SCRIPT_PATH, 'r') as f:
            self.lua_script = f.read()

    def execute(self) -> None:
        self.lua.execute(self.lua_script)