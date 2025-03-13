import pygame
import argparse
import settings
from sim.flight import DroneFlight
from sim.renderer import DroneRenderer
from tools.lua_runner import LuaRunner
from sim.utils import to_screen_coords

def main_simulation():
    """
    Main function to run the drone simulation.
    Initializes the flight and renderer objects, executes the Lua script,
    and runs the main simulation loop until the flight ends.
    """
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

def run_prompt(settings_file=None, output_file="prompt.txt", lua_file=None):
    """
    Function to create a prompt based on the settings file.
    
    Args:
        settings_file (str): Path to the custom settings file. Defaults to None.
        output_file (str): Path to the output file where the prompt will be saved. Defaults to "prompt.txt".
        lua_file (str, optional): Path to the existing Lua script file to be improved. Defaults to None.
    """
    from tools.prompt import create_prompt
    create_prompt(settings_file, output_file, lua_file)

def parse_arguments():
    """
    Function to parse command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Drone Simulator Application\n\n"
                    "By default (no arguments), the simulation will run with settings from settings.py",
        epilog="Example usage:\n"
                " python main.py           # Runs the simulation\n"
                " python main.py --prompt  # Creates a prompt with setting from settings.py\n"
                " python main.py --prompt -s custom_settings.py # Creates a prompt with custom settings\n"
                " python main.py --prompt --output custom_prompt.txt  # Saves the prompt to a different file\n"
                " python main.py --prompt --improve existing_script.lua  # Improves an existing Lua script with given file",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-p", "--prompt", action="store_true", help="Create the required Prompt (doesn't run simulation)")
    parser.add_argument("-s", "--settings", type=str, help="Specify a custom settings file (default: settings.py)")
    parser.add_argument("-o", "--output", type=str, default="prompt.txt", help="Specify output filename (default: prompt.txt)")
    parser.add_argument("-i", "--improve", type=str, help="Improve the existing Lua script with given file")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    if args.prompt:
        run_prompt(args.settings, args.output, args.improve)
    else:
        main_simulation()
