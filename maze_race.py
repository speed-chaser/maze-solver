# maze_solver.py
import random
from collections import deque
import time
import tkinter as tk

class MazeSolver:
    def __init__(self, maze_width, maze_height, cell_size):
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.cell_size = cell_size
        self.is_drawing = False
        self.drawn_cells = set()  # Keep track of drawn cells
        self.maze_completed = False  # Flag to indicate if the maze is completed
        self.accessible_tiles = set([(0, 0)])  # Start with only the starting point as accessible
        self.user_path = []
        self.init_ui()


    def init_ui(self):
        self.root = tk.Tk()
        self.root.title("Maze Solver Comparison")

        self.user_canvas = tk.Canvas(self.root, width=self.maze_width * self.cell_size, height=self.maze_height * self.cell_size, bg="white")
        self.algo_canvas = tk.Canvas(self.root, width=self.maze_width * self.cell_size, height=self.maze_height * self.cell_size, bg="white")

        self.user_canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.user_canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.user_canvas.bind("<B1-Motion>", self.on_mouse_move)

        self.user_canvas.pack(side="left", padx=10)
        self.algo_canvas.pack(side="right", padx=10)

        self.solvable_maze, self.end_point = self.generate_maze(self.maze_width, self.maze_height)
        self.draw_maze_on_canvas(self.solvable_maze, self.user_canvas, (0, 0), self.end_point, self.cell_size)
        self.draw_maze_on_canvas(self.solvable_maze, self.algo_canvas, (0, 0), self.end_point, self.cell_size)

        self.start = (0, 0)
        self.end = self.end_point

        # Start BFS solver on algo_canvas
        self.bfs_maze_solver(self.solvable_maze, self.start, self.end, self.algo_canvas, self.cell_size)

    def generate_maze(self, width, height):
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

    def print_maze(self, maze):
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

    def draw_maze_on_canvas(self, maze, canvas, start, end, cell_size=20):
        for x, row in enumerate(maze):
            for y, cell in enumerate(row):
                if (x, y) == start:
                    color = "blue"
                elif (x, y) == end:
                    color = "red"
                else:
                    color = "black" if cell == "#" else "white"
                canvas.create_rectangle(y * cell_size, x * cell_size, (y + 1) * cell_size, (x + 1) * cell_size, fill=color)

    def bfs_maze_solver(self, maze, start, end, canvas, cell_size=20, step_delay=0.25):
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
                # self.reconstruct_path(maze, predecessors, start, end, canvas, cell_size)
                print("You reached the end!")
                return

            for dx, dy in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
                next_x, next_y = x + dx, y + dy
                if 0 <= next_x < len(maze) and 0 <= next_y < len(maze[0]) and maze[next_x][next_y] == " " and (next_x, next_y) not in visited_cells:
                    queue.append((next_x, next_y))
                    predecessors[(next_x, next_y)] = current_position

        print("No path found")

    def reconstruct_path(self, maze, predecessors, start, end, canvas, cell_size=20):
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

    def on_mouse_down(self, event):
        self.is_drawing = True
        self.draw_path(event.x, event.y, self.user_canvas)

    def on_mouse_up(self, event):
        self.is_drawing = False

    def on_mouse_move(self, event):
        if self.is_drawing:
            self.draw_path(event.x, event.y, self.user_canvas)


    def draw_path(self, x, y, canvas):
        if self.maze_completed:  # Skip drawing if maze is completed
            return

        cell_x, cell_y = x // self.cell_size, y // self.cell_size

        if 0 <= cell_x < self.maze_width and 0 <= cell_y < self.maze_height:
            if self.solvable_maze[cell_y][cell_x] == "#":  # Skip walls
                return

            # Check if the cell is adjacent to the last cell in the user path
            if self.user_path and not self.is_adjacent((cell_x, cell_y), self.user_path[-1]):
                return

            # Draw the cell and add it to the user path
            if (cell_x, cell_y) not in self.user_path:  # Draw only if not already drawn
                canvas.create_rectangle(cell_x * self.cell_size, cell_y * self.cell_size, 
                                        (cell_x + 1) * self.cell_size, (cell_y + 1) * self.cell_size, fill="blue")
                self.user_path.append((cell_x, cell_y))

                if (cell_x, cell_y) == self.end:  # Check for end condition
                    self.handle_end_condition()

    def is_adjacent(self, cell1, cell2):
        # Check if two cells are adjacent (diagonals not considered adjacent)
        x1, y1 = cell1
        x2, y2 = cell2
        return (x1 == x2 and abs(y1 - y2) == 1) or (y1 == y2 and abs(x1 - x2) == 1)

    def handle_end_condition(self):
        if self.user_path[-1] != self.end:
            return  # Do nothing if the last drawn cell is not the end

        # Check if the drawn path is continuous and valid
        if all(self.is_adjacent(self.user_path[i], self.user_path[i + 1]) for i in range(len(self.user_path) - 1)):
            self.maze_completed = True
            for x, y in self.user_path:
                self.user_canvas.create_rectangle(y * self.cell_size, x * self.cell_size, 
                                                (y + 1) * self.cell_size, (x + 1) * self.cell_size, fill="lime green")
            print("Maze solved!")


def main():
    maze_solver = MazeSolver(20, 20, 20)
    maze_solver.root.mainloop()

if __name__ == "__main__":
    main()