import pygame
from definitions import *

# Draw intersections and traffic lights
def draw_traffic_lights(nodes, city_graph, traffic_lights, screen):
    for node, pos in nodes.items():
        neighbors = list(city_graph.neighbors(node))
        light_positions = []

        # Determine traffic light positions based on road directions
        for neighbor in neighbors:
            dx = nodes[neighbor][0] - pos[0]
            dy = nodes[neighbor][1] - pos[1]

            # Place traffic lights 30 pixels away from the intersection in the direction of the road
            if dx > 0:  # Road to the right (East)
                light_positions.append((pos[0] + 30, pos[1], "E"))
            elif dx < 0:  # Road to the left (West)
                light_positions.append((pos[0] - 30, pos[1], "W"))
            elif dy > 0:  # Road downward (South)
                light_positions.append((pos[0], pos[1] + 30, "S"))
            elif dy < 0:  # Road upward (North)
                light_positions.append((pos[0], pos[1] - 30, "N"))

        # Draw traffic lights and arrows
        for light_pos in light_positions:
            x, y, direction = light_pos
            light_state = traffic_lights[node][direction]["state"]
            color = GREEN if light_state == "green" else YELLOW if light_state == "yellow" else RED
            pygame.draw.circle(screen, color, (x, y), 8)
