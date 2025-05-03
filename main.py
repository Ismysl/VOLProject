#import pandas as pd
import numpy as np
import cv2
#import matplotlib.pyplot as plt
import math, copy
import os
import glob
#import pyautogui

# Инициализация переменных
drawing = False # Флаг для определения, рисуется ли линия
start_point = () # Начальная точка линии
end_point = () # Конечная точка линии
coordinates = [] # Создаем список для хранения координат

def draw_square(img_asis, center, size, color):
    top_left = (center[0] - size // 2, center[1] - size // 2)
    bottom_right = (center[0] + size // 2, center[1] + size // 2)
    cv2.rectangle(img_asis, top_left, bottom_right, color, 2)


# Функция обратного вызова для обработки событий кнопки мыши
def mouse_callback(event, x, y, flags, params):
    global start_point, end_point
    if event == cv2.EVENT_LBUTTONDOWN:
        if start_point is None:
            start_point = (x, y)
        else:
            end_point = (x, y)
            cv2.line(img_asis, start_point, end_point, (0, 0, 255), 2)
            start_point = None
            end_point = None
    if event == cv2.EVENT_RBUTTONDOWN:
        draw_square(img_asis, (x, y), 10, (0, 255, 0))  # Рисуем зеленый квадрат размером 50x50 пикселей
        params.append((x, y))
        print(f"Правая кнопка мыши нажата в координатах: ({x}, {y})")
        print('Список координат', coordinates)


# Путь к папке с исходными изображениями
source_folder = 'D:/Work/Football/VOLProject'
# Переходим в директорию с изображениями
os.chdir(source_folder)

# Получаем список всех файлов .png и .jpg в директории
image_files = glob.glob('*.png') + glob.glob('*.jpg')

if not image_files:
    print("No PNG files found in the directory.")
else:
    # Обрабатываем каждое изображение
    for image_file in image_files:
        print("Processing file:", image_file)
        try:
            img = cv2.imread(image_file, 1)
            if img is None:
                print(f"Failed to read image {image_file}")
                continue
            # Further processing...
        except Exception as e:
            print(f"Error processing {image_file}: {e}")

        print("start")

        # Создание окна
        cv2.namedWindow('image')

        # Установка обработчика событий мыши
        cv2.setMouseCallback('image', mouse_callback, param=coordinates)

        # Переменные для хранения начальной и конечной точек
        start_point = None
        end_point = None
        flag_Q = 0
        img_asis = copy.copy(img)

        while True:
            # Рисование линии, если указаны начальная и конечная точки
            cv2.imshow('image', img_asis)
            if cv2.waitKey(1) & 0xFF == 27:  # Если нажата клавиша 'Esc'
                break
            elif cv2.waitKey(1) & 0xFF == 32: # Если нажата клавиша 'Space'
                flag_Q = 1
                break
        cv2.destroyAllWindows()

        if flag_Q == 1:
            img_asis = cv2.flip(img_asis, 1)


        hsv = cv2.cvtColor(img_asis, cv2.COLOR_BGR2HSV)
        # Определение диапазона зеленых оттенков
        lower_green = np.array([0, 70, 50], dtype=np.uint8)
        upper_green = np.array([10, 255, 255], dtype=np.uint8)
        # Создание маски зеленых оттенков
        mask = cv2.inRange(hsv, lower_green, upper_green)
        # cv2.imshow('Mask', mask)
        and1 = cv2.bitwise_and(img_asis, img_asis, mask=mask)


        # Преобразование изображения в оттенки серого
        gray = cv2.cvtColor(and1, cv2.COLOR_BGR2GRAY)

        eroded = cv2.Canny(gray, 100, 200)
        # cv2.imshow("eroded", eroded)

        # Создание структурного элемента для операций морфологии
        kernel = np.ones((5, 5), np.uint8)

        # Удаление горизонтальных линий
        dilated = cv2.dilate(eroded, kernel, iterations=1)
        edge = cv2.erode(dilated, kernel, iterations=1)

        # Отображение результата
        #cv2.imshow('Edge', edge)

        rho = 1
        # 1 degree
        theta = (np.pi/180) * 1
        threshold = 50
        min_line_length = 120
        max_line_gap = 10
        counter = 0
        max_angle = 1000
        min_angle = 1000
        x1_min = 100
        x1_max = 100
        y1_min = 100
        y1_max = 100
        lines=cv2.HoughLinesP(edge, rho, theta, threshold, np.array([]),
                             minLineLength=min_line_length, maxLineGap=max_line_gap)

        for line in lines:
            for x1,y1,x2,y2 in line:
                if y2 - y1 != 0:
                    y_size = y2-y1
                    tan = (x2 - x1) / (y2 - y1)
                    angle = math.atan(tan)
                    angle = math.degrees(angle)

                    # Фильтруем линии по длине
                    if y_size > 100:
                        if max_angle == 1000:
                            max_angle = angle
                            min_angle = angle
                        else:
                            print('1 angle grad ', angle)
                            print('max_angle ', max_angle)
                            if max_angle < angle:
                                max_angle = angle
                                x1_max = x1
                                y1_max = y1
                            print('2 angle grad ', angle)
                            print('min_angle ', min_angle)
                            if min_angle > angle:
                                min_angle = angle
                                x1_min = x1
                                y1_min = y1
                            if max_angle == angle:
                                x1_max = x1
                                y1_max = y1

                        print("Angle = ",  angle)
                        print("Y = ",  y_size)
                        print()
                        counter += 1

        print(counter)

        x0 = 50
        angle_izo = angle
        if angle > 0:
            x1_min = int(x1_min - (y1_min * math.tan(math.radians(min_angle))))
            x1_max = int(x1_max - (y1_max * math.tan(math.radians(max_angle))))
            if(x1_max - x1_min) != 0:
                angle_coef = (max_angle-min_angle)/(x1_max - x1_min)
            else:
                angle_coef = 1


        # Формируем путь к новому файлу
        new_file_path = os.path.join(source_folder + '/images/', image_file)

        line = 0
        num = 1
        while(1):
            img2 = copy.copy(img)
            if flag_Q == 1:
                img2 = cv2.flip(img, 1)
            if angle > 0:
                angle_izo = min_angle + angle_coef*(-x1_min + x0)

            xn = int(math.tan(math.radians(angle_izo)) * img2.shape[0] + x0)
            if line == 0:
                x0_line0 = x0
                xn_line0 = xn
                cv2.line(img2, (x0, 0), (xn, img2.shape[0]-1), [0,255,255], 2)
            else:
                cv2.line(img2, (x0_line0, 0), (xn_line0, img2.shape[0]-1), [255,0,0], 2)
                cv2.line(img2, (x0, 0), (xn, img2.shape[0]-1), [0,0,255], 2)
            cv2.imshow('output', img2)

            key = cv2.waitKey(100)
            if key == ord('a'):
                x0 = x0 - 1
            elif key == ord('d'):
                x0 = x0 + 1
            elif key == ord('w'):
                num = num + 1
                break
            elif key == ord('e'):
                line = 1
            elif key == ord('s'):
                if flag_Q == 1:
                    img2 = cv2.flip(img2, 1)
                print('qwert',new_file_path)
                cv2.imwrite(new_file_path, img2)
                break

        cv2.destroyAllWindows()
