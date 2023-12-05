# maze_solver.py
import random
from collections import deque
import time

def generate_maze(width, height):
    """Generates a maze of given width and height."""
    # Initialize maze with walls
    maze = [["#" for _ in range(width)] for _ in range(height)]

    # Depth-First Search to carve paths
    def dfs(x, y):
        directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        random.shuffle(directions)  # Randomize directions

        for dx, dy in directions:
            nx, ny = x + dx*2, y + dy*2
            if 0 <= nx < height and 0 <= ny < width and maze[nx][ny] == "#":
                maze[nx][ny] = " "
                maze[x+dx][y+dy] = " "  # Remove wall
                dfs(nx, ny)

    # Start DFS from a corner of the maze
    start_x, start_y = 0, 0
    maze[start_x][start_y] = " "
    dfs(start_x, start_y)

    return maze


def get_coordinates_input(prompt, maze):
    """Gets valid coordinates input from the user."""
    while True:
        try:
            x, y = map(int, input(prompt).split())
            if 0 <= x < len(maze) and 0 <= y < len(maze[0]) and maze[x][y] != "#":
                return (x, y)
            else:
                print("Invalid input. Please enter coordinates within the maze.")
        except ValueError:
            print("Invalid input. Please enter two integers separated by space.")

def get_maze_size_input(prompt, min_size=4, max_size=10):
    """Gets valid maze dimensions input from the user."""
    while True:
        try:
            width, height = map(int, input(prompt).split())
            if min_size <= width <= max_size and min_size <= height <= max_size:
                return width, height
            else:
                print(f"Invalid input. Please enter dimensions within {min_size}x{min_size} and {max_size}x{max_size}")
        except ValueError:
            print("Invalid input. Please enter two numbers separated by a space.")

def print_maze(maze):
    """Prints the maze."""
    height = len(maze)
    width = len(maze[0]) if height > 0 else 0

    # Print column numbers with reduced spacing
    print("     " + " ".join(str(i).rjust(1) for i in range(width)))

    # Adjust the separator line to match the new spacing
    print("   " + "-" * (2 * width))

    # Print each row with row numbers, adjust spacing as needed
    for i, row in enumerate(maze):
        row_number = str(i).rjust(2)  # Adjust rjust for alignment if maze is very large
        print(f"{row_number} | " + " ".join(row))

    print()


def bfs_maze_solver(maze, start, end, step_delay=0.5):
    print("Maze Solver")

    if maze[start[0]][start[1]] == "#" or maze[end[0]][end[1]] == "#":
        print("Start or end point is blocked.")
        return
    if start == end:
        print("Start and end points are the same.")
        return

    directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    queue = deque([start])
    predecessors = {start: None}  # Dictionary to store predecessors

    while queue:
        current_position = queue.popleft()
        x, y = current_position

        # Mark the current cell with a special character
        if maze[x][y] == " ":
            maze[x][y] = "O"

        print_maze(maze)
        time.sleep(step_delay)

        if current_position == end:
            reconstruct_path(maze, predecessors, start, end)
            print("You reached the end!")
            return

        # Explore neighbors
        for dx, dy in directions:
            next_x, next_y = x + dx, y + dy

            if 0 <= next_x < len(maze) and 0 <= next_y < len(maze[0]) and maze[next_x][next_y] == " " and (next_x, next_y) not in predecessors:
                queue.append((next_x, next_y))
                predecessors[(next_x, next_y)] = current_position
        
        for x in range(len(maze)):
            for y in range(len(maze[0])):
                if maze[x][y] == "O":
                    maze[x][y] = " "

    print("No path found")

def reconstruct_path(maze, predecessors, start, end):
    current = end
    while current and current != start: # Ensure current is not None
        maze[current[0]][current[1]] = "." # Mark as part of the path
        current = predecessors.get(current) # Safely get the predecessor

    # Mark start and end points; replace path marker if present
    maze[start[0]][start[1]] = "S"
    maze[end[0]][end[1]] = "E"


def main():
    """Main function to run the maze solver program."""

    # Ask user to choose size for maze
    print("Enter the size of the maze (width height): ")
    maze_width, maze_height = get_maze_size_input("Enter width and height (e.g., '10 10'): ")
    # Generate the maze
    solvable_maze = generate_maze(maze_width, maze_height)

    # Print the generated maze
    print("Generated Maze:")
    print_maze(solvable_maze)

    # Get user input for start and end points
    start = get_coordinates_input("Enter start coordinates (row column (e.g., '0 4')): ", solvable_maze)
    end = get_coordinates_input("Enter end coordinates (row column (e.g., '0 4')): ", solvable_maze)

    bfs_maze_solver(solvable_maze, start, end)

    print("Solved Maze:")
    print_maze(solvable_maze)

if __name__ == "__main__":
    main()