from django.shortcuts import render
from createvideo.models import Ticker
from django import forms
from django.http import FileResponse

# Create your views here.
import cv2
import numpy
from math import ceil

def create_ticker(ticker):
    ## параметры видео
    width, height = ticker.width,ticker.height
    message = ticker.text
    duration = ticker.duration * 24 ##перевод секунд в кадры при 24 кадрах/сек
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


class TickerForm(forms.ModelForm):
    class Meta:
        model = Ticker
        fields = ['text', 'width', 'height', 'duration']
        widgets = {
            'text': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Текст строки'}), 
        }

# def main_page(request):
#     if request.method == "POST":
#         data = request.POST

#         ##запись в историю запросов
#         w=int(data['width'])
#         h=int(data['height'])
#         d=int(data['duration'])
#         new_ticker=Ticker(text=data['text'],width=w,height=h,duration=d)
#         new_ticker.save()

#         create_ticker(new_ticker)
        
#         # return HttpResponse(f"Видео строки {new_ticker.text} было создано.")
#         return FileResponse(open('ticker.mp4','rb'), as_attachment=True)
#     else:
#         form = TickerForm()
#         return render(request, 'index.html', {
#             'tickerform': form,
#             })
        
def main_page(request):
    if request.method == "GET":
        if request.GET.get('text'):
            data = request.GET
            ##запись в историю запросов
            if request.GET.get('width'):
                w=int(data['width'])
            else:
                w=100
            if request.GET.get('height'):
                h=int(data['height'])
            else:
                h=100
            if request.GET.get('duration'):
                d=int(data['duration'])
            else:
                d=3
            new_ticker=Ticker(text=data['text'],width=w,height=h,duration=d)
            if request.GET.get('save') != "no":
                new_ticker.save()
                create_ticker(new_ticker)          
        
            # return HttpResponse(f"Видео строки {new_ticker.text} было создано.")
            return FileResponse(open('ticker.mp4','rb'), as_attachment=True)
        else:
            form = TickerForm()
            return render(request, 'index.html', {
                'tickerform': form,
                })       

def history(request):
    data = Ticker.objects.all()
    return render(request,"history.html", {"tickers": data})