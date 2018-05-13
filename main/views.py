from django.shortcuts import render
from main.models import Post, Bulletin
from django.http import HttpResponse
from django.db.models import Q
from datetime import datetime, timedelta

# Create your views here.


def index(request):
    data = []
    bulletin = Bulletin.objects.get(status='Y').content
    for info in Post.objects.filter(date__range=[datetime.now() - timedelta(days=7), datetime.now()]).order_by('-date'):
        data.append(info)
    return render(request, 'index.html', {
        'data': data,
        'bulletin': bulletin,
        'length': len(data),
        'Language': request.LANGUAGE_CODE
    })


def show_detail(request, id):
    data = Post.objects.get(pid=id)
    return render(request, 'detail.html', {'data': data})


def lost_found(request, type):
    status = 'L' if type == 'lost' else 'F'
    data = []
    for info in Post.objects.get(status='L'):
        data.append(info)
    return render(request, 'index.html', {})


def search(request):
    result = []
    key = request.GET['key']
    date = request.GET['date']
    location = request.GET['location']
    status = request.GET['status']
    data = Post.objects.filter(status__in=status).order_by("-date")
    if len(location) > 2:
        data = data.filter(locationrange__in=location)
    if len(key) > 0:
        data = data.filter(Q(name__icontains=key) | Q(location__icontains=key) | Q(poster__icontains=key))
    if int(date) == 0:
        data = data.filter(date__range=[datetime.now() - timedelta(days=7), datetime.now()]).order_by("-date")
    elif int(date) == 1:
        data = data.filter(date__range=[datetime.now() - timedelta(days=30), datetime.now()]).order_by("-date")
    for info in data:
        result.append([info.name, info.status, info.location, info.date.strftime("%Y-%m-%d"), info.poster, info.pid])
    string = "["
    for info in result:
        string += str(info) + ','
    string = string[:-1] + "]"
    return HttpResponse(string)