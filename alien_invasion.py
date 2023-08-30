import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet


class AlienInvasion:
    """Класс для управления ресурсами и поведение игры"""

    def __init__(self):
        """Инициализируем игру и создает игровые ресурсы"""
        pygame.init()
        self.settings = Settings()  # создаем экзепляр класса Settings

        #  Создаем окно (поверхность), в котором прорисавываются все графические элементы игры.
        #  При создании экрана используются FULLSCREEN, вычисляющий размер окна
        #  атрибуты screen_width и screen_height используются для обновления объекта self.settings
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        #  Назначение цвета фона
        self.bg_color = (230, 230, 230)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()


    def run_game(self):
        """Запуск основного цикла игры"""
        while True:
            self._check_events()  # вспомогательный метод

            # позиция корабля будет обновляться после проверки событий клавиатуры,
            # но перед обновление экрана
            self.ship.update()

            # вспомогательные методы
            self._update_bullets()
            self._update_screen()


    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)


    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиши"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()

    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавиши"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key - - pygame.K_LEFT:
            self.ship.moving_left = False


    def fire_bullet(self):
        """Создание нового снаряяда и включение его в группу bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды"""
        self.bullets.update()  # позиция снаряда будет обновляться при каждом проходе цикла

        # удаление снарядов, вышедших за край экрана
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)


    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран"""
        #  При каждом проходе цикла перерисовывается экран
        #  Для получения цвета фона при заполнении экрана используется объект self.settings
        self.screen.fill(self.settings.bg_color)

        self.ship.blitne()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        #  Отображение последнего прорисованного экрана
        pygame.display.flip()


if __name__ == '__main__':
    #  Создание экземпляра и запуск игры
    ai = AlienInvasion()
    ai.run_game()
