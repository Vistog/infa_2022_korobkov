import math
from random import randint
import pygame
from pygame.draw import *
from pygame.font import *
from screeninfo import get_monitors

points = 0  # Счётчик очков
score_circle = 2  # Количество очков, даваемое за попадание в шар
score_arrow = 5  # Количество очков, даваемое за попадание в стрелу
speed_circle = [5, 20]  # Границы скорости шара
speed_arrow = [20, 30]  # Границы скорости стрелы
timing = 200  # Время жизни объекта
tick = 0  # Номер текущего тика
obj = []  # База данных с объектами на экране


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


def new_circle():
    """
    генерирует новый шарик и возвращает его координаты в базу данных об объектах на экране, Данные поступают в базу данных
    в формате dict с ключами {'coord_x', 'coord_y', 'color', 'size', 'type', 'time_alive', 'speed',
           'speed_angle', 'speed_x', 'speed_y': int(sp_y), 'score': score_circle}
    """
    x = randint(100, res[0] - 70)
    y = randint(100, res[1] - 70)
    r = randint(30, 70)
    color = COLORS[randint(0, 5)]
    deg = randint(0, 359)
    speed = randint(speed_circle[0], speed_circle[1])
    sp_x = math.cos(deg / 57.3) * speed
    sp_y = math.sin(deg / 57.3) * speed
    cir = {'coord_x': x, 'coord_y': y, 'color': color, 'size': r, 'type': 'circle', 'time_alive': 0, 'speed': speed,
           'speed_angle': deg, 'speed_x': int(sp_x), 'speed_y': int(sp_y), 'score': score_circle}
    return cir


def new_arrow():
    """
    генерирует новую стрелу и возвращает её координаты в базу данных об объектах на экране,
    Данные поступают в базу данных в формате dict с ключами
    {'coord_x', 'coord_y', 'color', 'size', 'type', 'time_alive', 'speed',
           'speed_angle', 'speed_x', 'speed_y': int(sp_y), 'score': score_circle}
    """
    x = randint(100, res[0] - 70)
    y = randint(100, res[1] - 70)
    r = randint(30, 70)
    color = COLORS[randint(0, 5)]
    deg = randint(0, 359)
    speed = randint(speed_arrow[0], speed_arrow[1])
    sp_x = math.cos(deg / 57.3) * speed
    sp_y = math.sin(deg / 57.3) * speed
    arr = {'coord_x': x, 'coord_y': y, 'color': color, 'size': r, 'type': 'arrow', 'time_alive': 0, 'speed': speed,
           'speed_angle': deg, 'speed_x': int(sp_x), 'speed_y': int(sp_y), 'score': score_arrow}
    return arr


def arrow(scr, color, coord, size, deg):
    """
    :param scr: Экран, на котором русуется стрела
    :param color: Цвет стрелы
    :param coord: Координаты вершины стрелы
    :param size: половина высоты треугольника
    :param deg: угол между горизонтальной осью и стрелой, отсчитывается против часовой стрелки
    Данная функция рисует стрелу на экране по заданным параметрам
    """
    x1, y1 = coord[0], coord[1]
    L = 2 * size * math.tan(15 / 57.3)
    x2 = x1 - 2 * size * math.cos(deg / 57.3) + L * math.sin(deg / 57.3)
    y2 = y1 + 2 * size * math.sin(deg / 57.3) + L * math.cos(deg / 57.3)
    x3 = x1 - 2 * size * math.cos(deg / 57.3) - L * math.sin(deg / 57.3)
    y3 = y1 + 2 * size * math.sin(deg / 57.3) - L * math.cos(deg / 57.3)
    pygame.draw.polygon(scr, color, [[x1, y1], [x2, y2], [x3, y3]])


def upd(object_data_base, time_of_life):
    """
    :param object_data_base: База данным о существующих объектах
    :param time_of_life: Время, в течение которого объект может существовать на экране
    :return: Возвращает обновлённую базу данных с учётом пропавших объектов
    Данная функция отвечает за очистку экрана и проверку времени существования объектов, а так же удаляет "просроченных"
    """
    for i in range(len(object_data_base) - 1, -1, -1):
        object_data_base[i]['time_alive'] += 1
        if object_data_base[i]['time_alive'] > time_of_life:
            del object_data_base[i]
            global points
            points -= 1
    screen.fill(BLACK)
    return object_data_base


def draw(scr, object_data_base):
    """
    :param scr: Экран, на котором нужно нарисовать
    :param object_data_base: База данных о существующих в данный момент объектах
    Данная функция отвечает за рисование всех существующих объектов при каждом обновлении экрана
    """
    for i in object_data_base:
        if i['type'] == 'circle':
            circle(scr, i['color'], (i['coord_x'], i['coord_y']), i['size'])
        elif i['type'] == 'arrow':
            arrow(scr, i['color'], (i['coord_x'], i['coord_y']), i['size'], -i['speed_angle'])


def moving(odj, numbertick):
    """
    :param odj: База данных о существующих в данный момент объектах
    :param numbertick: Номер тика, в данный момент
    :return: Возвращает обновлённую базу данных с учётом движений объектов
    Данная функция отвечает за рассчёт движений объектов на экране, использует подфункцию для рассчёта столкновений
    """
    for i in range(len(odj)):
        if odj[i]['type'] == 'circle':
            odj[i]['coord_x'] += odj[i]['speed_x']
            odj[i]['coord_y'] += odj[i]['speed_y']
            odj = rikocheting(odj, i)
        elif odj[i]['type'] == 'arrow':
            if numbertick % 500 == 0:
                for z in range(10):
                    odj[i]['coord_x'] += odj[i]['speed_x']
                    odj[i]['coord_y'] += odj[i]['speed_y']
                    odj = rikocheting(odj, i)
    return odj


