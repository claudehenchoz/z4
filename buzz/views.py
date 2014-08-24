from django.shortcuts import render
from buzz.models import BuzzItem
import time


def index(request):
    latest_buzz_list = BuzzItem.objects.order_by('-date')[:50]
    context = {'latest_buzz_list': latest_buzz_list,
               'time':time.strftime("%Y-%m-%d %H:%M")}
    return render(request, 'buzz/index.html', context)


def tagi(request):
    latest_buzz_list = BuzzItem.objects.filter(source='tagesanzeiger.ch').order_by('-date')[:50]
    context = {'latest_buzz_list': latest_buzz_list,
               'source': 'tagi',
               'time':time.strftime("%Y-%m-%d %H:%M")}
    return render(request, 'buzz/index.html', context)

def woz(request):
    latest_buzz_list = BuzzItem.objects.filter(source='woz.ch').order_by('-date')[:50]
    context = {'latest_buzz_list': latest_buzz_list,
               'source': 'woz',
               'time':time.strftime("%Y-%m-%d %H:%M")}
    return render(request, 'buzz/index.html', context)

def rps(request):
    latest_buzz_list = BuzzItem.objects.filter(source='rockpapershotgun.com').order_by('-date')[:50]
    context = {'latest_buzz_list': latest_buzz_list,
               'source': 'rps',
               'time':time.strftime("%Y-%m-%d %H:%M")}
    return render(request, 'buzz/index.html', context)
