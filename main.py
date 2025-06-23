import pygame
import sys
import math

# Настройки окна
WIDTH, HEIGHT = 1000, 500
FPS = 60
dt = 1 / FPS

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Динамика тележек: столкновение с трением и вращением")
clock = pygame.time.Clock()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
BLUE = (30, 144, 255)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)


class Cart:
    def __init__(self, x, y, mass, velocity, mu, color, image=None):
        self.x = x
        self.y = y
        self.mass = mass
        self.vx = velocity
        self.mu = mu  # Коэффициент трения
        self.color = color
        self.width = 60
        self.height = 40
        self.angle = 0  # угол поворота в радианах
        self.omega = 0  # угловая скорость
        self.I = 0.1 * self.mass * (self.width / 100) ** 2  # момент инерции (примерно)
        self.image = image
        if image:
            self.img = pygame.image.load(image)
            self.img = pygame.transform.scale(self.img, (self.width, self.height))
        else:
            self.img = None

    def apply_friction(self):
        friction_force = self.mu * self.mass * 9.8
        deceleration = friction_force / self.mass
        if self.vx > 0:
            self.vx -= deceleration * dt * 100
            if self.vx < 0:
                self.vx = 0
        elif self.vx < 0:
            self.vx += deceleration * dt * 100
            if self.vx > 0:
                self.vx = 0

    def apply_rot_friction(self):
        torque_friction = 0.05 * self.omega
        alpha = -torque_friction / self.I
        self.omega += alpha * dt

    def update(self):
        self.x += self.vx * dt
        self.angle += self.omega * dt

        self.apply_friction()
        self.apply_rot_friction()

        # Ограничение по экрану
        if self.x < 0:
            self.x = 0
            self.vx = 0
        elif self.x > WIDTH - self.width:
            self.x = WIDTH - self.width
            self.vx = 0

    def draw(self, surface):
        if self.img:
            rotated_image = pygame.transform.rotate(self.img, -math.degrees(self.angle))
            rect = rotated_image.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
            surface.blit(rotated_image, rect.topleft)
        else:
            # Рисуем прямоугольник с поворотом
            surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            surf.fill(self.color)
            rotated = pygame.transform.rotate(surf, -math.degrees(self.angle))
            rect = rotated.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
            surface.blit(rotated, rect.topleft)

        # Вектор скорости
        vx_end = self.x + self.width / 2 + self.vx / 3
        vy_end = self.y + self.height / 2
        pygame.draw.line(surface, GREEN, (self.x + self.width / 2, self.y + self.height / 2), (vx_end, vy_end), 3)


def collision(cart1, cart2, e):
    # Проверяем столкновение по оси X (простая коллизия)
    if cart1.x + cart1.width >= cart2.x and cart1.x < cart2.x + cart2.width:
        # Рассчёт новых скоростей по закону сохранения импульса с коэффициентом восстановления
        v1_new = ((cart1.mass - e * cart2.mass) * cart1.vx + (1 + e) * cart2.mass * cart2.vx) / (
                    cart1.mass + cart2.mass)
        v2_new = ((cart2.mass - e * cart1.mass) * cart2.vx + (1 + e) * cart1.mass * cart1.vx) / (
                    cart1.mass + cart2.mass)

        # Обновляем скорости
        cart1.vx = v1_new
        cart2.vx = v2_new

        # Вращение при столкновении
        relative_velocity = abs(cart1.vx - cart2.vx)
        torque1 = 0.02 * relative_velocity * cart2.mass
        torque2 = 0.02 * relative_velocity * cart1.mass

        cart1.omega += torque1 / cart1.I
        cart2.omega += torque2 / cart2.I

        # Смещаем тележки, чтобы не залипали
        overlap = (cart1.x + cart1.width) - cart2.x
        cart1.x -= overlap / 2
        cart2.x += overlap / 2


def create_carts():
    # Функция для создания начальных тележек (для перезапуска)
    return (
        Cart(x=200, y=HEIGHT // 2, mass=2.0, velocity=200, mu=0.02, color=RED, image='cart1.png'),
        Cart(x=700, y=HEIGHT // 2, mass=1.5, velocity=-150, mu=0.03, color=BLUE, image='cart2.png')
    )


def draw_button(surface, rect, text, font, active=True):
    color = DARK_GRAY if active else GRAY
    pygame.draw.rect(surface, color, rect)
    txt_surf = font.render(text, True, WHITE if active else DARK_GRAY)
    txt_rect = txt_surf.get_rect(center=rect.center)
    surface.blit(txt_surf, txt_rect)


# Инициализация
cart1, cart2 = create_carts()
e = 0.7  # Коэффициент восстановления

font = pygame.font.SysFont('timesnewroman', 18)

# Кнопка "Начать заново"
button_rect = pygame.Rect(WIDTH - 150, 10, 140, 40)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                # Перезапуск — создаём новые тележки
                cart1, cart2 = create_carts()

    screen.fill(WHITE)

    # Обновление тележек
    cart1.update()
    cart2.update()

    # Проверка столкновения
    collision(cart1, cart2, e)

    # Отрисовка тележек
    cart1.draw(screen)
    cart2.draw(screen)

    # Текст с параметрами
    text1 = font.render(f'Cart1: v={cart1.vx:.1f} px/s, ω={cart1.omega:.2f} rad/s', True, BLACK)
    text2 = font.render(f'Cart2: v={cart2.vx:.1f} px/s, ω={cart2.omega:.2f} rad/s', True, BLACK)
    screen.blit(text1, (10, 10))
    screen.blit(text2, (10, 30))

    # Отрисовка кнопки
    draw_button(screen, button_rect, "Начать заново", font)

    pygame.display.flip()
    clock.tick(FPS)
