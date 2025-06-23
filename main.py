import pygame
import os

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Симуляция движения по коридору")

# Параметры движения
pos_x, pos_y = 0, 0  # Координаты пользователя
view_angle = 0       # Угол обзора (0-360)
STEP = 1             # Шаг по координатам (в логической системе, не пикселях)
ANGLE_STEP = 45      # Шаг поворота

# Загрузка изображений в словарь
image_db = {}
image_folder = "images"

# Предполагаем, что у нас есть изображения для точки (0,0) под всеми углами
angles_list = [0, 45, 90, 135, 180, 225, 270, 315]

for ang in angles_list:
    filename = f"{pos_x}_{pos_y}_{ang}.jpg"
    path = os.path.join(image_folder, filename)
    if os.path.exists(path):
        image_db[(pos_x, pos_y, ang)] = pygame.image.load(path)
    else:
        print(f"[!] Не найдено изображение: {filename}")

# Функция для обновления изображения
def update_scene():
    key = (pos_x, pos_y, view_angle)
    if key in image_db:
        win.blit(pygame.transform.scale(image_db[key], (WIDTH, HEIGHT)), (0, 0))
    else:
        win.fill((0, 0, 0))
        print(f"[!] Нет изображения для: {key}")
    pygame.display.update()

# Основной цикл
run = True
update_scene()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        run = False

    moved = False

    if keys[pygame.K_LEFT]:
        view_angle = (view_angle - ANGLE_STEP) % 360
        moved = True
        pygame.time.wait(150)

    if keys[pygame.K_RIGHT]:
        view_angle = (view_angle + ANGLE_STEP) % 360
        moved = True
        pygame.time.wait(150)

    if keys[pygame.K_UP]:
        if view_angle == 0:
            pos_y -= STEP
        elif view_angle == 90:
            pos_x += STEP
        elif view_angle == 180:
            pos_y += STEP
        elif view_angle == 270:
            pos_x -= STEP
        moved = True
        pygame.time.wait(150)

    if keys[pygame.K_DOWN]:
        if view_angle == 0:
            pos_y += STEP
        elif view_angle == 90:
            pos_x -= STEP
        elif view_angle == 180:
            pos_y -= STEP
        elif view_angle == 270:
            pos_x += STEP
        moved = True
        pygame.time.wait(150)

    if moved:
        update_scene()

pygame.quit()
