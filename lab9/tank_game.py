from math import cos, sin, atan
from random import randint
import pygame
from pygame.draw import *
from pygame.font import *
import numpy as np
from screeninfo import get_monitors
from copy import deepcopy

'''
Ввод основных цветов'''
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN, WHITE]

m_color = (39, 115, 38)
s_color = (34, 71, 34)
sd_color = (14, 51, 14)
t_color = (100, 100, 100)
tb_color = (30, 30, 30)


def distance(a, b):
    '''
    Рассчитывает расстояние между двумя точками на плокости
    :param a: итерабольный объект с координатами первой точки
    :param b: итерабольный объект с координатами второй точки
    :return: Искомое расстояние
    '''
    x = (a[0] - b[0]) ** 2
    y = (a[1] - b[1]) ** 2
    if x > 10000000 or y > 10000000:
        return 0
    return (abs(x) + abs(y)) ** 0.5


def get_res():
    """
    Получает разрешение вашего монитора
    Возвращает кортеж с разрешением,
    выводит параметры вашего монитора на экран
    """
    monitor = str(get_monitors()[0])[8:-1].split(', ')
    current_resolution = (int(monitor[2][6:]), int(monitor[3][7:]))
    print('Your screen resolution is', current_resolution[0], 'x', current_resolution[1])
    return current_resolution


class Mouse:
    def __init__(self):
        '''
        Описывает параметры объекта класса "Mouse"
        '''
        self.pos = (0, 0)  # Позиция мыши, tuple

    def position_upd(self, eventing):
        '''
        Отвечает за обновление координат мыши у объекта
        :param eventing: Используется в основном коде как описание ивента-триггера
        :return: nothing
        '''
        self.pos = eventing.pos

    def draw(self, current_screen):
        '''
        Отвечает за рисование курсора в виде прицела на экране
        :param current_screen: текущий экран
        :return:
        '''
        circle(current_screen, RED, self.pos, 3)
        line(current_screen, BLACK, [self.pos[0] + 10, self.pos[1]], [self.pos[0] + 20, self.pos[1]])
        line(current_screen, BLACK, [self.pos[0] - 10, self.pos[1]], [self.pos[0] - 20, self.pos[1]])
        line(current_screen, BLACK, [self.pos[0], self.pos[1] + 10], [self.pos[0], self.pos[1] + 20])
        line(current_screen, BLACK, [self.pos[0], self.pos[1] - 10], [self.pos[0], self.pos[1] - 20])


