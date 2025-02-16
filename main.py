import pygame
import random
import networkx as nx
import numpy as np
from definitions import *
from traffic_light import *
from car import Car
from utils import *
from scoot import *
from fixed_times import *
from qlearningagent import QLearningAgent
from ai_scoot import *

# Variables
SIM_MODE = 1  # 1: Fixed Time, 2: SCOOT

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("City with Traffic Lights Simulation")
clock = pygame.time.Clock()

# Define road network using a graph
city_graph = nx.Graph()

stopped_buffer = CircularArray(FPS*180) # 3 minutes

# Generate node positions based on ROWS and COLS
nodes = {}
for r in range(ROWS):
    for c in range(COLS):
        node_name = f"{chr(65 + c)}{r+1}"  # Create node names like A1, B1, C1...
        node_pos = (node_spacing_x * (c + 1), node_spacing_y * (r + 1))
        nodes[node_name] = node_pos

# Define the road network
city_graph = nx.Graph()

# Add road nodes (intersections)
for node_name, pos in nodes.items():
    city_graph.add_node(node_name, pos=pos)

# Add roads (edges between nodes)
edges = []
for r in range(ROWS):
    for c in range(COLS):
        node_name = f"{chr(65 + c)}{r+1}"
        if c < COLS - 1:  # Horizontal roads
            edges.append((node_name, f"{chr(65 + c + 1)}{r+1}"))
        if r < ROWS - 1:  # Vertical roads
            edges.append((node_name, f"{chr(65 + c)}{r+2}"))
city_graph.add_edges_from(edges)

# Traffic lights (simplified for each node)
traffic_lights = {
    node: {
        "N": {"green": CYCLE_BASE, "red": CYCLE_BASE, "yellow": YELLOW_TIME, "timer": 0, "state": "green", "queue": []},
        "S": {"green": CYCLE_BASE, "red": CYCLE_BASE, "yellow": YELLOW_TIME, "timer": 0, "state": "red", "queue": []},
        "E": {"green": CYCLE_BASE, "red": CYCLE_BASE, "yellow": YELLOW_TIME, "timer": 0, "state": "red", "queue": []},
        "W": {"green": CYCLE_BASE, "red": CYCLE_BASE, "yellow": YELLOW_TIME, "timer": 0, "state": "green", "queue": []}
    }
    for node in nodes
}

# Synchronize N/S and E/W timers
for node in nodes:
    traffic_lights[node]["S"]["green"] = traffic_lights[node]["N"]["green"]
    traffic_lights[node]["S"]["red"] = traffic_lights[node]["N"]["red"]
    traffic_lights[node]["W"]["green"] = traffic_lights[node]["E"]["green"]
    traffic_lights[node]["W"]["red"] = traffic_lights[node]["E"]["red"]

# Initialize cars with random start and target nodes
cars = [Car(random.choice(list(nodes.keys())), random.choice(list(nodes.keys())), nodes, city_graph) for _ in range(NUM_CARS)]

# Add the display_sim_mode function
def display_sim_mode(screen):
    """Display the current simulation mode on the screen."""
    font = pygame.font.Font(None, 36)
    if SIM_MODE == 1:
        mode_text = "Mode: Fixed Time"
    elif SIM_MODE == 2:
        mode_text = "Mode: SCOOT training AI"
    elif SIM_MODE == 3:
        mode_text = "Mode: AI Control"
    else:
        mode_text = "Mode: Unknown"

    # Render the text
    text_surface = font.render(mode_text, True, BLACK)
    screen.blit(text_surface, (10, 10))  # Display at the top-left corner

# Initialize Q-learning agent
state_size = len(nodes) * 4  # Number of nodes * 4 directions
action_size = 2  # Two actions: increase or decrease green time
agent = QLearningAgent(state_size, action_size)

# Main loop
running = True
frame_count = 0
previous_avg_stopped = 0

while running:
    screen.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                SIM_MODE = 1  # Fixed time mode
            elif event.key == pygame.K_2:
                SIM_MODE = 2  # SCOOT 
            elif event.key == pygame.K_3:
                SIM_MODE = 3  # AI Control

    # Draw roads
    for edge in edges:
        pygame.draw.line(screen, BLACK, nodes[edge[0]], nodes[edge[1]], 5)

    # Move and draw cars
    stopped_cars = 0
    for car in cars:
        car.move(cars, nodes, traffic_lights, city_graph)
        car.draw(screen)
        if car.stopped:
            stopped_cars += 1
    
    percentage_of_stopped = 100 * stopped_cars / NUM_CARS
    stopped_buffer.add(percentage_of_stopped)

    draw_traffic_lights(nodes, city_graph, traffic_lights, screen)

    cycle = CYCLE_BASE
    # Update traffic lights (Fixed Time, SCOOT, or AI Control)
    if SIM_MODE == 1:
        update_traffic_lights(traffic_lights, nodes)
    elif SIM_MODE == 2:
        cycle = scoot_update_traffic_lights(frame_count, traffic_lights, nodes)
    elif SIM_MODE == 3:
        cycle = ai_update_traffic_lights(frame_count, traffic_lights, nodes, agent)

    # Display queue lengths and metrics
    display_statistics(screen, nodes, traffic_lights, stopped_buffer, cycle)

    # Display the current simulation mode
    display_sim_mode(screen)

    # Increment frame count
    frame_count += 1

    # Train the agent if in SCOOT mode
    if SIM_MODE == 2:
        current_avg_stopped = stopped_buffer.average()
        reward = 1 if current_avg_stopped < previous_avg_stopped else -1
        previous_avg_stopped = current_avg_stopped

        state = np.array([len(traffic_lights[node][direction]["queue"]) for node in nodes for direction in ["N", "S", "E", "W"]])
        action = agent.choose_action(state)
        next_state = state  # In this simplified example, we assume the state doesn't change
        agent.learn(state, action, reward, next_state)

    pygame.display.flip()
    clock.tick(FPS)
    
pygame.quit()