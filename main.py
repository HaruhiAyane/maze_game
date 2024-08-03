import pygame
import sys
import time

# Pygameの初期化
pygame.init()

# 画面の設定
wide_size = 40
narrow_size = 10
# 壁も含んだ maze の長さ
cols, rows = 15, 15
widecols = cols // 2
narrowcols = (cols + 1) // 2
widerows = cols // 2
narrowrows = (cols + 1) // 2
screen = pygame.display.set_mode(
    (widecols * wide_size + narrow_size * narrowcols, widerows * wide_size + narrowrows * narrow_size)
)
pygame.display.set_caption("WASD to Move Character in Maze")

# キャラクターの設定
character_sprite = pygame.image.load("character.png").convert_alpha()
character_sprite = pygame.transform.scale(character_sprite, (wide_size, wide_size))
goaled_character_sprite = pygame.image.load("goaled_character.png").convert_alpha()
goaled_character_sprite = pygame.transform.scale(goaled_character_sprite, (wide_size, wide_size))
character_rect = character_sprite.get_rect()

# ゴールの設定
goal_sprite = pygame.image.load("goal.png").convert_alpha()
goal_sprite = pygame.transform.scale(goal_sprite, (wide_size, wide_size))

# 迷路の定義
mazes = [
    [
        "###############",
        "#Soooooooo#ooo#",
        "#########o#o#o#",
        "#ooo#ooo#o#o#o#",
        "#o#o#o#o#o###o#",
        "#o#ooo#o#ooo#o#",
        "#o#####o###o#o#",
        "#ooooo#ooo#ooo#",
        "#####o#######o#",
        "#ooooo#ooooo#o#",
        "#o#####o###o#o#",
        "#o#ooo#o#o#o#o#",
        "#o#o#o#o#o#o#o#",
        "#ooo#ooooo#ooG#",
        "###############",
    ],
    [
        "###############",
        "#Soooo#ooooooo#",
        "#####o#o#####o#",
        "#ooo#ooo#ooo#o#",
        "#o#######o#o#o#",
        "#ooooo#ooo#ooo#",
        "###o#o#o#######",
        "#ooo#o#ooo#ooo#",
        "#o#o#####o#o#o#",
        "#o#o#ooooo#o#o#",
        "#o###o#####o#o#",
        "#ooo#ooo#ooo#o#",
        "#o#o###o###o#o#",
        "#o#ooooooooo#G#",
        "###############",
    ],
    [
        "###############",
        "#S#o#ooo#ooooo#",
        "#o#o#o#o#o###o#",
        "#o#ooo#o#o#ooo#",
        "#o#####o#o#o#o#",
        "#ooooo#ooo#o#o#",
        "#####o#o###o###",
        "#ooo#o#ooo#ooo#",
        "###o#o###o###o#",
        "#ooo#ooo#o#ooo#",
        "#o#o###o###o#o#",
        "#o#ooo#ooooo#o#",
        "#o###########o#",
        "#ooooooooooooG#",
        "###############",
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


# ピクセル位置に変換する関数
def to_pixel(x, y):
    widex = x // 2
    narrowx = (x + 1) // 2
    widey = y // 2
    narrowy = (y + 1) // 2
    return widex * wide_size + narrowx * narrow_size, widey * wide_size + narrowy * narrow_size


# 現在の迷路を設定
current_maze_index = 0
maze = mazes[current_maze_index]
start_pos, goal_pos = find_positions(maze)
character_pos = start_pos

# 通った場所のリスト
visited = set()
visited.add(start_pos)


def draw_maze(show_goal=True):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            pixel_x, pixel_y = to_pixel(x, y)
            pixel_x1, pixel_y1 = to_pixel(x + 1, y + 1)
            if cell == "#":
                color = (0, 0, 0)
            else:
                color = (255, 255, 255)
            pygame.draw.rect(screen, color, pygame.Rect(pixel_x, pixel_y, pixel_x1 - pixel_x, pixel_y1 - pixel_y))
    for x, y in visited:
        pixel_x, pixel_y = to_pixel(x, y)
        pixel_x1, pixel_y1 = to_pixel(x + 1, y + 1)
        pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(pixel_x, pixel_y, pixel_x1 - pixel_x, pixel_y1 - pixel_y))
    # ゴールの背景
    if show_goal:
        pixel_x, pixel_y = to_pixel(goal_pos[0], goal_pos[1])
        pixel_x1, pixel_y1 = to_pixel(goal_pos[0] + 1, goal_pos[1] + 1)
        pygame.draw.rect(screen, (255, 127, 127), pygame.Rect(pixel_x, pixel_y, pixel_x1 - pixel_x, pixel_y1 - pixel_y))
        # ゴールの描画
        screen.blit(goal_sprite, (pixel_x, pixel_y))


def rotate_and_blit(image, pos, angle):
    """画像を回転させて描画する関数"""
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=(pos[0] + wide_size // 2, pos[1] + wide_size // 2))
    screen.blit(rotated_image, new_rect.topleft)


# メインループ
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # キー入力の取得
    keys = pygame.key.get_pressed()
    new_pos = list(character_pos)
    via_pos = list(character_pos)
    if keys[pygame.K_w]:
        new_pos[1] -= 2
        via_pos[1] -= 1
    if keys[pygame.K_a]:
        new_pos[0] -= 2
        via_pos[0] -= 1
    if keys[pygame.K_s]:
        new_pos[1] += 2
        via_pos[1] += 1
    if keys[pygame.K_d]:
        new_pos[0] += 2
        via_pos[0] += 1

    # 衝突判定
    if 0 <= new_pos[0] < cols and 0 <= new_pos[1] < rows and 0 <= via_pos[0] < cols and 0 <= via_pos[1] < rows:
        if maze[new_pos[1]][new_pos[0]] != "#" and maze[via_pos[1]][via_pos[0]] != "#":
            character_pos = tuple(new_pos)
            visited_pos = tuple(via_pos)
            visited.add(character_pos)
            visited.add(visited_pos)

    # ゴール判定
    if character_pos == goal_pos:
        # キャラクター位置を更新してからクリア画面表示
        screen.fill((255, 255, 255))  # 背景を白にする
        draw_maze(show_goal=False)  # ゴールを非表示にする
        screen.blit(
            goaled_character_sprite, to_pixel(character_pos[0], character_pos[1])
        )  # キャラクターを旗を持っている姿に変更
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
        character_pos = start_pos
        visited = set()
        visited.add(start_pos)

    # 画面の描画
    screen.fill((255, 255, 255))  # 背景を白にする
    draw_maze()
    screen.blit(character_sprite, to_pixel(character_pos[0], character_pos[1]))
    pygame.display.flip()

    # フレームレートを設定
    pygame.time.Clock().tick(30)
