import cv2
import numpy
from math import ceil

## ввод текста для строки
#message = input()
message = 'Hello, World!' ##Test message

## параметры видео
width, height = 100,100
duration = 72  ## 3 секунды с частотой 24 кадра/сек

s = ceil((len(message)*20) / duration) ##сдвиг строки между кадрами

##сохранение видео
out = cv2.VideoWriter("ticker.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 24, (width, height))

# кадр с черным фоном
frame = numpy.zeros((height, width, 3), dtype=numpy.uint8)

# начальные координаты для бегущей строки
x, y = width, height // 2

# параметры шрифта
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
font_thickness = 2
font_color = (255, 255, 255) 

for t in range(duration):
    # Заливка кадра
    frame.fill(0)

    ##координаты текста в новом фрейме
    x -= s  

    cv2.putText(frame, message, (x, y), font, font_scale, font_color, font_thickness)

    out.write(frame)

# закрываем потоки
out.release()