import tkinter
from tkinter.filedialog import *
from math import pi
# раскомментируйте три строки ниже
from solar_visuals import * 
from solar_physics import *
from solar_read import *


perform_execution = False
"""Флаг цикличности выполнения расчёта"""

physical_time = 0
"""Физическое время от начала расчёта.
Тип: float"""

displayed_time = None
"""Отображаемое на экране время.
Тип: переменная tkinter"""

time_step = None
"""Шаг по времени при моделировании.
Тип: float"""

space_objects = []
"""Список космических объектов."""


def execution():
    """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
    а также обновляя их положение на экране.
    Цикличность выполнения зависит от значения глобальной переменной perform_execution.
    При perform_execution == True функция запрашивает вызов самой себя по таймеру через от 1 мс до 100 мс.
    """
    global physical_time
    global displayed_time
    recalculate_space_objects_positions(space_objects, time_step.get())
    for body in space_objects:
        update_object_position(space, body)
    for body in space_objects:
        for obj in space_objects:
            if not(body is obj) and (body.x - obj.x)**2 + (body.y - obj.y)**2 < (body.R + obj.R)**2 and body.type == obj.type == 'planet':
                collision(body, obj)
    
    physical_time += time_step.get()
    displayed_time.set("%.1f" % physical_time + " seconds gone")

    if perform_execution:
        space.after(101 - time_speed, execution)


def start_execution():
    """Обработчик события нажатия на кнопку Start.
    Запускает циклическое исполнение функции execution.
    """
    global perform_execution
    perform_execution = True
    start_button['text'] = "Pause"
    start_button['command'] = stop_execution

    execution()
    print('Started execution...')


def stop_execution():
    """Обработчик события нажатия на кнопку Start.
    Останавливает циклическое исполнение функции execution.
    """
    global perform_execution
    perform_execution = False
    start_button['text'] = "Start"
    start_button['command'] = start_execution
    print('Paused execution.')


def open_file_dialog():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    global space_objects
    global perform_execution
    perform_execution = False
    for obj in space_objects:
        space.delete(obj.image)  # удаление старых изображений планет
    in_filename = askopenfilename(filetypes=(("Text file", ".txt"),))
    space_objects = read_space_objects_data_from_file(in_filename)
    max_distance = max([max(abs(obj.x), abs(obj.y)) for obj in space_objects])
    calculate_scale_factor(max_distance)

    for obj in space_objects:
        if isinstance(obj, Star):
            create_star_image(space, obj)
        elif isinstance(obj, Planet):
            create_planet_image(space, obj)
        else:
            raise AssertionError()


def save_file_dialog():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    out_filename = asksaveasfilename(filetypes=(("Text file", ".txt"),))
    write_space_objects_data_to_file(out_filename, space_objects)


def collision(body, obj):
    global space_objects
    global space
    body_rho = body.m / 4*3 / pi / body.R**3
    obj_rho = obj.m / 4*3 / pi / obj.R**3
    
    """Ищет прямоугольник, внутри которого происходит столкновение"""
    collision_rect_bottom = max(body.y - body.R, obj.y - obj.R)
    collision_rect_up = min(body.y + body.R, obj.y + obj.R)
    collision_rect_left = max(body.x - body.R, obj.x - obj.R)
    collision_rect_right = min(body.x + body.R, obj.x + obj.R)
    x0 = (collision_rect_left + collision_rect_right)/2
    y0 = (collision_rect_up + collision_rect_bottom)/2

    if body.m > obj.m:
        large = body
        small = obj
    else:
        large = obj
        small = body

    space.delete(body.image)
    if body in space_objects:
        space_objects.remove(body)
    space.delete(obj.image)
    if obj in space_objects:
        space_objects.remove(obj)
    frag = Fragment()
    frag.x, frag.y = x0, y0
    frag.R = (collision_rect_up - collision_rect_bottom + collision_rect_right - collision_rect_left)/1.8
    frag_rho = (body_rho + obj_rho)/2
    frag.m = frag_rho * 4/3 * pi * frag.R**3
    frag.Vx, frag.Vy = small.Vx*1.15, small.Vy*1.15
    
    new_planet = Planet()
    new_planet.m = large.m + small.m - frag.m
    new_planet.x, new_planet.y = large.x, large.y
    new_planet.R = large.R * 0.8
    new_planet.Vx, new_planet.Vy = large.Vx, large.Vy
    new_planet.color = 'darkolivegreen'
    create_planet_image(space, new_planet)
    create_planet_image(space, frag)
    space_objects.append(new_planet)
    space_objects.append(frag)


def main():
    """Главная функция главного модуля.
    Создаёт объекты графического дизайна библиотеки tkinter: окно, холст, фрейм с кнопками, кнопки.
    """
    global physical_time
    global displayed_time
    global time_step
    global time_speed
    global space
    global start_button

    print('Modelling started!')
    physical_time = 0

    root = tkinter.Tk()
    # космическое пространство отображается на холсте типа Canvas
    space = tkinter.Canvas(root, width=window_width, height=window_height, bg="black")
    space.pack(side=tkinter.TOP)
    # нижняя панель с кнопками
    frame = tkinter.Frame(root)
    frame.pack(side=tkinter.BOTTOM)

    start_button = tkinter.Button(frame, text="Start", command=start_execution, width=6)
    start_button.pack(side=tkinter.LEFT)

    time_step = tkinter.DoubleVar()
    time_step.set(1)
    time_step_entry = tkinter.Entry(frame, textvariable=time_step)
    time_step_entry.pack(side=tkinter.LEFT)

    time_speed = 60

    load_file_button = tkinter.Button(frame, text="Open file...", command=open_file_dialog)
    load_file_button.pack(side=tkinter.LEFT)
    save_file_button = tkinter.Button(frame, text="Save to file...", command=save_file_dialog)
    save_file_button.pack(side=tkinter.LEFT)

    displayed_time = tkinter.StringVar()
    displayed_time.set(str(physical_time) + " seconds gone")
    time_label = tkinter.Label(frame, textvariable=displayed_time, width=30)
    time_label.pack(side=tkinter.RIGHT)

    root.mainloop()
    print('Modelling finished!')

if __name__ == "__main__":
    main()
