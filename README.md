# Traffic Light Control Simulation

This project simulates a city with traffic lights and uses reinforcement learning (Q-learning) to optimize traffic flow. The simulation includes three modes: Fixed Time, SCOOT, and AI Control.

## Project Structure

- `main.py`: The main script that runs the simulation.
- `qlearningagent.py`: Contains the QLearningAgent class used for reinforcement learning.
- `scoot.py`: Contains functions for the SCOOT traffic light control algorithm.
- `utils.py`: Utility functions for displaying simulation statistics and modes.
- `definitions.py`: Contains constants and definitions used throughout the project.
- `traffic_light.py`: Contains the TrafficLight class.
- `car.py`: Contains the Car class.
- `circular_array.py`: Contains the CircularArray class used for storing stopped car percentages.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/traffic-light-control.git
    cd traffic-light-control
    ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv myenv
    source myenv/bin/activate
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the simulation:
```bash
python main.py
