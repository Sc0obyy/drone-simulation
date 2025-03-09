import pygame
import argparse
import settings
from sim.flight import DroneFlight
from sim.renderer import DroneRenderer
from tools.lua_runner import LuaRunner
from sim.utils import to_screen_coords

def main_simulation():
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

def run_prompt(settings_file=None, output_file="prompt.txt"):
    from tools.prompt import create_prompt
    create_prompt(settings_file, output_file)

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Drone Simulator Application\n\n"
                    "By default (no arguments), the simualtion will run with settings from settings.py",
        epilog="Example usage:\n"
                " python main.py           # Runs the simulation\n"
                " python main.py --prompt  # Creates a prompt with setting from settings.py\n"
                " python main.py --prompt -s custom_settings.py # Creates a prompt with custom settings\n"
                " python main.py --prompt --output custom_prompt.txt  # Saves the prompt to a different file",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-p", "--prompt", action="store_true", help="Create the required Prompt (doesn't run simulation)")
    parser.add_argument("-s", "--settings", type=str, help="Specify a custom settings file (default: settings.py)")
    parser.add_argument("-o", "--output", type=str, default="prompt.txt", help="Specify output filename (default: prompt.txt)")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    if args.prompt:
        run_prompt(args.settings, args.output)
    else:
        main_simulation()
