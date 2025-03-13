# Drone Simulator

This project simulates a drone performing survey missions over designated areas using Lua scripts. The simulator ensures the drone stays within defined boundaries, captures photographs periodically, and adheres to flight constraints.

The aim of this simulator is to enhance the usability of the [DroneGPT](https://github.com/L3S/DroneGPT) application. Without simulating the drone flight paths, it can be tedious to check, if the ChatGPT generated lua script adhers to given requirements.

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

## Dependencies

To run this project, you need to have the following dependencies installed:

- **Python 3.8+**

You can install the required Python packages using `pip`:

```sh
pip install -r requirements.txt
```

## Running the Simulation

To run the simulation, execute the following command:

```sh
python main.py
```

## Generating a Prompt

To generate a prompt based on the settings, use the following command:

```sh
python main.py --prompt
```

You can specify a custom settings file and output file for the prompt:

```sh
python main.py --prompt --settings path/to/custom_settings.py --output path/to/custom_prompt.txt
```

You can improve a pre-generated Lua script for the drone's flight path:

```sh
python main.py --prompt --improve path/to/lua_file.lua
```

Replace `path/to/lua_file.lua` with the actual path to your Lua script file. This will create a prompt with your lua code, demanding it to be improved.

## Example Lua Scripts

The `examples/` directory contains example Lua scripts for different survey missions:

- **offset_circle.lua**: Survey mission within a circular boundary.
- **offset_square.lua**: Survey mission within a square boundary.
- **square.lua**: Survey mission within a rectangular boundary.

## Configuration

The `settings.py` file contains various configuration settings for the simulation, including screen dimensions, simulation speed, drone parameters, and boundary definitions.

The most important settings that might need to be changed for individual needs are:

- `SIMULATION_SPEED`: This variable sets the speed of the simulation. A value of `1` is real time.
- `LUA_SCRIPT_PATH`: This variable lets you set the path for your lua script.
- `PRINT_OUTPUT`: If enabled, all actions made by the drone (and lua script) will be printed.
- `BOUNDARY_SHAPE`: Set the area shape of your targeted flight area. Possible values are: `circle` and `rectangle`
- `BOUNDARY_PARAMS`: Set the variables for your area:
    - If your shape is a circle. The values `x` and `y` are the circle origin coordinates, and `radius` is the circles radius:
        ```
        BOUNDARY_PARAMS = {
            "x": 100,
            "y": 0,
            "radius": 130
        }
        ```
    - If you shape is a rectangle. The values `v1` - `v4` represent the coordinates of your recatangles vertices (corners):
        ```
        BOUNDARY_PARAMS= {
            'v1': (0, 25),
            'v2': (50, 25),
            'v3': (50, -25),
            'v4': (0, -25)
        }
        ```
> [!WARNING] 
> Make sure, that the Boundary values, as well as the prompt settings are identical to the values found for the prompt used to create the lua script. 
> Make sure, that the shapes and parameters are set correctly.

## Usage with DroneGPT

> [!NOTE]
> This Procedure is nowhere near optimal, but it works and might be improved in the future.

### Prerequisites

- A version of DroneGPT installed on the android phone that supports copying the lua code. At the moment only [my forked version](https://github.com/Sc0obyy/DroneGPT) supports this feature, as it is not merged into the original repo.
- The simulator software must be installed on your PC.
- Google drive, or any similar cloud, is installed on the phone and PC.
- The phone and PC have internet connection (to sync the files on the cloud)

### Steps

1. Create an experiment in the DroneGPT app as described in the documentation.
2. Use the app to create a lua script.
3. Press and hold the ChatGPT generated answer and copy the code.
4. Switch into your cloud app, create/open a document and paste the lua code.
5. On the PC, create a lua file and paste the lua code from the cloud into the file.
6. Use this lua file to create a new prompt:\
`python main.py -p -i path/to/lua_file.lua`\
Ensure, that the settings file contains the same values as your experiment from DroneGPT
7. Use the generated prompt to improve the flight path.
8. If you are satisfied with the flight path, copy the lua code into a (new) file in the cloud.
9. Copy the lua code from the cloud app, into DroneGPT with the instruction to use this code instead.
10. Use the optimized code with the normal instructions from DroneGPT.

> [!TIP]
> You can skip steps 1-7 and generate the lua code on you PC, then follow the steps from step 8.

## Bachelor's Thesis

This project was developed as part of my bachelor's thesis. The goal of the program was to create a simulator that can validate the flight paths generated by the DroneGPT application. By simulating the drone's flight, we can ensure that the generated Lua scripts meet the specified requirements and constraints. This simulation was used together with [DroneGPT](https://github.com/L3S/DroneGPT) to create an image dataset of animal photos, captured with a drone. The dataset will be used later on for conducting federated learning experiments.

## License

This project is licensed under the MIT License.
