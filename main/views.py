from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.db.models import Q
from main.models import Post, PostEncrypt
from datetime import datetime, timedelta

# Create your views here.


def index(request):
    data = []
    for info in Post.objects.filter(status__in=['L', 'F'], date__range=[datetime.now() - timedelta(days=7), datetime.now()]).order_by('-date'):
        data.append(info)
    return render(request, 'index.html', {
        'data': data,
        'length': len(data)
    })


def show_detail(request, id):
    data = Post.objects.get(pid=id)
    encrypt = data.postencrypt.encrypt
    return render(request, 'detail.html', {
        "data": data,
        "encrypt": encrypt
    })


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

def new_post(request):
    # Other information of post form
    name = request.POST['objectName']
    location = request.POST['location']
    description = request.POST['description']
    contact = request.POST['contact']
    poster = request.user.username
    date = datetime.now()
    status = request.POST['status-type']

    if not request.POST.get('default'):
        # Picture upload
        img = request.FILES['photo']
        filetype = img.content_type.split("/")[1]
        if filetype == "jpeg":
            filetype = "jpg"
        filename = "%s-%s-%s.%s" % (name, poster, date.strftime("%Y-%m-%d"), filetype)
        encryptString = filename
        path = "static/img/%s" % (filename)
        with open(path, 'wb+') as destination:
            for chunk in img.chunks():
                destination.write(chunk)
    else:
        filename = "saber.jpg"
        encryptString = "%s-%s-%s" % (name, poster, date.strftime("%Y-%m-%d"))
    # Insert into database
    post_detail = Post(
        poster=poster,
        description=description,
        status=status,
        pic=filename,
        date=date,
        name=name,
        location=location,
        contact=contact
    )
    post_detail.save()
    eid = Post.objects.get(pid=post_detail.pid)
    encrypt = PostEncrypt(id=eid, encrypt=make_password(encryptString, "", 'pbkdf2_sha256'))
    encrypt.save()
    return HttpResponse("success")


def delete_post(request, id):
    pid = PostEncrypt.objects.get(encrypt=id).id
    Post.objects.get(pid=pid).delete()
    return HttpResponse("success")