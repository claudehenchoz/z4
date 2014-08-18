from django.shortcuts import render

from django.http import HttpResponse

from buzz.models import BuzzItem

def index(request):

    latest_buzz_list = BuzzItem.objects.order_by('-date')[:10]

    context = {'latest_buzz_list': latest_buzz_list}
    return render(request, 'buzz/index.html', context)

    #output = ', '.join([b.title for b in latest_buzz_list])
    #return HttpResponse(output)
