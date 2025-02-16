WIDTH, HEIGHT = 1400, 1200
FPS = 30
MAX_GREEN_TIME = 100
MAX_RED_TIME = 100
YELLOW_TIME = 20
STOP_DISTANCE = 40
CAR_GAP = 30
MAX_QUEUE_LENGTH = 5
WINDOW_SIZE = 60
NUM_CARS = 100
CYCLE_BASE = 50
SIM_MODE = 1  # 1: Fixed Time, 2: SCOOT

WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
YELLOW = (200, 200, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GRAY = (100, 100, 100)


# Add road nodes (intersections)
# Grid Configuration (Adjustable Rows and Columns)
ROWS = 5
COLS = 6

# Calculate node positions based on grid configuration
node_spacing_x = WIDTH // (COLS + 1)
node_spacing_y = HEIGHT // (ROWS + 1)

class CircularArray:
    def __init__(self, capacity):
        self.capacity = capacity
        self.array = [None] * capacity
        self.index = 0
        self.count = 0

    def add(self, value):
        self.array[self.index] = value
        self.index = (self.index + 1) % self.capacity
        if self.count < self.capacity:
            self.count += 1

    def get_array(self):
        return self.array

    def average(self):
        valid_values = [x for x in self.array if x is not None]
        return sum(valid_values) / len(valid_values) if valid_values else 0
