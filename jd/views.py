from django.shortcuts import render

from jd.models import Club


def index(request):
    return render(request, 'jd/index.html')


def club_list(request):
    clubs = Club.objects.order_by('deadline')
    context = {'list': clubs}
    return render(request, 'jd/club_list.html', context)
