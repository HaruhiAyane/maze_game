import random


def generate_maze(width, height):
    maze = [["#" for _ in range(width)] for _ in range(height)]
    start_pos = (1, 1)

    maze[start_pos[0]][start_pos[1]] = "S"

    def carve_passages(x, y):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + 2 * dx, y + 2 * dy
            if 1 <= nx < height - 1 and 1 <= ny < width - 1 and maze[nx][ny] == "#":
                maze[x + dx][y + dy] = "o"
                maze[nx][ny] = "o"
                carve_passages(nx, ny)

    maze[start_pos[0]][start_pos[1]] = "o"
    carve_passages(start_pos[0], start_pos[1])

    # ゴール位置を設定
    goal_pos = (height - 2, width - 2)
    while maze[goal_pos[0]][goal_pos[1]] != "o":
        goal_pos = (random.randint(1, height - 2), random.randint(1, width - 2))
    maze[goal_pos[0]][goal_pos[1]] = "G"

    # スタート位置を再設定
    maze[start_pos[0]][start_pos[1]] = "S"

    return maze


def print_maze(maze):
    for row in maze:
        print("".join(row))


def maze_to_string(maze):
    return ["".join(row) for row in maze]


width, height = 15, 15
maze = generate_maze(width, height)
print_maze(maze)

maze_strings = maze_to_string(maze)
print(maze_strings)
