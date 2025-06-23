import pygame
import sys

# Инициализация Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Симуляция движения по коридору")
clock = pygame.time.Clock()

# Игрок
player_x, player_y = 0, 0
player_dir = 0  # 0 = вверх, 90 = вправо, 180 = вниз, 270 = влево

# Глубина
depth = 6

# Цвета
WALL_COLOR = (120, 120, 200)
FLOOR_COLOR = (40, 40, 40)
CEIL_COLOR = (25, 25, 45)
OBJECT_COLOR = (200, 80, 80)

# Объекты
objects = {
    (0, 3): {"color": (255, 100, 100), "active": True},
    (1, 4): {"color": (100, 255, 100), "active": True},
}

def move_forward():
    global player_x, player_y
    if player_dir == 0:
        player_y += 1
    elif player_dir == 90:
        player_x += 1
    elif player_dir == 180:
        player_y -= 1
    elif player_dir == 270:
        player_x -= 1

def move_backward():
    global player_x, player_y
    if player_dir == 0:
        player_y -= 1
    elif player_dir == 90:
        player_x -= 1
    elif player_dir == 180:
        player_y += 1
    elif player_dir == 270:
        player_x += 1

def get_relative_coords(obj_x, obj_y):
    dx = obj_x - player_x
    dy = obj_y - player_y
    if player_dir == 0:
        return dx, dy
    elif player_dir == 90:
        return -dy, dx
    elif player_dir == 180:
        return -dx, -dy
    elif player_dir == 270:
        return dy, -dx

def draw_corridor():
    for i in range(depth):
        z = i + 1
        scale = 1 / z
        width = int(WIDTH * 0.8 * scale)
        height = int(HEIGHT * 0.8 * scale)
        x = WIDTH // 2 - width // 2
        y = HEIGHT // 2 - height // 2

        # Потолок
        pygame.draw.polygon(screen, CEIL_COLOR, [
            (x, y),
            (x + width, y),
            (WIDTH // 2 + WIDTH // 4, 0),
            (WIDTH // 2 - WIDTH // 4, 0)
        ])

        # Пол
        pygame.draw.polygon(screen, FLOOR_COLOR, [
            (x, y + height),
            (x + width, y + height),
            (WIDTH // 2 + WIDTH // 4, HEIGHT),
            (WIDTH // 2 - WIDTH // 4, HEIGHT)
        ])

        # Стены
        pygame.draw.rect(screen, WALL_COLOR, (x, y, width, height), 2)

def draw_objects():
    for (x, y), obj in objects.items():
        rel_x, rel_y = get_relative_coords(x, y)
        if rel_y <= 0 or rel_y > depth:
            continue
        scale = 1 / rel_y
        size = int(100 * scale)
        offset_x = int(rel_x * 120 * scale)
        pos_x = WIDTH // 2 + offset_x - size // 2
        pos_y = HEIGHT // 2 + int(100 * scale) - size
        pygame.draw.ellipse(screen, obj["color"], (pos_x, pos_y, size, size * 1.3))

def update_objects():
    for key in objects:
        if pygame.time.get_ticks() % 2000 < 100:
            objects[key]["active"] = not objects[key]["active"]

# Основной цикл
running = True
while running:
    screen.fill((0, 0, 0))

    # События
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
    elif keys[pygame.K_UP]:
        move_forward()
        pygame.time.wait(150)
    elif keys[pygame.K_DOWN]:
        move_backward()
        pygame.time.wait(150)
    elif keys[pygame.K_LEFT]:
        player_dir = (player_dir - 90) % 360
        pygame.time.wait(150)
    elif keys[pygame.K_RIGHT]:
        player_dir = (player_dir + 90) % 360
        pygame.time.wait(150)

    # Отрисовка
    update_objects()
    draw_corridor()
    draw_objects()
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