def rikocheting(odj, i):
    """
    :param odj: База данных о существующих в данный момент объектах
    :param i: Номер рассматриваемого объекта
    :return: Обновлённая база данных с учётом столкновений со стенками
    Рассчитывает направления отскоков и новые скорости для объектов в случае столкновения со стенкой
    """
    if odj[i]['coord_x'] <= odj[i]['size']:
        obj[i]['speed_angle'] = randint(-90, 90)
        odj[i]['speed_x'] = int(odj[i]['speed'] * math.cos(obj[i]['speed_angle'] / 57.2975))
        odj[i]['speed_y'] = int(odj[i]['speed'] * math.sin(obj[i]['speed_angle'] / 57.2975))
    if odj[i]['coord_x'] >= res[0] - odj[i]['size']:
        obj[i]['speed_angle'] = randint(90, 180)
        odj[i]['speed_x'] = int(odj[i]['speed'] * math.cos(obj[i]['speed_angle'] / 57.2975))
        odj[i]['speed_y'] = int(odj[i]['speed'] * math.sin(obj[i]['speed_angle'] / 57.2975))
    if odj[i]['coord_y'] <= odj[i]['size']:
        obj[i]['speed_angle'] = randint(0, 180)
        odj[i]['speed_x'] = int(odj[i]['speed'] * math.cos(obj[i]['speed_angle'] / 57.2975))
        odj[i]['speed_y'] = int(odj[i]['speed'] * math.sin(obj[i]['speed_angle'] / 57.2975))
    if odj[i]['coord_y'] >= res[1] - odj[i]['size']:
        obj[i]['speed_angle'] = randint(180, 360)
        odj[i]['speed_x'] = int(odj[i]['speed'] * math.cos(obj[i]['speed_angle'] / 57.2975))
        odj[i]['speed_y'] = int(odj[i]['speed'] * math.sin(obj[i]['speed_angle'] / 57.2975))
    return odj


def collision_check(odj, cl_x, cl_y, cl_but):
    """
    :param odj:  База данных о существующих в данный момент объектах
    :param cl_x: Координата клика мышкой по оси X
    :param cl_y: Координата клика мышкой по оси Y
    :param cl_but: Кнопка, на которую нажали
    :return: Возвращает обновлённую базу данных с учётом исчезновения шаров от кликов мышью
    Данная функция отвечает за проверку попаданий по шарам и стелам, а так же за соответствие кнопки мыши типу объекта
    """
    for i in range(len(odj)):
        global points
        if odj[i]['type'] == 'circle' and cl_but == 1:
            if (cl_x - odj[i]['coord_x']) ** 2 + (cl_y - odj[i]['coord_y']) ** 2 <= odj[i]['size'] ** 2:
                points += odj[i]['score']
                del odj[i]
                return odj
        elif odj[i]['type'] == 'arrow' and cl_but == 3:
            if (cl_x - (odj[i]['coord_x'] - odj[i]['size'] * math.cos(-odj[i]['speed_angle'] / 57.3))) ** 2 \
                    + (cl_y - (odj[i]['coord_y'] + odj[i]['size'] * math.sin(-odj[i]['speed_angle'] / 57.3))) ** 2 \
                    <= odj[i]['size'] ** 2:
                points += odj[i]['score']
                del odj[i]
                return odj
    return odj


pygame.init()
pygame.font.init()
global res
FPS = 60
res = get_res()

screen = pygame.display.set_mode(res)

"""
Задание цветов, в которые могут быть раскрашены объекты
"""
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            """
            Условие остановки программы при закрытии окна
            """
            finished = True
        elif event.type == pygame.KEYDOWN:
            """
            Условие выхода из игры при нажатии клавиши <<ESC>>
            """
            if event.key == 27:
                finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            """
            Проверка попадания в случае клика мышью
            """
            mouse_button = event.button
            mouse_pos_x, mouse_pos_y = event.pos
            obj = collision_check(obj, mouse_pos_x, mouse_pos_y, mouse_button)
    if (2 * tick) % FPS == 0:
        """
        Блок, отвечающий за частоту создания шаров
        """
        obj.append(new_circle())
    if tick % (2 * FPS) == 0:
        """
        Блок, отвечающий за частоту создания стрел
        """
        obj.append(new_arrow())
    if tick < 200:
        """
        Блок, отвечающий за показ инструкции на экране
        """
        font = pygame.font.Font(None, 36)
        text = font.render("To catch circles use LMB, and RMB to triangles", True, (100, 100, 0))
        place = text.get_rect(center=(res[0] / 2, 100))
        screen.blit(text, place)
    """
    Блок, отвечающий за показ счёта на экране
    """
    font = pygame.font.Font(None, 72)
    text = font.render("points:" + str(points), True, (255, 0, 0))
    place = text.get_rect(center=(100, 100))
    screen.blit(text, place)
    """
    Блок, отвечащий за ежетиковое оновление экрана, вызова функций заполнения объектов, рассчёта их перемещений
    и проверки объектов на превышение времени существования
    """
    draw(screen, obj)
    pygame.display.update()
    obj = upd(obj, timing)
    obj = moving(obj, tick)
    tick += 1

pygame.quit()
