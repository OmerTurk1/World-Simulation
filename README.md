# WorldSim

## About
WorldSim is a simple world map and population simulation project built with Python. The project simulates agents that walk, eat, and reproduce on a randomly generated terrain map. When the simulation ends, daily population data is stored in `data/population_data.csv`.

## Key Features
- World map generation using fractal noise (`generate_world.py`)
- Walkable surface and food source detection on the map (`map_manager.py`)
- Agent-based simulation with energy, aging, and reproduction logic (`agent.py`)
- Real-time visualization using Pygame (`main.py`)
- Daily population statistics saved as CSV

## Project Structure
- `main.py`: Starts the simulation loop, creates agents, renders the simulation with Pygame, and saves results to CSV.
- `generate_world.py`: Generates a world map based on input parameters and saves a PNG file to the `worlds/` folder.
- `map_manager.py`: Manages map loading, walkability checks, food state, and random position selection.
- `agent.py`: Defines agent behavior including position, energy, age, movement, and reproduction.
- `data/`: Contains simulation output files.
- `worlds/`: Contains generated map images.

## Requirements
- Python 3.9 or later
- Pygame
- NumPy
- Matplotlib
- SciPy

## Installation
1. Open the project folder.


2. Install the required packages:

```bash
pip install -r requirements.txt
```

## How to Run
1. First generate a world map(There is already some samples, just run this script if you want your own world):

```bash
python generate_world.py
```

2. Then run the simulation:

```bash
python main.py
```

3. When you close the simulation window, the file `data/population_data.csv` will be created or updated.

## Notes
- `main.py` uses `worlds/world_map_s=1000_r=6_o=10.png` by default. To use a different map, update the `map_path` variable in `main.py`.
- Agents cannot move over water or mountain-like areas; they only travel on walkable terrain.

## Development Ideas
- Add different agent types and behavior models
- Add combat or competition mechanics between agents
- Make food distribution more dynamic
- Allow map generation parameters to be controlled with user input
