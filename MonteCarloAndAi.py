import random
import numpy as np
from game_logic import create_grid,randomly_place_all_ships,num_test_simulations_efficient,grid_size,ship_sizes,player_board,update_ships,ships,simulate_player_ship_placement
import matplotlib.pyplot as plt
import seaborn as sns

def run_monte_carlo_simulations_efficient(num_simulations, grid_size, ship_sizes):
    """
    Run Monte Carlo simulations using the efficient placement logic.
    """
    placement_frequency = np.zeros((grid_size, grid_size), dtype=int)
    for _ in range(num_simulations):
        grid = create_grid(grid_size)
        randomly_place_all_ships(grid, ship_sizes)
        placement_frequency += grid
    return placement_frequency

# Testing the efficient version with a reduced number of simulations for performance evaluation
test_placement_frequency_efficient = run_monte_carlo_simulations_efficient(num_test_simulations_efficient, grid_size, ship_sizes)
print(test_placement_frequency_efficient)  # Displaying the test placement frequency grid

def ai_make_move(ai_probabilities, player_board, last_hits):
    """AI makes a move based on the highest probability cell."""
    chosen_cell = None

    if last_hits:
        # Gather potential targets adjacent to the last hit
        last_hit = last_hits[-1]
        row, col = last_hit
        potential_targets = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]

        # Filter out invalid, already hit, or zero probability cells
        valid_targets = [(r, c) for r, c in potential_targets
                         if 0 <= r < ai_probabilities.shape[0]
                         and 0 <= c < ai_probabilities.shape[1]
                         and player_board[r][c] == 0
                         and ai_probabilities[r][c] > 0]

        # Sort valid targets by probability and choose the highest
        if valid_targets:
            valid_targets.sort(key=lambda x: ai_probabilities[x[0], x[1]], reverse=True)
            chosen_cell = valid_targets[0]

    if not chosen_cell:
        # If no valid target is found, revert to general targeting
        # Choose the cell with the overall highest probability
        candidates = np.argwhere(ai_probabilities == np.max(ai_probabilities))
        untargeted_candidates = [cell for cell in candidates
                                 if player_board[cell[0], cell[1]] == 0
                                 and ai_probabilities[cell[0], cell[1]] > 0]

        if untargeted_candidates:
            chosen_cell = untargeted_candidates[0]
        else:
            chosen_cell = candidates[0]

    # Determining if it's a hit or miss
    hit = player_board[chosen_cell[0], chosen_cell[1]] == 1
    return chosen_cell, hit



def clear_adjacent_cells(ai_probabilities, ship_cells):
    """Zero out probabilities for all cells adjacent to the destroyed ship."""
    for cell in ship_cells:
        row, col = cell
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            adj_row, adj_col = row + dr, col + dc
            if 0 <= adj_row < ai_probabilities.shape[0] and 0 <= adj_col < ai_probabilities.shape[1]:
                ai_probabilities[adj_row][adj_col] = 0


def update_probabilities(ai_probabilities, row, col, hit, player_board, last_hits):
    # Set the probability of the targeted cell to zero, as it is already a hit or a miss
    ai_probabilities[row, col] = 0

    if hit:
        # Adjusting multipliers, the numbers were chosen by us
        direction_multiplier = 2
        default_multiplier = 1.8

        # Determine if there is a known direction (horizontal or vertical)
        known_direction = None
        if len(last_hits) >= 2:
            if last_hits[-1][0] == last_hits[-2][0]:
                known_direction = 'horizontal'
            elif last_hits[-1][1] == last_hits[-2][1]:
                known_direction = 'vertical'

        # Zero out diagonal cells as they cannot be part of the same ship
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            adj_row, adj_col = row + dr, col + dc
            if 0 <= adj_row < ai_probabilities.shape[0] and 0 <= adj_col < ai_probabilities.shape[1]:
                ai_probabilities[adj_row][adj_col] = 0

        # Increase probabilities for adjacent cells
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            adj_row, adj_col = row + dr, col + dc
            if 0 <= adj_row < ai_probabilities.shape[0] and 0 <= adj_col < ai_probabilities.shape[1]:
                multiplier = default_multiplier
                if known_direction == 'horizontal' and dc != 0:
                    multiplier = direction_multiplier
                elif known_direction == 'vertical' and dr != 0:
                    multiplier = direction_multiplier
                ai_probabilities[adj_row][adj_col] *= multiplier

    else:
        # Reduce probabilities for surrounding cells on a miss
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                adj_row, adj_col = row + dr, col + dc
                if 0 <= adj_row < ai_probabilities.shape[0] and 0 <= adj_col < ai_probabilities.shape[1]:
                    ai_probabilities[adj_row][adj_col] *= 0.95

    print(f"Updated probabilities after {'hit' if hit else 'miss'} at ({row}, {col})")
    for row in ai_probabilities:
        print(' '.join(f'{val:.3f}' for val in row))