class Tank:
    def __init__(self, current_screen):
        '''
        Задаёт основные параметры объектов
        :param current_screen: текущий экран для рисования
        '''
        self.pos = [res[0] // 2, res[1] - 60]  # Позиция танка, любой итерируемый объект
        self.hp = 3  # Начальное количество здоровья танка
        self.power_shoot = 0  # Начальная сила заряда орудия
        self.size = 1  # Множитель размера танка
        self.gun_angle = 0  # Угол наклона орудия танка, отсчитывается от положительного направления оси Х в градусах
        self.body_angle = 0  # Угол наклона корпуса танка, отсчитывается от положительного направления оси Х в градусах
        self.track_pos = 0  # UNRELEASED Текущее положение ходовой танка
        self.scr = current_screen  # Текущий экран
        self.gun_pos = (0, 0)  # итерируемый объект с координатами кончика орудия
        self.speed = 0  # Скорость танка по оси Х
        self.load = 100  # Состояние процесса зарядка орудия

    def draw(self):
        '''
        Рисует любой объект данного класса
        :return: nothing
        '''
        ang = self.gun_angle / 57.3
        anb = self.body_angle / 57.3

        def body(c_scr, coord, ts, an_body):
            '''
            Рисует корпус танка
            :param c_scr: Текущий экран
            :param coord: итерируемый объект с координатами центра верхней части корпуса
            :param ts: Коэффицент увеличения танка
            :param an_body: Угол наклона корпуса танка
            :return: nothing
            '''
            an_body += 1
            cx = coord[0]
            cy = coord[1]
            coord_main_up = np.array([[100, 0],
                                      [120, 15],
                                      [-120, 15],
                                      [-120, 0]])
            coord_main_down = np.array([[120, 15],
                                        [90, 40],
                                        [-90, 40],
                                        [-120, 25],
                                        [-120, 15]])
            coord_tower_down = np.array([[70, 0],
                                         [50, -10],
                                         [-50, -10],
                                         [-70, 0]])
            coord_tower_up = np.array([[20, -10], [10, -60],
                                       [-10, -60],
                                       [-20, -10]])
            coord_mudguard = np.array([[-135, 20],
                                       [-125, 15],
                                       [120, 15],
                                       [130, 20]])
            coord_shar = np.array([0, -50])

            otn_arr1 = np.array([cx, cy])
            otn_arr4 = np.array([[cx, cy] * 4]).reshape(4, 2)
            otn_arr5 = np.array([[cx, cy] * 5]).reshape(5, 2)

            coord_main_up_it = (coord_main_up * ts + otn_arr4).astype(int)
            coord_main_down_it = (coord_main_down * ts + otn_arr5).astype(int)
            coord_tower_down_it = (coord_tower_down * ts + otn_arr4).astype(int)
            coord_tower_up_it = (coord_tower_up * ts + otn_arr4).astype(int)
            coord_shar_it = (coord_shar * ts + otn_arr1).astype(int)
            coord_mudguard_it = (coord_mudguard * ts + otn_arr4).astype(int)

            aalines(c_scr, s_color, True, coord_main_up_it)
            aalines(c_scr, sd_color, True, coord_main_down_it)
            aalines(c_scr, t_color, True, coord_tower_down_it)
            aalines(c_scr, s_color, True, coord_tower_up_it)

            polygon(c_scr, s_color, coord_main_up_it)
            polygon(c_scr, sd_color, coord_main_down_it)
            polygon(c_scr, t_color, coord_tower_down_it)
            polygon(c_scr, s_color, coord_tower_up_it)

            circle(c_scr, t_color, coord_shar_it, int(5 * ts))

            lines(c_scr, tb_color, False, coord_mudguard_it, int(4 * ts))

        def gun(c_scr, coord, ts, an, power_shoot):
            '''
            Отвечает за рисовку самой пушки танка и рассчёт её координат после поворота
            :param c_scr: Текущий экран
            :param coord: итерируемый объект с координатами центра верхней части корпуса
            :param ts: Коэффицент увеличения танка
            :param an: Угол поворота пушки, отсчитывается от горизонтальной оси против часовой стрелки
            :param power_shoot: Мощность выстрела
            :return: np.array 1х2 с координатами конца орудия
            '''
            cx = coord[0]
            cy = coord[1]
            otn_arr2 = np.array([[cx, cy] * 2]).reshape(2, 2)
            otn_arr4 = np.array([[cx, cy] * 4]).reshape(4, 2)

            gun_l_b = 20
            gun_l_mi = 70
            gun_l_ma = 150
            gun_r = 5

            gun_l = gun_l_mi + (gun_l_ma - gun_l_mi) * power_shoot / 100
            coord_shar = np.array([0, -50])
            otn_coord_shar = np.array([coord_shar] * 4).reshape(4, 2)
            otn_coord_shar2 = np.array([coord_shar] * 2).reshape(2, 2)

            coord_gun = np.array([[-gun_l_b * cos(an) + gun_r * sin(an), gun_l_b * sin(an) + gun_r * cos(an)],
                                  [-gun_l_b * cos(an) - gun_r * sin(an), gun_l_b * sin(an) - gun_r * cos(an)],
                                  [gun_l * cos(an) - gun_r * sin(an), -gun_l * sin(an) - gun_r * cos(an)],
                                  [gun_l * cos(an) + gun_r * sin(an), -gun_l * sin(an) + gun_r * cos(an)]])
            coord_rel = np.array([[-gun_l_b * cos(an) + gun_r * sin(an), gun_l_b * sin(an) + gun_r * 1.4 * cos(an)],
                                  [-gun_l_b * cos(an) - gun_r * sin(an), gun_l_b * sin(an) - gun_r * 1.4 * cos(an)],
                                  [-2 * gun_l_b * cos(an) - gun_r * sin(an),
                                   2 * gun_l_b * sin(an) - gun_r * 1.4 * cos(an)],
                                  [-2 * gun_l_b * cos(an) + gun_r * sin(an),
                                   2 * gun_l_b * sin(an) + gun_r * 1.4 * cos(an)]])
            coord_gun_start_bul = np.array([[gun_l * cos(an), -gun_l * sin(an)],
                                            [gun_l * cos(an), -gun_l * sin(an)]])

            coord_gun_it = ((coord_gun + otn_coord_shar) * ts + otn_arr4).astype(int)
            coord_rel_it = ((coord_rel + otn_coord_shar) * ts + otn_arr4).astype(int)
            coord_gun_start_bul_it = ((coord_gun_start_bul + otn_coord_shar2) * ts + otn_arr2).astype(int)

            polygon(c_scr, m_color, coord_gun_it)
            polygon(c_scr, t_color, coord_rel_it)
            aalines(c_scr, m_color, True, coord_gun_it)
            aalines(c_scr, t_color, True, coord_rel_it)

            return coord_gun_start_bul_it[0]

        def track(c_scr, coord, ts, trp):
            '''
            Отвечает за рисовку ходовой
            :param c_scr: Текущий экран
            :param coord: итерируемый объект с координатами центра верхней части корпуса
            :param ts: Коэффицент увеличения танка
            :param trp: UNRELEASED Состояние ходовой
            :return: Nothing
            '''
            cx = coord[0]
            cy = coord[1]
            tr_rad_sm = 10
            tr_rad_bi = 18
            otn_arr1 = np.array([cx, cy])
            coord_track_big = np.array([82, 40])
            coord_track_big_step = np.array([44, 0])
            coord_track_small_fr = np.array([110, 27])
            coord_track_small_ba = np.array([-120, 27])

            coord_track_small_fr_it = np.array((coord_track_small_fr * ts + otn_arr1)).astype(int)
            circle(c_scr, s_color, coord_track_small_fr_it, int(tr_rad_sm * ts))
            circle(c_scr, m_color, coord_track_small_fr_it, int((tr_rad_sm - 2) * ts))

            coord_track_small_ba_it = np.array((coord_track_small_ba * ts + otn_arr1)).astype(int)

            circle(c_scr, s_color, coord_track_small_ba_it, int(tr_rad_sm * ts))
            circle(c_scr, m_color, coord_track_small_ba_it, int((tr_rad_sm - 2) * ts))

            for iteral in range(5):
                coord_track_big_it = ((coord_track_big - coord_track_big_step * iteral) * ts + otn_arr1).astype(int)
                circle(c_scr, s_color, coord_track_big_it, int(tr_rad_bi * ts))
                circle(c_scr, m_color, coord_track_big_it, int((tr_rad_bi - 4) * ts))

        self.gun_pos = gun(self.scr, self.pos, self.size, ang, self.power_shoot)
        body(self.scr, self.pos, self.size, anb)
        track(self.scr, self.pos, self.size, self.track_pos)

    def shoot(self, bullet_data_base, but_mou):
        '''
        Отвечает за выстрел из орудия, Обязательно при применении результат записать в базу данных пуль, так же
        :param bullet_data_base: принимает базу данных пуль для добавления элемента
        :param but_mou: принимает номер кнопки, нажатой на мыши (1 или 3)
        :return: Изменённую базу данных пуль
        '''
        if but_mou == 1:
            bullet_data_base.append(Bullet(self.gun_angle, self.gun_pos, self.scr, self.power_shoot, BLACK))
        else:
            bullet_data_base.append(Bullet(self.gun_angle, self.gun_pos, self.scr, self.power_shoot, RED))
        self.load = 0
        return bullet_data_base

    def targeting(self, mouse_pos):
        '''
        Отвечает за обновление наклона орудия в зависимости от координат мыши и танка
        :param mouse_pos: итерируемый объект с координатами мыши
        :return: Nothing
        '''
        tangh1 = -(self.pos[0] - mouse_pos[0])
        tangh2 = (mouse_pos[1] - self.pos[1] + 50)
        if mouse_pos[1] > res[1] - 110 and mouse_pos[0] > self.pos[0]:
            self.gun_angle = 0
        elif mouse_pos[1] > res[1] - 110 and mouse_pos[0] <= self.pos[0]:
            self.gun_angle = 180
        elif tangh2 == 0:
            self.gun_angle = 0
        else:
            self.gun_angle = atan(tangh1 / tangh2) * 57.3 + 90

    def move(self):
        '''
        Отвечает за обновление координат тела и изменение его скорости
        :return: nothing
        '''
        self.pos[0] += self.speed
        if self.pos[0] < 135 * self.size:
            self.pos[0] = 135 * self.size
        if self.pos[0] > res[0] - 125 * self.size:
            self.pos[0] = res[0] - 125 * self.size


class Bullet:
    def __init__(self, gun_angle, gun_pos, current_screen, power, color):
        '''
        Отвечает за создание объекта "пуля"
        :param gun_angle: Угол наклона орудия в момент выстрела в градусах
        :param gun_pos: Позиция кончика орудия в момент выстрела в итерируемом объекте
        :param current_screen: Текущий экран
        :param power: Сила выстрела
        :param color: Цвет требуемой пули
        '''
        if color == BLACK:
            self.speed = 50 * power / 100  # Начальная скорость чёрной пули
        else:
            self.speed = 30  # Начальная скорость красной пули
        self.x_speed = int(self.speed * cos(gun_angle / 57.3))  # Скорость снаряда по оси Х
        self.y_speed = int(-self.speed * sin(gun_angle / 57.3))  # Скорость снаряда по оси Н
        self.rec_times = 0  # UNRELEASED Количество соударений пули
        self.time_alive = 0  # UNRELEASED Длительность жизни пули
        self.angle = gun_angle  # Угол наклона пули
        self.coord = gun_pos  # Координаты пули в итеририруемом объекте
        self.dmg = 1  # Урон пули
        self.radius = 5  # Толщина пули
        self.scr = current_screen  # Текущий экран
        self.color = color  # Цвет данной пули

    def draw(self):
        '''
        Рисует любой объект данного класса
        :return: nothing
        '''
        circle(self.scr, self.color, self.coord, self.radius)

    def collision(self, targ_db, number_in_db):
        '''
        Проверяет столкновения с объектами из итерируемого объекта, после столкновения удаляет пулю
        :param targ_db: итерируемый объект с объектами, требующими проверки
        :param number_in_db: Номер пули в базе данных, необходимо для удаления
        :return: Было ли попадание, номер объекта, в который попали
        '''
        for itera in range(len(targ_db)):
            if distance(targ_db[itera].pos, self.coord) <= targ_db[itera].radius:
                return True, itera
        global bullet_db
        if self.coord[0] <= 0 or self.coord[0] >= res[0]:
            self.x_speed = -self.x_speed
        elif self.coord[1] <= 0 or self.coord[1] >= res[1]:
            del bullet_db[number_in_db]
            return False, -1
        return False, 0

    def move(self):
        '''
        Отвечает за обновление координат тела и изменение его скорости
        :return: nothing
        '''
        self.coord = self.coord + np.array([self.x_speed, self.y_speed])
        self.y_speed += gravity


class Target:
    def __init__(self, current_screen):
        '''
        Задаёт основные параметры объектов
        :param current_screen: текущий экран для рисования
        '''
        self.scr = current_screen  # Текущий экран
        a = [randint(targ_rad_max, res[0] - targ_rad_max), randint(targ_rad_max, res[1] - targ_rad_max - 200)]
        self.pos = np.array(a)  # Массив numpy с координатами цели
        self.radius = randint(targ_rad_min, targ_rad_max)  # Радиус цели
        self.score = 5  # Очки за уничтожение цели
        self.x_speed = randint(targ_sp_min, targ_sp_max)  # Скорость цели по оси Х
        self.y_speed = randint(targ_sp_min, targ_sp_max)  # Скорость цели по оси Y

    def move(self):
        '''
        Отвечает за обновление координат тела и изменение его скорости
        :return: nothing
        '''
        self.pos[0] += self.x_speed
        self.pos[1] += self.y_speed
        if self.pos[0] < self.radius:
            self.x_speed = -self.x_speed
            self.pos[0] = self.radius
        if self.pos[0] > res[0] - self.radius:
            self.x_speed = -self.x_speed
            self.pos[0] = res[0] - self.radius
        if self.pos[1] < self.radius:
            self.y_speed = -self.y_speed
            self.pos[1] = self.radius
        if self.pos[1] > res[1] - self.radius - 200:
            self.y_speed = -self.y_speed
            self.pos[1] = res[1] - self.radius - 200

    def draw(self):
        '''
        Рисует любой объект данного класса
        :return: nothing
        '''
        circle(self.scr, RED, self.pos, self.radius)


class Enemy:
    def __init__(self, current_screen):
        '''
        Задаёт основные параметры объектов
        :param current_screen: текущий экран для рисования
        '''
        self.scr = current_screen  # Текущий экран
        a = [randint(targ_rad_max, res[0] - targ_rad_max), randint(targ_rad_max, res[1] - targ_rad_max - 200)]
        self.pos = np.array(a)  # numpy.array с координатами врага
        self.radius = 40  # Ширина врага
        self.score = 20  # Очки за убийство врага
        self.x_speed = randint(targ_sp_min, targ_sp_max)  # Скорость врага по оси Х
        self.y_speed = 0  # Скорость врага по оси Х

    def boombing(self, bomb_data):
        '''
        Отвечает за создание новой бомбы и занесение её в базу данных
        :param bomb_data: база данных
        :return: Обновлённая база данных
        '''
        bomb_data.append(Bomb(self.scr, self.pos))
        return bomb_data

    def move(self):
        '''
        Отвечает за обновление координат тела и изменение его скорости
        :return: nothing
        '''
        self.pos += np.array([self.x_speed, 0])

        if self.pos[0] < self.radius:
            self.x_speed = -self.x_speed
            self.pos[0] = self.radius
        if self.pos[0] > res[0] - self.radius:
            self.x_speed = -self.x_speed
            self.pos[0] = res[0] - self.radius

    def draw(self):
        '''
        Рисует любой объект данного класса
        :return: nothing
        '''
        leng = 30
        wid = 20
        otn_arr4 = np.array([[self.pos[0], self.pos[1]] * 4]).reshape(4, 2)
        coord1 = np.array([-wid, -leng // 4]) * 2 + self.pos
        rect(self.scr, tb_color, [coord1[0], coord1[1], 4 * wid, leng // 2])
        coord2 = np.array([[-6, -leng // 2],
                           [-4, -leng // 2],
                           [-4, leng // 2],
                           [-6, leng // 2 - 2]]) * 2
        coord3 = np.array([[6, -leng // 2],
                           [4, -leng // 2],
                           [4, leng // 2 - 2],
                           [6, leng // 2]]) * 2
        polygon(self.scr, t_color, coord2 + otn_arr4)
        polygon(self.scr, t_color, coord3 + otn_arr4)


class Bomb:
    def __init__(self, current_screen, curr_pos):
        '''
        Задаёт основные параметры объектов
        :param current_screen: текущий экран для рисования
        '''
        self.scr = current_screen  # Текущий экран
        self.pos = deepcopy(curr_pos)  # Координаты бомбы
        self.radius = 5  # Ширина бомбы
        self.score = 1  # Очки за уничтожение бомбы
        self.y_speed = 0  # Скорость бомбы по оси Y

    def boom(self, player):
        '''
        Проверяет на столкновение с объектом player
        :param player: Искомый объект
        :return: 2 - попала, 1 - не попала, 0 - ещё летит
        '''
        if self.pos[1] >= player.pos[1]:
            if player.pos[0] - 135 - self.radius < self.pos[0] < player.pos[0] + 135 + self.radius:
                return 2
            return 1
        return 0

    def move(self):
        '''
        Отвечает за обновление скорости и координат объекта
        :return: nothing
        '''
        self.pos[1] += self.y_speed
        self.y_speed += gravity

    def draw(self):
        '''
        Рисует любой объект данного класса
        :return: nothing
        '''
        coord1 = self.pos - np.array([self.radius, 20])
        otn_coord3 = np.array([[self.pos[0], self.pos[1]] * 3]).reshape(3, 2)
        coord2 = np.array([[0, 0],
                           [-2 * self.radius, -20],
                           [2 * self.radius, -20]])
        polygon(self.scr, tb_color, coord2 + otn_coord3)
        circle(self.scr, RED, self.pos + np.array([0, 20]), self.radius)
        rect(self.scr, t_color, [coord1[0], coord1[1], 2 * self.radius, 40])


pygame.init()
pygame.font.init()
FPS = 60
res = get_res()

bullet_db = []  # База данных с пулями
target_db = []  # База данных с целями
enemy_db = []  # База данных с врагами
bomb_db = []  # База данных с бомбами

screen = pygame.display.set_mode(res)

pygame.display.update()
clock = pygame.time.Clock()
finished = False
charging = False
tick = 0  # Номер текущего тика
score = 0  # Текущий счёт игрока

main_tank = Tank(screen)  # Играбельный танк игрока
mouse = Mouse()  # Мышь игрока
tank_max_speed = 10  # Наибольшая, развиваемая танком скорость
gravity = 1  # Константа гравитации
reloading_time = 100  # Время перезарядки танка
err = 0  # Время отображения ошибки

targ_rad_min = 40  # Наименьший радиус мишени
targ_rad_max = 50  # Наибольший радиус мишени
targ_sp_min = 2  # Наименьшая скорость мишение
targ_sp_max = 5  # Наибольшая скорость мишени

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        '''
        Серия проверок событий'''
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            button = event.key
            if button == 27:
                finished = True
        elif event.type == pygame.MOUSEMOTION:
            mouse.pos = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            charging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            charging = False
            if main_tank.load >= reloading_time:
                bullet_db = main_tank.shoot(bullet_db, event.button)
            else:
                err = 30
            main_tank.power_shoot = 0
        if main_tank.hp <= 0:
            finished = True

    '''
    Блок, отвечающий за изменение скорости танка в зависимости от нажатой кнопки'''
    keys = pygame.key.get_pressed()
    if keys[100] and keys[97]:
        main_tank.speed = 0
    elif keys[100]:
        main_tank.speed = tank_max_speed
    elif keys[97]:
        main_tank.speed = -tank_max_speed
    else:
        main_tank.speed = 0

    # Обновление позиции прицела танка и его координат
    main_tank.targeting(mouse.pos)
    main_tank.move()

    # Отрисовка простых объектов
    main_tank.draw()
    mouse.draw(screen)

    # Анализ столкновений
    for i in range(len(bullet_db) - 1, -1, -1):
        bullet_db[i].draw()
        bullet_db[i].move()
        hit1, numb1 = bullet_db[i].collision(target_db, i)
        if numb1 != -1:
            hit2, numb2 = bullet_db[i].collision(enemy_db, i)
        else:
            hit2, numb2 = False, -1
        if numb2 != -1:
            hit3, numb3 = bullet_db[i].collision(bomb_db, i)
        else:
            hit3, numb3 = False, -1
        if hit1:
            score += target_db[numb1].score
            del target_db[numb1]
            del bullet_db[i]
        elif hit2:
            score += enemy_db[numb2].score
            del enemy_db[numb2]
            del bullet_db[i]
        elif hit3:
            score += bomb_db[numb3].score
            del bomb_db[numb3]
            del bullet_db[i]

    # Отрисовка врагов и обновление их координат
    for i in range(len(enemy_db) - 1, -1, -1):
        enemy_db[i].move()
        enemy_db[i].draw()
    # Отрисовка бомб, обновление их координат и проверка на взрымы
    for i in range(len(bomb_db) - 1, -1, -1):
        bomb_db[i].move()
        t = bomb_db[i].boom(main_tank)
        if t == 2:
            main_tank.hp -= 1
            del bomb_db[i]
        elif t == 1:
            del bomb_db[i]
        elif t == 0:
            bomb_db[i].draw()

    # Отрисовка и обновление координат мишеней
    for i in range(len(target_db)):
        target_db[i].draw()
        target_db[i].move()

    # Блок, отвечающий за создание новых объектов и их периоды
    if tick % (4 * FPS) == 0:
        target_db.append(Target(screen))
    if tick % (5 * FPS) == 0:
        enemy_db.append(Enemy(screen))
    if tick % (3 * FPS) == 0:
        for i in range(len(enemy_db)):
            bomb_db = enemy_db[i].boombing(bomb_db)

    # Модуль, отвечающий за наколение заряда орудия
    if charging:
        main_tank.power_shoot += 5
    if main_tank.power_shoot >= 100:
        main_tank.power_shoot = 100
    main_tank.load += 1

    # Отображение статуса орудия
    if main_tank.load >= reloading_time:
        main_tank.load = reloading_time
        font = pygame.font.Font(None, 40)
        text = font.render("RELOADING:" + str(int(main_tank.load / reloading_time * 10000) / 100) + '%', True,
                           (0, 255, 0))
        place = text.get_rect(center=(150, 50))
        screen.blit(text, place)
    else:
        font = pygame.font.Font(None, 40)
        text = font.render("RELOADING:" + str(int(main_tank.load / reloading_time * 10000) / 100) + '%', True,
                           (255, 0, 0))
        place = text.get_rect(center=(150, 50))
        screen.blit(text, place)

    # Отображение здоровья
    font = pygame.font.Font(None, 40)
    text = font.render("HP:" + str(main_tank.hp), True, (255, 0, 0))
    place = text.get_rect(center=(150, 150))
    screen.blit(text, place)

    # Отображение ошибки перезарядки
    if err > 0:
        font = pygame.font.Font(None, 50)
        text = font.render("RELOADING, WAIT", True, (255, 0, 0))
        place = text.get_rect(center=(res[0] / 2, 200))
        screen.blit(text, place)
        err -= 1

    # Отображение счёта
    font = pygame.font.Font(None, 40)
    text = font.render("SCORE:" + str(score), True, (0, 100, 255))
    place = text.get_rect(center=(150, 100))
    screen.blit(text, place)

    # Отображение инструкции
    if tick < FPS * 10:
        font = pygame.font.Font(None, 40)
        text = font.render("Используйте LMB для выстрела с переменной стартовой скоростью", True, (100, 100, 0))
        place = text.get_rect(center=(res[0] // 2, 100))
        screen.blit(text, place)
        font = pygame.font.Font(None, 40)
        text = font.render("Используйте RMB для выстрела с постоянной стартовой скоростью", True, (100, 100, 0))
        place = text.get_rect(center=(res[0] // 2, 150))
        screen.blit(text, place)
    tick += 1
    pygame.display.update()
    screen.fill(WHITE)
print('Congratulations! Your score is', score)
