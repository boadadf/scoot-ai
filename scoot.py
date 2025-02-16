from definitions import FPS, CYCLE_BASE

# SCOOT
K = .8
SATURATION_FLOW = 19
BASE_CYCLE = 8

scoot_cycle = 8 * FPS
min_green_time = 1  # Minimum green time per phase (to allow car movement)

# The cycle is calculated for all the junctions
def calculate_cycle(traffic_lights, nodes):
    # 30 frames = 1 second
    min_cycle_time = 8 * FPS  # Minimum total cycle time (in frames)
    max_cycle_time = 80 * FPS  # Maximum total cycle time

    max_queue = 1
    for node in nodes:
        n_light = traffic_lights[node]["N"]
        s_light = traffic_lights[node]["S"]
        e_light = traffic_lights[node]["E"]
        w_light = traffic_lights[node]["W"]

        # Get queue lengths
        n_queue = len(n_light["queue"])
        s_queue = len(s_light["queue"])
        e_queue = len(e_light["queue"])
        w_queue = len(w_light["queue"])

        max_queue = max(max_queue, n_queue, s_queue, e_queue, w_queue)

    cycle = (BASE_CYCLE + K * max_queue) * FPS

    if cycle < min_cycle_time:
        return min_cycle_time
    elif cycle > max_cycle_time:
        return max_cycle_time
    else:
        return cycle

def scoot_update_traffic_lights(frame_count, traffic_lights, nodes):
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
                calculate_split_ew(traffic_lights, node)

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
                calculate_split_ns(traffic_lights, node)

    return scoot_cycle

def calculate_split_ns(traffic_lights, node):
    n_light = traffic_lights[node]["N"]
    s_light = traffic_lights[node]["S"]

    # Get queue lengths
    n_queue = len(n_light["queue"])
    s_queue = len(s_light["queue"])

    max_queue_ns = max(min_green_time, n_queue, s_queue)

    green_ns = max_queue_ns * K * FPS  # scoot_cycle

    # Assign times to lights
    n_light["green"] = green_ns
    s_light["green"] = green_ns

def calculate_split_ew(traffic_lights, node):
    e_light = traffic_lights[node]["E"]
    w_light = traffic_lights[node]["W"]

    # Get queue lengths
    e_queue = len(e_light["queue"])
    w_queue = len(w_light["queue"])

    max_queue_ew = max(min_green_time, e_queue, w_queue)

    green_ew = max_queue_ew * K * FPS  # scoot_cycle

    # Assign times to lights
    e_light["green"] = green_ew
    w_light["green"] = green_ew