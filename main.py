import pygame
import math
import random
from car import Car

pygame.init()

# Параметры экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Гоночная игра")

# Цвета
GREEN = (0, 150, 0)  # Задний фон
ROAD_COLOR = (100, 100, 100)  # Цвет дороги
BARRIER_COLOR = (255, 0, 0)  # Препятствия
WHITE = (255, 255, 255)  # Текст
BUTTON_COLOR = (50, 50, 50)  # Кнопка
BUTTON_HOVER_COLOR = (80, 80, 80)  # Кнопка при наведении

# Параметры дороги
road_x = WIDTH // 4
road_width = WIDTH // 2
scroll_speed = 3  # Скорость движения дороги


# Функция генерации препятствий
def generate_barrier():
    barrier_width = random.randint(50, 80)
    barrier_x = random.randint(road_x + 10, road_x + road_width - barrier_width - 10)
    barrier_y = -50  # Препятствие появляется сверху
    barriers.append((barrier_x, barrier_y, barrier_width, 40))


# Функция отрисовки дороги
def draw_road():
    pygame.draw.rect(screen, ROAD_COLOR, (road_x, 0, road_width, HEIGHT))  # Дорога
    pygame.draw.rect(screen, BARRIER_COLOR, (road_x - 10, 0, 10, HEIGHT))  # Левая граница
    pygame.draw.rect(screen, BARRIER_COLOR, (road_x + road_width, 0, 10, HEIGHT))  # Правая граница


# Функция отрисовки препятствий
def draw_barriers():
    for barrier in barriers:
        pygame.draw.rect(screen, BARRIER_COLOR, barrier)


# Функция, ограничивающая движение машины в пределах дороги
def constrain_movement():
    if car.x - 20 < road_x:
        car.x = road_x + 20
    if car.x + 20 > road_x + road_width:
        car.x = road_x + road_width - 20


# Функция проверки столкновения машины с препятствиями
def check_collision():
    car_rect = pygame.Rect(car.x - 20, car.y - 40, 40, 80)
    for barrier in barriers:
        barrier_rect = pygame.Rect(barrier)
        if car_rect.colliderect(barrier_rect):
            return True
    return False


# Функция отображения сообщения о проигрыше
def display_message(message):
    font = pygame.font.Font(None, 74)
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(text, text_rect)


# Функция отрисовки кнопки "Начать заново"
def draw_button():
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    mouse_pos = pygame.mouse.get_pos()

    if button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)

    font = pygame.font.Font(None, 40)
    text = font.render("Начать заново", True, WHITE)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

    return button_rect


# Функция сброса игры
def reset_game():
    global car, barriers, frame_counter, game_over
    car = Car(WIDTH // 2, HEIGHT - 120, "assets/car.png")
    barriers = []
    frame_counter = 0
    game_over = False


# Основные переменные
running = True
game_over = False
frame_counter = 0
car = Car(WIDTH // 2, HEIGHT - 120, "assets/car.png")
barriers = []
clock = pygame.time.Clock()

# Главный игровой цикл
while running:
    screen.fill(GREEN)  # Фон
    draw_road()  # Отрисовка дороги
    draw_barriers()  # Отрисовка препятствий

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if restart_button.collidepoint(event.pos):
                reset_game()

    # Основная логика игры
    if not game_over:
        keys = pygame.key.get_pressed()
        car.update(keys)  # Обновление состояния машины
        constrain_movement()  # Ограничение выхода за границы

        # Движение препятствий вниз при движении машины вперед
        if car.speed > 0:
            for i in range(len(barriers)):
                x, y, w, h = barriers[i]
                barriers[i] = (x, y + scroll_speed, w, h)

            barriers = [b for b in barriers if b[1] < HEIGHT]

            if frame_counter % 60 == 0:
                generate_barrier()

        # Проверка столкновений
        if car.speed > 0 and check_collision():
            game_over = True

        car.draw(screen)
        frame_counter += 1

    else:
        display_message("Вы проиграли!")
        restart_button = draw_button()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
