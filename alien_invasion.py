import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


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
        self.aliens = pygame.sprite.Group()

        self._create_fleet()  # вспомогательный метод для создания флота

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
            self._update_aliens()

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
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self.fire_bullet()

    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавиши"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

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
            if (bullet.rect.bottom <= 0) \
                    or (bullet.rect.left >= self.ship.screen_rect.right) \
                    or (bullet.rect.right <= 0):
                self.bullets.remove(bullet)

    def _update_aliens(self):
        """Проверяет, достиг ли флот края экрана,
            с последиющим обновлением позиций всех пришельцев во флоте"""
        self._check_fleet_edges()
        self.aliens.update()

    def _create_fleet(self):
        """Создание флота вторжения"""
        alien = Alien(self)  # создание пришельца, он не войдет во флот и не включается в группу aliens
        alien_width, alien_height = alien.rect.size  # size содержит кортеж с шириной и высотой объекта rect

        # Вычисляется доступное горизонтальное пространство и количество пришельцев, которые в нем поместятся.
        # Интервал между соседними пришельцами равен ширине пришельца.
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)  # количество пришельцев в ряду

        # Определяет количество рядов, помещающихся на экране.
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        number_rows = available_space_y // (2 * alien_height)

        # Создание флота
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Создание пришельца и размещение его в ряду"""
        alien = Alien(self)  # создается новый пришелец
        alien_width, alien_height = alien.rect.size

        # Пришелец сдвигается вправо на одну ширину от левого края поля.
        # 2 * alien_width - полное пространство выделенное на одного пришельца (две ширины пришельца)
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x

        # Прибавляется одна высота пришельца, чтобы создать пустое место у вехнего края экрана.
        # Каждый новый ряд начинается на две высоты ниже последнего ряда - 2 * alien.rect.height
        # Номер первого ряда равен 0
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)  # новый пришелец добавляется в группу

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление флота"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран"""
        #  При каждом проходе цикла перерисовывается экран
        #  Для получения цвета фона при заполнении экрана используется объект self.settings
        self.screen.fill(self.settings.bg_color)

        self.ship.blitne()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)  # вызов метода draw для появления пришельца на экране

        #  Отображение последнего прорисованного экрана
        pygame.display.flip()


if __name__ == '__main__':
    #  Создание экземпляра и запуск игры
    ai = AlienInvasion()
    ai.run_game()
