import sys
import pygame
from settings import Settings
from ship import Ship


class AlienInvasion:
    """Класс для управления ресурсами и поведение игры"""

    def __init__(self):
        """Инициализируем игру и создает игровые ресурсы"""
        pygame.init()
        self.settings = Settings()  # создаем экзепляр класса Settings

        #  Создаем окно (поверхность), в котором прорисавываются все графические элементы игры.
        #  При создании экрана используются атрибуты screen_width и screen_height объекта self.settings
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        #  Назначение цвета фона
        self.bg_color = (230, 230, 230)

        self.ship = Ship(self)

    def run_game(self):
        """Запуск основного цикла игры"""
        while True:
            self._check_events()  # вспомогательный метод
            self._update_screen()  # вспомогательный метод


    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран"""
        #  При каждом проходе цикла перерисовывается экран
        #  Для получения цвета фона при заполнении экрана используется объект self.settings
        self.screen.fill(self.settings.bg_color)

        self.ship.blitne()

        #  Отображение последнего прорисованного экрана
        pygame.display.flip()


if __name__ == '__main__':
    #  Создание экземпляра и запуск игры
    ai = AlienInvasion()
    ai.run_game()