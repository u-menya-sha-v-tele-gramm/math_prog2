import pygame
import math


class Car:
    def __init__(self, x, y, image_path):
        # Загружаем изображение с прозрачностью
        self.original_image = pygame.image.load(image_path).convert_alpha()

        # Изменяем размер машины (40x80)
        self.original_image = pygame.transform.scale(self.original_image, (40, 80))

        # Поворачиваем на -90 градусов (чтобы машина смотрела вверх)
        self.original_image = pygame.transform.rotate(self.original_image, 0)

        self.image = self.original_image  # Копия для работы
        self.rect = self.image.get_rect(center=(x, y))  # Хитбокс
        self.x, self.y = x, y
        self.angle = 0
        self.speed = 0
        self.max_speed = 5
        self.acceleration = 0.1
        self.friction = 0.05
        self.turn_speed = 3

    def update(self, keys):
        # Управление скоростью
        if keys[pygame.K_UP]:
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        if keys[pygame.K_DOWN]:
            self.speed = max(self.speed - self.acceleration, -self.max_speed / 2)

        # Повороты (если машина двигается)
        if self.speed != 0:
            if keys[pygame.K_LEFT]:
                self.angle -= self.turn_speed * (self.speed / self.max_speed)
            if keys[pygame.K_RIGHT]:
                self.angle += self.turn_speed * (self.speed / self.max_speed)

        # Применение трения
        if self.speed > 0:
            self.speed = max(self.speed - self.friction, 0)
        elif self.speed < 0:
            self.speed = min(self.speed + self.friction, 0)

        # Обновление позиции
        self.x += self.speed * math.sin(math.radians(self.angle))
        self.y -= self.speed * math.cos(math.radians(self.angle))

        # Поворот изображения
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=(self.x, self.y))  # Центрируем после поворота

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
