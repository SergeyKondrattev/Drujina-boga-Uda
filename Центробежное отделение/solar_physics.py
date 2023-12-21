from random import randint
from solar_visuals import *

gravitational_constant = 6.67408E-11
"""Гравитационная постоянная Ньютона G"""



class Star():
    """Тип данных, описывающий звезду.
    Содержит массу, координаты, скорость звезды,
    а также визуальный радиус звезды в пикселах и её цвет.
    """

    type = "star"
    """Признак объекта звезды"""

    m = 0
    """Масса звезды"""

    x = 0
    """Координата по оси **x**"""

    y = 0
    """Координата по оси **y**"""

    Vx = 0
    """Скорость по оси **x**"""

    Vy = 0
    """Скорость по оси **y**"""

    Fx = 0
    """Сила по оси **x**"""

    Fy = 0
    """Сила по оси **y**"""

    R = 5
    """Радиус звезды"""

    color = "red"
    """Цвет звезды"""

    image = None
    """Изображение звезды"""


class Planet():
    """Тип данных, описывающий планету.
    Содержит массу, координаты, скорость планеты,
    а также визуальный радиус планеты в пикселах и её цвет
    """

    type = "planet"
    """Признак объекта планеты"""

    m = 0
    """Масса планеты"""

    x = 0
    """Координата по оси **x**"""

    y = 0
    """Координата по оси **y**"""

    Vx = 0
    """Скорость по оси **x**"""

    Vy = 0
    """Скорость по оси **y**"""

    Fx = 0
    """Сила по оси **x**"""

    Fy = 0
    """Сила по оси **y**"""

    R = 0
    """Радиус планеты"""

    color = "green"
    """Цвет планеты"""

    image = None
    """Изображение планеты"""


def calculate_force(body, space_objects, W):
    """Вычисляет силу, действующую на тело.

    Параметры:

    **body** — тело, для которого нужно вычислить дейстующую силу.

    **space_objects** — список объектов, которые воздействуют на тело.
    """

    sf = 4.8e-08
    body.Fx = body.Fy = 0
    for obj in space_objects:
        if ((body.x - obj.x)**2 + (body.y - obj.y)**2) == 0:
            continue
        if ((sf * body.x - sf * obj.x)**2 + (sf * body.y - sf * obj.y)**2)**0.5 > 0.95*(body.R + obj.R) and((sf * body.x - sf * obj.x)**2 + (sf * body.y - sf * obj.y)**2)**0.5 <= (body.R + obj.R) and body.m != 0:
            center_m = body.m + obj.m
            center_x = (body.x * body.m + obj.x * obj.m)/center_m
            center_y = (body.y * body.m + obj.y * obj.m)/center_m
            rc_x = body.x - center_x
            rc_y = body.y - center_y
            body.Fx += body.m * W**2 * rc_x
            body.Fy += body.m * W**2 * rc_y
            """Вычисляет центробежную силу."""
        r = ((body.x - obj.x)**2 + (body.y - obj.y)**2)**0.5
        body.Fx += gravitational_constant * body.m * obj.m / r**3 * (obj.x - body.x)
        body.Fy += gravitational_constant * body.m * obj.m / r**3 * (obj.y - body.y)


def move_space_object(body, dt, space_objects, W):
    """Перемещает тело в соответствии с действующей на него силой.

    Параметры:

    **body** — тело, которое нужно переместить.
    """
    sf = 4.8e-08
    if body.m != 0:
        ax = body.Fx / body.m
        body.x += body.Vx * dt + ax * dt**2 / 2
        body.Vx += ax * dt
        ay = body.Fy / body.m
        body.y += body.Vy * dt + ay * dt**2 / 2
        body.Vy += ay * dt
    """Проверяет слипшиеся тела и вращает их с заданной угловой скоростью"""
    for obj in space_objects:
        if obj == body or obj.m == 0:
            continue
        elif ((sf * body.x - sf * obj.x)**2 + (sf * body.y - sf * obj.y)**2)**0.5 > (body.R + obj.R):
            continue
        elif ((sf * body.x - sf * obj.x)**2 + (sf * body.y - sf * obj.y)**2)**0.5 < 0.95*(body.R + obj.R):
            x1 = body.x - obj.x
            y1 = body.y - obj.y
            if (x1 != 0) and (y1 != 0):
                body.x = obj.x + x1 / abs(x1) * (body.R+obj.R)/(1 + x1**2/y1**2)**0.5/(sf)
                body.y = obj.y + y1 / abs(y1) * (body.R+obj.R)/(1 + x1**2/y1**2)**0.5/(sf)
            elif (x1 != 0):
                body.x = obj.x + x1 / abs(x1) * (body.R+obj.R)/(sf)
                body.y = obj.y
            else:
                body.y = obj.y + y1 / abs(y1) * (body.R+obj.R)/(sf)
                body.x = obj.x
        elif obj.m != 0:
            center_m = body.m + obj.m
            center_x = (body.x * body.m + obj.x * obj.m)/center_m
            center_y = (body.y * body.m + obj.y * obj.m)/center_m

            rc_x = body.x - center_x
            rc_y = body.y - center_y
            r = (rc_y**2 + rc_x**2)**0.5
            sin = rc_y/r
            cos = rc_x/r
            v = W * r
            if sin * cos >= 0:
                sin = -rc_y/r
                cos = rc_x/r
            elif sin * cos < 0:
                sin = rc_y/r
                cos = -rc_x/r
            body.Vx = v * cos
            body.Vy = v * sin

            body.x += body.Vx * dt
            body.y += body.Vy * dt


    '''zhitь ( ͡ಥ ͜ʖ ͡ಥ)'''


def recalculate_space_objects_positions(space_objects, dt, W):
    """Пересчитывает координаты объектов.

    Параметры:

    **space_objects** — список оьъектов, для которых нужно пересчитать координаты.

    **dt** — шаг по времени
    """

    for body in space_objects:
        calculate_force(body, space_objects, W)
    for body in space_objects:
        move_space_object(body, dt, space_objects, W)


if __name__ == "__main__":
    print("This module is not for direct call!")
