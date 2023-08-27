import pygame

class Ship:
    """Класс управления кораблём"""

    def __init__(self, ai_game):
        """Инициализирует корабли и задает его начальную позиция"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Загружает изображение корабля и получает прямоугольник
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Каждый новый корабль появляется у нижнего края экрана
        self.rect.midbottom = self.screen_rect.midbottom

        # Флаги перемещения
        # При перемещении True, в неподвижном состоянии False
        self.moving_right = False
        self.moving_left = False


    def update(self):
        """Обновляет позицию корабля с учетом флага"""
        if self.moving_right:
            self.rect.x += 1
        if self.moving_left:
            self.rect.x -= 1

    def blitne(self):
        """Рисует корабль в текущей позиции"""
        self.screen.blit(self.image, self.rect)
