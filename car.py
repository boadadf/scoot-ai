import pygame
import random
import math
import networkx as nx
from definitions import *


# Car class
class Car:
    def __init__(self, start_node, target_node, nodes, city_graph):
        self.path = nx.shortest_path(city_graph, start_node, target_node)
        self.current_index = 0
        self.x, self.y = nodes[self.path[self.current_index]]
        self.speed = 2
        self.color = random.choice([YELLOW, BLUE, ORANGE, PURPLE])
        self.width = 20
        self.height = 10
        self.stopped = False
        self.angle = 0
        self.safe_distance = CAR_GAP
        self.queue_position = None

    def move(self, cars, nodes, traffic_lights, city_graph):
        """Move car along its path and stop at red or yellow lights if far from the intersection."""
        if self.current_index < len(self.path) - 1:
            next_node = self.path[self.current_index + 1]
            target_x, target_y = nodes[next_node]

            # Calculate direction of movement
            dx = target_x - self.x
            dy = target_y - self.y
            distance_to_next_node = (dx ** 2 + dy ** 2) ** 0.5

            # Calculate the angle of movement
            self.angle = math.degrees(math.atan2(dy, dx))

            # Determine traffic light direction based on movement
            if dx > 0:  # Moving East
                light_direction = "E"
            elif dx < 0:  # Moving West
                light_direction = "W"
            elif dy > 0:  # Moving South
                light_direction = "S"
            elif dy < 0:  # Moving North
                light_direction = "N"

            # Check traffic light state at the next node
            light_state = traffic_lights[next_node][light_direction]["state"]

            # If the light is red or yellow, add the car to the queue
            if (light_state == "red" or light_state == "yellow") and distance_to_next_node <= STOP_DISTANCE + len(traffic_lights[next_node][light_direction]["queue"]) * CAR_GAP:
                if self not in traffic_lights[next_node][light_direction]["queue"]:
                    # Only add to the queue if there is space
                    if len(traffic_lights[next_node][light_direction]["queue"]) < MAX_QUEUE_LENGTH:
                        traffic_lights[next_node][light_direction]["queue"].append(self)
                    else:
                        # If the queue is full, stop the car but don't add it to the queue
                        self.stopped = True
                        return
                self.queue_position = traffic_lights[next_node][light_direction]["queue"].index(self)

                # If the car is in the queue, it should fully stop
                self.stopped = True
                self.move_towards(next_node, self.queue_position, nodes)  # Stop at the correct position in the queue
                return  # Do not move at all
            else:
                self.stopped = False
                if self in traffic_lights[next_node][light_direction]["queue"]:
                    traffic_lights[next_node][light_direction]["queue"].remove(self)
                self.queue_position = None

            # Move towards the next node
            if dx != 0:
                self.x += self.speed if dx > 0 else -self.speed
            if dy != 0:
                self.y += self.speed if dy > 0 else -self.speed

            # Check if reached the next node
            if (self.x, self.y) == nodes[next_node]:
                self.current_index += 1

        else:
            # At the target node, pick a new random target
            current_node = self.path[-1]
            neighbors = list(city_graph.neighbors(current_node))
            if len(self.path) > 1:  # Prevent U-turns
                next_node = random.choice([n for n in neighbors if n != self.path[-2]])
            else:
                next_node = random.choice(neighbors)
            self.path = [current_node, next_node]
            self.current_index = 0


    def move_towards(self, target_node, queue_position, nodes):
        """Stop car before intersection or behind another car, maintaining a safe distance."""
        target_x, target_y = nodes[target_node]

        # Calculate direction to the target
        dx = target_x - self.x
        dy = target_y - self.y

        # Calculate the stop position based on the queue position
        stop_distance = STOP_DISTANCE + queue_position * CAR_GAP

        # Move towards the target but stop at the stop distance
        if dx != 0:
            if abs(dx) > stop_distance:
                self.x += self.speed if dx > 0 else -self.speed
            else:
                self.x = target_x - (stop_distance if dx > 0 else -stop_distance)
        if dy != 0:
            if abs(dy) > stop_distance:
                self.y += self.speed if dy > 0 else -self.speed
            else:
                self.y = target_y - (stop_distance if dy > 0 else -stop_distance)

    def draw(self, screen):
        # Create a surface for the car
        car_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(car_surface, self.color, (0, 0, self.width, self.height))

        # Rotate the car surface based on the angle
        rotated_surface = pygame.transform.rotate(car_surface, -self.angle)
        rotated_rect = rotated_surface.get_rect(center=(self.x, self.y))

        # Draw the rotated car
        screen.blit(rotated_surface, rotated_rect.topleft)
