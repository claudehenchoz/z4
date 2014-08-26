from django.shortcuts import render
from django.db.models import Count
from buzz.models import BuzzItem
import time


def index(request):
    latest_buzz_list = BuzzItem.objects.order_by('-date')[:50]
    context = {'latest_buzz_list': latest_buzz_list,
               'isindex': True,
               'source': 'all',
               'time':time.strftime("%Y-%m-%d %H:%M")}
    return render(request, 'buzz/index.html', context)

def bysource(request, mysource):
    latest_buzz_list = BuzzItem.objects.filter(source=mysource).order_by('-date')[:50]
    context = {'latest_buzz_list': latest_buzz_list,
               'source': mysource,
               'time':time.strftime("%Y-%m-%d %H:%M")}
    return render(request, 'buzz/index.html', context)