def play_ai_game(player_board, ai_probabilities, ships):
    steps = 0
    last_hits = []  # Track all hits to determine ship direction

    while np.any(player_board == 1):
        # Choose the next move based on AI strategy
        ai_move, hit = ai_make_move(ai_probabilities, player_board, last_hits)
        row, col = ai_move

        if hit:
            # Update the ship's status and check if it's destroyed
            ship_destroyed, destroyed_ship_cells = update_ships(ships, row, col, player_board)
            if ship_destroyed:
                # Clear probabilities around the destroyed ship and reset last_hits
                clear_adjacent_cells(ai_probabilities, destroyed_ship_cells)
                last_hits.clear()
            else:
                # Add the hit to last_hits for further targeting
                last_hits.append((row, col))
        else:
            # Clear last_hits if the AI misses
            last_hits.clear()

        # Update probabilities based on the latest move
        update_probabilities(ai_probabilities, row, col, hit, player_board,last_hits)
        steps += 1

    return steps



# Playing the game
ai_probabilities = test_placement_frequency_efficient / num_test_simulations_efficient  # Using demo probabilities for this example
steps_taken = play_ai_game(player_board, ai_probabilities,ships)

print(f"The AI sunk all ships in {steps_taken} steps.")





##Below part is for the statistical analysis purposes

# plt.figure(figsize=(10, 8))
# sns.heatmap(test_placement_frequency_efficient, annot=True, cmap='viridis', fmt='d')
# plt.title("Heatmap of Ship Placement Frequencies from Monte Carlo Simulations, 5000 times")
# plt.xlabel("Column")
# plt.ylabel("Row")
# plt.show()
# def run_games(num_iterations, grid_size, ship_sizes):
#     results = []
#     for _ in range(num_iterations):
#         # Initialize the game board
#         player_board = create_grid(grid_size)
#
#         # Define the ships with their sizes and predetermined placements
#         # The placements should be tuples of (start_row, start_col, orientation)
#
#
#         # Simulate placing ships on the player_board
#         simulate_player_ship_placement(player_board, ships)
#
#         # Initialize AI probabilities
#         ai_probabilities = run_monte_carlo_simulations_efficient(num_test_simulations_efficient, grid_size, ship_sizes)
#
#         # Run the game
#         steps = play_ai_game(player_board, ai_probabilities, ships)
#         results.append(steps)
#     return results

# # Specify the number of iterations you want to run
# num_iterations = 100  # or any other number of iterations you want
#
# # Run the simulations and collect the results
# all_steps_taken = run_games(num_iterations, grid_size, ship_sizes)

# Now you can use all_steps_taken to perform your statistical analysis


# Now you can use all_steps_taken to perform your statistical analysis
# For example, calculate the mean, median, min, max, and standard deviation
# mean_steps = np.mean(all_steps_taken)
# median_steps = np.median(all_steps_taken)
# min_steps = np.min(all_steps_taken)
# max_steps = np.max(all_steps_taken)
# std_dev_steps = np.std(all_steps_taken)
# import matplotlib.pyplot as plt
# # Print the statistical results
# print(f"Over {num_iterations} iterations:")
# print(f"Mean steps: {mean_steps}")
# print(f"Median steps: {median_steps}")
# print(f"Minimum steps: {min_steps}")
# print(f"Maximum steps: {max_steps}")
# print(f"Standard deviation of steps: {std_dev_steps}")
#
# plt.hist(all_steps_taken, bins=20, alpha=0.75, color='blue')
# plt.title('Histogram of Steps Taken to Sink All Ships')
# plt.xlabel('Steps')
# plt.ylabel('Frequency')
# plt.show()

# plt.plot(sorted(all_steps_taken))
# plt.title('Line Plot of Steps Taken to Sink All Ships')
# plt.xlabel('Simulation Iteration')
# plt.ylabel('Steps Taken')
# plt.show()

# plt.boxplot(all_steps_taken, vert=False)
# plt.title('Box Plot of Steps Taken to Sink All Ships')
# plt.xlabel('Steps Taken')
# plt.show()
#
# categories = ['Min', 'Mean', 'Median', 'Max']
# values = [min_steps, mean_steps, median_steps, max_steps]
# plt.bar(categories, values, color=['green', 'blue', 'orange', 'red'])
# plt.title('Bar Chart of Descriptive Statistics')
# plt.xlabel('Statistic')
# plt.ylabel('Steps Taken')
# plt.show()
#
#
# plt.scatter(range(len(all_steps_taken)), all_steps_taken)
# plt.title('Scatter Plot of Steps Taken to Sink All Ships')
# plt.xlabel('Simulation Iteration')
# plt.ylabel('Steps Taken')
# plt.show()



