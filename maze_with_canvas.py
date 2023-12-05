# maze_solver.py
import random
from collections import deque
import time
import tkinter as tk

def generate_maze(width, height):
    # Initialize maze with walls
    maze = [["#" for _ in range(width)] for _ in range(height)]

    # Initialize variables to track the farthest point
    farthest_point = (0, 0)
    max_distance = 0

    def dfs(x, y, distance=0):
        nonlocal farthest_point, max_distance
        directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        random.shuffle(directions)  # Randomize directions

        for dx, dy in directions:
            nx, ny = x + dx*2, y + dy*2
            if 0 <= nx < height and 0 <= ny < width and maze[nx][ny] == "#":
                maze[nx][ny] = " "
                maze[x+dx][y+dy] = " "  # Remove wall
                next_distance = distance + 1
                if next_distance > max_distance:
                    max_distance = next_distance
                    farthest_point = (nx, ny)
                dfs(nx, ny, next_distance)

    # Start DFS from a corner of the maze
    start_x, start_y = 0, 0
    maze[start_x][start_y] = " "
    dfs(start_x, start_y)

    # Use the farthest point as the endpoint
    end_x, end_y = farthest_point
    maze[end_x][end_y] = " "

    return maze, (end_x, end_y)

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


def draw_maze_on_canvas(maze, canvas, start, end, cell_size=20):
    for x, row in enumerate(maze):
        for y, cell in enumerate(row):
            if (x, y) == start:
                color = "blue"
            elif (x, y) == end:
                color = "red"
            else:
                color = "black" if cell == "#" else "white"
            canvas.create_rectangle(y * cell_size, x * cell_size, (y + 1) * cell_size, (x + 1) * cell_size, fill=color)

def bfs_maze_solver(maze, start, end, canvas, cell_size=20, step_delay=0.15):
    queue = deque([start])
    predecessors = {start: None}
    visited_cells = set()

    while queue:
        current_position = queue.popleft()
        x, y = current_position

        if maze[x][y] == " ":
            visited_cells.add((x, y))
            canvas.create_rectangle(y * cell_size, x * cell_size, (y + 1) * cell_size, (x + 1) * cell_size, fill="gray")
            canvas.update()
            time.sleep(step_delay)

        if current_position == end:
            reconstruct_path(maze, predecessors, start, end, canvas, cell_size)
            print("You reached the end!")
            return

        for dx, dy in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
            next_x, next_y = x + dx, y + dy
            if 0 <= next_x < len(maze) and 0 <= next_y < len(maze[0]) and maze[next_x][next_y] == " " and (next_x, next_y) not in visited_cells:
                queue.append((next_x, next_y))
                predecessors[(next_x, next_y)] = current_position

    print("No path found")

def reconstruct_path(maze, predecessors, start, end, canvas, cell_size=20):
    current = end
    while current and current != start: # Ensure current is not None
        x, y = current
        maze[current[0]][current[1]] = "." # Mark as part of the path
        canvas.create_rectangle(y * cell_size, x * cell_size, (y + 1) * cell_size, (x + 1) * cell_size, fill="lime green")
        current = predecessors.get(current) # Safely get the predecessor

        sx, sy = start
        ex, ey = end
        canvas.create_rectangle(sy * cell_size, sx * cell_size, (sy + 1) * cell_size, (sx + 1) * cell_size, fill="blue")
        canvas.create_rectangle(ey * cell_size, ex * cell_size, (ey + 1) * cell_size, (ex + 1) * cell_size, fill="red")



def main():
    root = tk.Tk()
    root.title("Maze Solver")

    maze_width, maze_height = 20, 20
    cell_size = 20
    canvas = tk.Canvas(root, width=maze_width * cell_size, height=maze_height * cell_size)
    canvas.pack()

    solvable_maze, end_point = generate_maze(maze_width, maze_height)
    start_point = (0, 0)  # Starting point

    draw_maze_on_canvas(solvable_maze, canvas, start_point, end_point, cell_size)

    bfs_maze_solver(solvable_maze, start_point, end_point, canvas, cell_size)

    root.mainloop()

if __name__ == "__main__":
    main()