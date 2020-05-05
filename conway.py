import copy
import random

GRID_WIDTH = 8
GRID_HEIGHT = 8


def init_grid():
    grid = []
    for x in range(0, GRID_WIDTH):
        grid.append([])
        for y in range(0, GRID_HEIGHT):
            grid[x].append(False)
    return grid


def run_step(grid):
    new_grid = copy.deepcopy(grid)
    for i in range(0, GRID_WIDTH):
        for j in range(0, GRID_HEIGHT):
            is_alive = grid[i][j]
            living, dead = check_neighbors(grid, i, j)
            if is_alive and (living == 2 or living == 3):
                new_grid[i][j] = True
            elif not is_alive and living == 3:
                new_grid[i][j] = True
            else:
                new_grid[i][j] = False
    return new_grid


def check_neighbors(grid, x, y):
    living = 0
    dead = 0
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if i < 0:
                i = GRID_WIDTH + i
            if j < 0:
                j = GRID_HEIGHT + j
            if i > GRID_WIDTH-1:
                i = i - GRID_WIDTH
            if j > GRID_HEIGHT-1:
                j = j - GRID_HEIGHT

            if i < 0 or i > GRID_WIDTH-1 or j < 0 or j > GRID_HEIGHT-1 or (i == x and j == y):
                continue

            if grid[i][j]:
                living += 1
            else:
                dead += 1

    return living, dead


def clear_grid(grid):
    new_grid = copy.deepcopy(grid)
    for x in range(0, GRID_WIDTH):
        for y in range(0, GRID_HEIGHT):
            new_grid[x][y] = False
    return new_grid


def randomize_grid(grid):
    new_grid = copy.deepcopy(grid)
    for x in range(0, GRID_WIDTH):
        for y in range(0, GRID_HEIGHT):
            new_grid[x][y] = bool(random.getrandbits(1))
    return new_grid