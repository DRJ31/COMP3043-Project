from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db.models import Q
from main.models import Post
from datetime import datetime, timedelta

# Create your views here.


def index(request):
    data = []
    for info in Post.objects.filter(date__range=[datetime.now() - timedelta(days=7), datetime.now()]).order_by('-date'):
        data.append(info)
    return render(request, 'index.html', {
        'data': data,
        'length': len(data)
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
    status = request.GET['status']
    data = Post.objects.filter(status__in=status).order_by("-date")
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


def register(request):
    return render(request, 'register.html')

def profile(request):
    return render(request, 'profile.html')
