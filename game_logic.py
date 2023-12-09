import numpy as np
import random
import matplotlib
matplotlib.use('TkAgg')
from main import ship_sizes,grid_size,num_test_simulations_efficient,ships


def create_grid(size):
    """Creating an empty grid with the given size"""
    return np.zeros((size, size), dtype=int)

# def is_valid_placement(grid, row, col, ship_size, orientation):
#     """
#     Checking if a placement is valid or not
#     """
#     max_row, max_col = grid.shape
#
#     if orientation == 'H':
#         if col + ship_size > max_col:
#             return False
#         row_range = range(row - 1, row + 2)
#         col_range = range(col - 1, col + ship_size + 1)
#     else:  # orientation == 'V'
#         if row + ship_size > max_row:
#             return False
#         row_range = range(row - 1, row + ship_size + 1)
#         col_range = range(col - 1, col + 2)
#
#     for r in row_range:
#         for c in col_range:
#             if 0 <= r < max_row and 0 <= c < max_col and grid[r, c] == 1:
#                 return False
#
#     return True

def place_ship(grid, row, col, ship_size, orientation):
    """
    Place a ship on the grid using the placement check.
    """
    if is_valid_placement(grid, row, col, ship_size, orientation):
        for i in range(ship_size):
            if orientation == 'H':
                grid[row, col + i] = 1
            else:
                grid[row + i, col] = 1

def randomly_place_all_ships(grid, ship_sizes):
    """
    Randomly place all ships on the grid using the placement logic.
    """
    for ship_size in ship_sizes:
        placed = False
        while not placed:
            row = random.randint(0, grid.shape[0] - 1)
            col = random.randint(0, grid.shape[1] - 1)
            orientation = random.choice(['H', 'V'])
            if is_valid_placement(grid, row, col, ship_size, orientation):
                place_ship(grid, row, col, ship_size, orientation)
                placed = True


# Example ship data structure (size, hits)

def update_ships(ships, hit_row, hit_col, player_board):
    ship_destroyed = False
    destroyed_ship_cells = []

    for ship in ships:
        if (hit_row, hit_col) in ship['coordinates']:
            ship['hits'] += 1
            player_board[hit_row][hit_col] = 2  # Mark as part of a destroyed ship
            if ship['hits'] == ship['size']:
                ship_destroyed = True
                destroyed_ship_cells = ship['coordinates']
                break

    return ship_destroyed, destroyed_ship_cells


def is_valid_placement(grid, row, col, ship_size, orientation):
    """
    Check if a ship can be placed at the given location.
    This version minimizes the number of checks for valid placement.
    """
    max_row, max_col = grid.shape

    if orientation == 'H':
        if col + ship_size > max_col:
            return False
        row_range = range(row - 1, row + 2)
        col_range = range(col - 1, col + ship_size + 1)
    else:  # orientation == 'V'
        if row + ship_size > max_row:
            return False
        row_range = range(row - 1, row + ship_size + 1)
        col_range = range(col - 1, col + 2)

    for r in row_range:
        for c in col_range:
            if 0 <= r < max_row and 0 <= c < max_col and grid[r, c] == 1:
                return False

    return True

def place_ship(grid, row, col, ship_size, orientation):
    """
    Place a ship on the grid using the placement check.
    """
    if is_valid_placement(grid, row, col, ship_size, orientation):
        for i in range(ship_size):
            if orientation == 'H':
                grid[row, col + i] = 1
            else:
                grid[row + i, col] = 1

def randomly_place_all_ships(grid, ship_sizes):
    """
    Randomly place all ships on the grid using the placement logic.
    """
    for ship_size in ship_sizes:
        placed = False
        while not placed:
            row = random.randint(0, grid.shape[0] - 1)
            col = random.randint(0, grid.shape[1] - 1)
            orientation = random.choice(['H', 'V'])
            if is_valid_placement(grid, row, col, ship_size, orientation):
                place_ship(grid, row, col, ship_size, orientation)
                placed = True




# Simulate player placing ships
player_board = create_grid(7)
def print_board(board):
    """Print the game board in a readable format."""
    for row in board:
        print(' '.join(str(cell) for cell in row))
    print()




def generate_ship_coordinates(start_row, start_col, ship_size, orientation):
    """Generate coordinates for a ship based on its starting position, size, and orientation."""
    return [(start_row + i if orientation == 'V' else start_row,
             start_col + i if orientation == 'H' else start_col) for i in range(ship_size)]

def simulate_player_ship_placement(grid, ships):
    """Simulate the player placing their ships on the grid."""
    for ship in ships:
        ship_size = ship['size']
        start_row, start_col, orientation = ship['placement']
        ship['coordinates'] = generate_ship_coordinates(start_row, start_col, ship_size, orientation)

        # Place the ship on the grid
        for row, col in ship['coordinates']:
            grid[row][col] = 1



# Place ships first,then print the board
simulate_player_ship_placement(player_board, ships)

print("Player's board with ships placed:")
print_board(player_board)


