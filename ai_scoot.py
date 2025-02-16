from scoot import calculate_cycle
from definitions import *
import numpy as np

scoot_cycle = 8 * FPS

def ai_update_traffic_lights(frame_count, traffic_lights, nodes, agent):
    global scoot_cycle  # Use global to modify the outer scoot_cycle variable
    if frame_count % scoot_cycle == 0:
        scoot_cycle = calculate_cycle(traffic_lights, nodes)/10

    yellow_time = 0.5 * FPS  # Fixed yellow light duration

    for node in nodes:
        n_light = traffic_lights[node]["N"]
        s_light = traffic_lights[node]["S"]
        e_light = traffic_lights[node]["E"]
        w_light = traffic_lights[node]["W"]

        # Light control logic
        if n_light["state"] == "green":
            if n_light["timer"] < n_light["green"]:
                n_light["timer"] += 1
                s_light["timer"] += 1
                if n_light["queue"]:
                    n_light["queue"].pop(0)
                if s_light["queue"]:
                    s_light["queue"].pop(0)
            else:
                n_light["state"], s_light["state"] = "yellow", "yellow"
                n_light["timer"], s_light["timer"] = 0, 0

        elif n_light["state"] == "yellow":
            if n_light["timer"] < yellow_time:
                n_light["timer"] += 1
                s_light["timer"] += 1
            else:
                n_light["state"], s_light["state"] = "red", "red"
                e_light["state"], w_light["state"] = "green", "green"
                e_light["timer"], w_light["timer"] = 0, 0
                calculate_split_ai(traffic_lights, node, "E", "W", agent, nodes)

        elif e_light["state"] == "green":
            if e_light["timer"] < e_light["green"]:
                e_light["timer"] += 1
                w_light["timer"] += 1
                if e_light["queue"]:
                    e_light["queue"].pop(0)
                if w_light["queue"]:
                    w_light["queue"].pop(0)
            else:
                e_light["state"], w_light["state"] = "yellow", "yellow"
                e_light["timer"], w_light["timer"] = 0, 0

        elif e_light["state"] == "yellow":
            if e_light["timer"] < yellow_time:
                e_light["timer"] += 1
                w_light["timer"] += 1
            else:
                e_light["state"], w_light["state"] = "red", "red"
                n_light["state"], s_light["state"] = "green", "green"
                n_light["timer"], s_light["timer"] = 0, 0
                calculate_split_ai(traffic_lights, node, "N", "S", agent, nodes)

    return scoot_cycle

def calculate_split_ai(traffic_lights, node, dir1, dir2, agent, nodes):
    light1 = traffic_lights[node][dir1]
    light2 = traffic_lights[node][dir2]

    # Get the current state (all queues of all nodes)
    state = np.array([len(traffic_lights[n][d]["queue"]) for n in nodes for d in ["N", "S", "E", "W"]])

    # Use the AI agent to determine the green time
    action = agent.choose_action(state)
    green_time = max(1, action) * FPS  # Ensure green time is at least 1

    # Assign times to lights
    light1["green"] = green_time
    light2["green"] = green_time