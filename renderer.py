import conway
import launchpad
import random


COLOR_MODE_ALL_RANDOM = 'COLOR_MODE_ALL_RANDOM'
COLOR_MODE_RANDOM_PER_TURN = 'COLOR_MODE_RANDOM_PER_TURN'
COLOR_MODE_WHITE = 'COLOR_MODE_WHITE'

COLOR_MODES = [
    COLOR_MODE_ALL_RANDOM,
    COLOR_MODE_RANDOM_PER_TURN,
    COLOR_MODE_WHITE,
]
COLOR_MODE = COLOR_MODE_ALL_RANDOM

LAST_COLOR_USED_FOR_TURN = launchpad.COLOR_OFF


def draw_grid(lpad, grid):
    global LAST_COLOR_USED_FOR_TURN
    color = None # random

    if COLOR_MODE == COLOR_MODE_RANDOM_PER_TURN:
        color = random.choice(list(filter(lambda c: c != LAST_COLOR_USED_FOR_TURN, launchpad.COLORS)))
        LAST_COLOR_USED_FOR_TURN = color
    elif COLOR_MODE == COLOR_MODE_WHITE:
        color = launchpad.COLOR_WHITE

    for x in range(0, conway.GRID_WIDTH):
        for y in range(0, conway.GRID_HEIGHT):
            pad = lpad.get_grid_pad(x, y)
            if grid[x][y]:
                pad.set_on(color=color)
            else:
                pad.set_off()


def toggle_next_mode():
    global COLOR_MODE
    i = (COLOR_MODES.index(COLOR_MODE) + 1) % len(COLOR_MODES)
    COLOR_MODE = COLOR_MODES[i]


def toggle_pad(pad):
    color = None

    if COLOR_MODE == COLOR_MODE_RANDOM_PER_TURN:
        color = LAST_COLOR_USED_FOR_TURN
    elif COLOR_MODE == COLOR_MODE_WHITE:
        color = launchpad.COLOR_WHITE

    pad.toggle(color=color)