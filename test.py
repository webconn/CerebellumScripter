#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Здесь рассмотрим, как используется библиотека для связи с роботом в Cerebellum
# Постараюсь рассмотреть все основные конструкции и особенности работы с шасси,
# датчиками и актуаторами

# Подключаем библиотеку - файл должен лежать в директории со скриптом!
import cerebellum as c

c.DEBUG = True

# Надо будет немного тупить, поэтому и это тоже подключаем
from time import sleep


# Подключаемся к серверу - адрес условный, хотя таким и останется, скорее всего
c.connect("tcp://localhost:1234")


# Этап 1: настраиваем ODetect - обнаружение противника и препятствий.
# Функция принимает битовую маску, определяющую настраиваемые датчики
# и значение порога по дистанции (в сантиметрах). Если порог будет превышен -
# робот остановится (но сервы продолжат двигаться!)

# У ODetect шесть датчиков: перед, зад, лево, право, а также перед-лево и
# перед-право. Для каждого датчика определена константа
# OD_FRONT, OD_REAR, OD_LEFT, OD_RIGHT, OD_FLEFT, OD_FRIGHT.
# Также есть объединения - OD_FULLFRONT для всех передних,
# OD_SIDES - левый и правый, OD_ALL - все датчики

# Зададим границу в 20 сантиметров для всех передних датчиков
c.odetect_limit(c.OD_FULLFRONT, 20.0)

# По 10 сантиметров - для всех остальных
c.odetect_limit(c.OD_ALL ^ c.OD_FULLFRONT, 10.0)


# Этап 2. Выбор зоны
# Все датчики, вроде выбора зоны, шморгалка и прочие кнопки, сканируются
# функцией bsensor_get (от binary sensor). Функция вернёт True, если кнопка
# нажата.

if c.bsensor_get(c.BSENSOR_SELECTOR):
    zone = "left"
else:
    zone = "right"


# Этап 3. Тупим в шморгалку
# Всё аналогично, шморгалка вполне себе бинарный сенсор
while c.bsensor_get(c.BSENSOR_SHMORGALKA):
    pass


# Этап 4. Поехали!
#
# Основная функция для движения - twist. Она только посылает команду на
# движение шасси и сразу возвращается - дальнейшие действия будут выполняться
# "на ходу". Для того, чтобы этого избежать, есть функция twist_block. Она
# заблокируется на время движения робота.
#
# Обе функции принимают три аргумента - левая скорость, правая скорость и
# дистанция. (всё в сантиметрах, скорость - ориентировочная (надо провести
# параллель с сантиметрами в секунду, я постараюсь это реализовать)
#
# Скорость задаётся знаковым значением! Положительная - вперёд, отрицательная -
# назад. Расстояние - беззнаковое.

# Едем со скоростью 10 вперёд на 100 сантиметров и тупим :D
c.twist_block(10.0, 10.0, 100.0)


# Едем со скоростью 20 назад на 50 сантиметров и делаем "полезную работу"
# Для того, чтобы дождаться окончания движения робота, применяем функцию
# twist_wait()
c.twist(-20.0, -20.0, 50.0)

# Делаем полезную работу 1 секунду, после чего дожидаемся прохождения дистанции
sleep(1)
c.twist_wait()


# Поворот на месте - twist_rotate или twist_rotate_block. Принимает скорость
# вращения левого колеса (правому задаётся та же скорость с обратным знаком) и
# угол вращения (в градусах)

# Поворачиваемся против часовой стрелки на 90 градусов со скоростью 10
c.twist_rotate_block(-10.0, 90.0)


# Есть также возможность настроить ускорение разгона и торможения. Это делается
# функцией dynamics. Ускорение - ориентировочно сантиметры на секунду в квадрате

# Задаём ускорение разгона 1.0, торможения - 0.5
c.dynamics(1.0, 0.5)


# Для того, чтобы двигать сервами, есть функция servo. Принимает на вход номер
# управляемой сервы и её положение (в градусах от 0 до 180)
c.servo(c.SERVO_PAW, 90.0)

# Помашем лапкой! :)
for i in range(0, 180, 5):
    c.servo(c.SERVO_PAW, i)
    sleep(0.1)

for i in range(180, 0, -5):
    c.servo(c.SERVO_PAW, i)
    sleep(0.1)
