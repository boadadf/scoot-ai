import pygame
from definitions import *

def display_sim_mode(screen, SIM_MODE):
    font = pygame.font.Font(None, 36)
    if SIM_MODE == 1:
        mode_text = "Mode: Fixed Time"
    elif SIM_MODE == 2:
        mode_text = "Mode: SCOOT"
    else:
        mode_text = "Mode: Unknown"
    text_surface = font.render(mode_text, True, BLACK)
    screen.blit(text_surface, (10, 10))

    # Display queue lengths for each traffic light
def display_statistics(screen, nodes, traffic_lights, stopped_buffer, cycle_time):
    font = pygame.font.Font(None, 24)
    bottom_font = pygame.font.Font(None, 30)
    for node, pos in nodes.items():
        # Get the queue lengths for N, S, E, W directions
        n_queue_length = len(traffic_lights[node]["N"]["queue"])
        s_queue_length = len(traffic_lights[node]["S"]["queue"])
        e_queue_length = len(traffic_lights[node]["E"]["queue"])
        w_queue_length = len(traffic_lights[node]["W"]["queue"])


        # Display the current queue lengths and the 30 seconds average
        x, y = pos
        text_n = font.render(f"N: {n_queue_length}", True, BLACK)
        text_s = font.render(f"S: {s_queue_length}", True, BLACK)
        text_e = font.render(f"E: {e_queue_length}", True, BLACK)
        text_w = font.render(f"W: {w_queue_length}", True, BLACK)

        # Display current and average queue lengths above the intersection
        screen.blit(text_n, (x + 10, y - 80))  # Display N queue above the intersection
        screen.blit(text_s, (x + 10, y - 60))  # Display S queue above the intersection
        screen.blit(text_e, (x + 10, y - 40))  # Display E queue above the intersection
        screen.blit(text_w, (x + 10, y - 20))  # Display W queue above the intersection
    
    avg_text = bottom_font.render(f"Cycle: {cycle_time:.0f}", True, (0, 0, 0))
    screen.blit(avg_text, (10, 40))
    avg_text = bottom_font.render(f"Avg Stop time: {stopped_buffer.average():.2f}", True, (0, 0, 0))
    screen.blit(avg_text, (10, 60))
