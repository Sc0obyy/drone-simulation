import pygame
import settings
from sim.flight import DroneFlight
from sim.renderer import DroneRenderer
from lua_runner import LuaRunner
from sim.utils import to_screen_coords

def main():
    # Initialize flight and renderer objects
    flight = DroneFlight()
    renderer = DroneRenderer(flight)

    # Optionally execute the Lua script (which will use the flight API)
    lua_runner = LuaRunner(flight, renderer)
    lua_runner.execute()

    # Main simulation loop
    clock = pygame.time.Clock()
    while flight.running:
        delta_time = (clock.tick(settings.FPS) / 1000.0) * settings.SIMULATION_SPEED
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flight.running = False

        flight.update(delta_time)
        renderer.draw()

    # After simulation ends, draw final info
    renderer.draw_colorbar(50, int(settings.HEIGHT / 4), 50, int(settings.HEIGHT / 2))
    flight.end_flight()  # Record flight time
    renderer.print_info()

    # Draw final flight path
    for point in flight.path:
        pygame.draw.circle(renderer.screen, settings.PATH_COLOR, to_screen_coords(point), 1)

    pygame.display.update()
    renderer.wait_for_exit()
    pygame.quit()

if __name__ == '__main__':
    main()
