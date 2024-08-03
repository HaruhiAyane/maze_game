import pygame
import sys
import time

# Pygameの初期化
pygame.init()

# 画面の設定
cell_size = 40
cols, rows = 11, 11
screen = pygame.display.set_mode((cols * cell_size, rows * cell_size))
pygame.display.set_caption("WASD to Move Character in Maze")

# キャラクターの設定
character_sprite = pygame.image.load("character.png").convert_alpha()
character_sprite = pygame.transform.scale(character_sprite, (cell_size, cell_size))
goaled_character_sprite = pygame.image.load("goaled_character.png").convert_alpha()
goaled_character_sprite = pygame.transform.scale(goaled_character_sprite, (cell_size, cell_size))
character_rect = character_sprite.get_rect()

# ゴールの設定
goal_sprite = pygame.image.load("goal.png").convert_alpha()
goal_sprite = pygame.transform.scale(goal_sprite, (cell_size, cell_size))

# 迷路の定義
mazes = [
    [
        "###########",
        "#Soo#ooooo#",
        "###o###o###",
        "#o#ooo#ooo#",
        "#o###o###o#",
        "#ooo#ooooo#",
        "#o#######o#",
        "#ooooooo#o#",
        "#o###o###o#",
        "#ooo#ooooG#",
        "###########",
    ],
    [
        "###########",
        "#Soo#ooooo#",
        "###o#o#o#o#",
        "#ooo#o#o#o#",
        "#o###o#o#o#",
        "#o#o#o#o#o#",
        "#o#o#o#o#o#",
        "#o#ooo#o#o#",
        "#o#####o#o#",
        "#ooooooo#G#",
        "###########",
    ],
    [
        "###########",
        "#S#ooooooo#",
        "#o#o#####o#",
        "#ooo#ooooo#",
        "#####o#####",
        "#ooo#o#ooo#",
        "#o###o#o#o#",
        "#ooo#o#o#o#",
        "#o#o#o#o#o#",
        "#o#ooooo#G#",
        "###########",
    ],
    [
        "###########",
        "#Soo#ooooo#",
        "###o###o###",
        "#o#ooo#ooo#",
        "#o###o###o#",
        "#ooo#ooo#o#",
        "#o#o###o#o#",
        "#o#ooooo#o#",
        "#o#######o#",
        "#ooooooooG#",
        "###########",
    ],
    [
        "###########",
        "#S#ooooooo#",
        "#o#####o#o#",
        "#ooooooo#o#",
        "#########o#",
        "#ooo#ooo#o#",
        "###o#o#o#o#",
        "#ooo#o#ooo#",
        "#o###o#####",
        "#ooooooooG#",
        "###########",
    ],
    [
        "###########",
        "#Soooo#ooo#",
        "#####o#o#o#",
        "#ooooo#o#o#",
        "#o#####o#o#",
        "#ooo#ooo#o#",
        "###o#####o#",
        "#ooo#ooooo#",
        "#o###o###o#",
        "#ooooo#ooG#",
        "###########",
    ],
]


# スタート位置とゴール位置を見つける関数
def find_positions(maze):
    start_pos = None
    goal_pos = None
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == "S":
                start_pos = (x, y)
            elif cell == "G":
                goal_pos = (x, y)
    return start_pos, goal_pos


# 現在の迷路を設定
current_maze_index = 0
maze = mazes[current_maze_index]
start_pos, goal_pos = find_positions(maze)
character_rect.topleft = (start_pos[0] * cell_size, start_pos[1] * cell_size)

# 速度設定
speed = cell_size

# 通った場所のリスト
visited = set()
visited.add((start_pos[0], start_pos[1]))


def draw_maze(show_goal=True):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == "#":
                color = (0, 0, 0)
            else:
                color = (255, 255, 255)
            pygame.draw.rect(screen, color, pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))
    for x, y in visited:
        pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))
    # ゴールの背景
    if show_goal:
        pygame.draw.rect(
            screen, (255, 127, 127), pygame.Rect(goal_pos[0] * cell_size, goal_pos[1] * cell_size, cell_size, cell_size)
        )
        # ゴールの描画
        screen.blit(goal_sprite, (goal_pos[0] * cell_size, goal_pos[1] * cell_size))


def rotate_and_blit(image, rect, angle):
    """画像を回転させて描画する関数"""
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=rect.center)
    screen.blit(rotated_image, new_rect.topleft)


# メインループ
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # キー入力の取得
    keys = pygame.key.get_pressed()
    new_rect = character_rect.copy()
    if keys[pygame.K_w]:
        new_rect.y -= speed
    if keys[pygame.K_a]:
        new_rect.x -= speed
    if keys[pygame.K_s]:
        new_rect.y += speed
    if keys[pygame.K_d]:
        new_rect.x += speed

    # 衝突判定
    if maze[new_rect.y // cell_size][new_rect.x // cell_size] != "#":
        character_rect = new_rect
        visited.add((character_rect.x // cell_size, character_rect.y // cell_size))

    # ゴール判定
    if (character_rect.x // cell_size, character_rect.y // cell_size) == goal_pos:
        # キャラクター位置を更新してからクリア画面表示
        screen.fill((255, 255, 255))  # 背景を白にする
        draw_maze(show_goal=False)  # ゴールを非表示にする
        screen.blit(goaled_character_sprite, character_rect)  # キャラクターを旗を持っている姿に変更
        pygame.display.flip()
        time.sleep(0.1)

        # クリア表示と回転アニメーション
        font = pygame.font.Font(None, 74)
        text = font.render("Clear!", True, (255, 0, 0))
        screen.blit(
            text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() // 2)
        )
        pygame.display.flip()
        for angle in range(0, 1801, 15):  # 15度ごとに回転
            screen.fill((255, 255, 255))  # 背景を白にする
            draw_maze(show_goal=False)  # ゴールを非表示にする
            screen.blit(
                text,
                (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() // 2),
            )
            rotate_and_blit(goaled_character_sprite, to_pixel(character_pos[0], character_pos[1]), angle)
            pygame.display.flip()
            pygame.time.wait(50)  # 回転アニメーションの速度調整

        time.sleep(1)  # Clear画面表示時間を変更

        # 次の迷路に進む
        current_maze_index = (current_maze_index + 1) % len(mazes)
        maze = mazes[current_maze_index]
        start_pos, goal_pos = find_positions(maze)
        character_rect.topleft = (start_pos[0] * cell_size, start_pos[1] * cell_size)
        visited = set()
        visited.add((start_pos[0], start_pos[1]))

    # 画面の描画
    screen.fill((255, 255, 255))  # 背景を白にする
    draw_maze()
    screen.blit(character_sprite, character_rect)
    pygame.display.flip()

    # フレームレートを設定
    pygame.time.Clock().tick(30)
