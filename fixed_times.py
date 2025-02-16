import pygame
import networkx as nx

# Traffic light cycle function
def update_traffic_lights(traffic_lights, nodes):
    """Switch traffic lights between green, yellow, and red periodically."""
    for node in nodes:
        # Get the traffic light states for N, S, E, W directions
        n_light = traffic_lights[node]["N"]
        s_light = traffic_lights[node]["S"]
        e_light = traffic_lights[node]["E"]
        w_light = traffic_lights[node]["W"]

        # Update timers for N and S lights (synchronized)
        if n_light["state"] == "green":
            if n_light["timer"] < n_light["green"]:
                n_light["timer"] += 1
                s_light["timer"] += 1
            else:
                # Switch N and S to yellow
                n_light["state"] = "yellow"
                s_light["state"] = "yellow"
                n_light["timer"] = 0
                s_light["timer"] = 0
        elif n_light["state"] == "yellow":
            if n_light["timer"] < n_light["yellow"]:
                n_light["timer"] += 1
                s_light["timer"] += 1
            else:
                # Switch N and S to red, and E and W to green
                n_light["state"] = "red"
                s_light["state"] = "red"
                e_light["state"] = "green"
                w_light["state"] = "green"
                n_light["timer"] = 0
                s_light["timer"] = 0
                e_light["timer"] = 0
                w_light["timer"] = 0
                # Allow the first car in the E and W queues to proceed
                if e_light["queue"]:
                    e_light["queue"].pop(0)
                if w_light["queue"]:
                    w_light["queue"].pop(0)
        else:
            if n_light["timer"] < n_light["red"]:
                n_light["timer"] += 1
                s_light["timer"] += 1
            else:
                # Switch N and S to green, and E and W to red
                n_light["state"] = "green"
                s_light["state"] = "green"
                e_light["state"] = "red"
                w_light["state"] = "red"
                n_light["timer"] = 0
                s_light["timer"] = 0
                e_light["timer"] = 0
                w_light["timer"] = 0
                # Allow the first car in the N and S queues to proceed
                if n_light["queue"]:
                    n_light["queue"].pop(0)
                if s_light["queue"]:
                    s_light["queue"].pop(0)

        # Update timers for E and W lights (synchronized)
        if e_light["state"] == "green":
            if e_light["timer"] < e_light["green"]:
                e_light["timer"] += 1
                w_light["timer"] += 1
            else:
                # Switch E and W to yellow
                e_light["state"] = "yellow"
                w_light["state"] = "yellow"
                e_light["timer"] = 0
                w_light["timer"] = 0
        elif e_light["state"] == "yellow":
            if e_light["timer"] < e_light["yellow"]:
                e_light["timer"] += 1
                w_light["timer"] += 1
            else:
                # Switch E and W to red, and N and S to green
                e_light["state"] = "red"
                w_light["state"] = "red"
                n_light["state"] = "green"
                s_light["state"] = "green"
                e_light["timer"] = 0
                w_light["timer"] = 0
                n_light["timer"] = 0
                s_light["timer"] = 0
                # Allow the first car in the N and S queues to proceed
                if n_light["queue"]:
                    n_light["queue"].pop(0)
                if s_light["queue"]:
                    s_light["queue"].pop(0)
        else:
            if e_light["timer"] < e_light["red"]:
                e_light["timer"] += 1
                w_light["timer"] += 1
            else:
                # Switch E and W to green, and N and S to red
                e_light["state"] = "green"
                w_light["state"] = "green"
                n_light["state"] = "red"
                s_light["state"] = "red"
                e_light["timer"] = 0
                w_light["timer"] = 0
                n_light["timer"] = 0
                s_light["timer"] = 0
                # Allow the first car in the E and W queues to proceed
                if e_light["queue"]:
                    e_light["queue"].pop(0)
                if w_light["queue"]:
                    w_light["queue"].pop(0)
