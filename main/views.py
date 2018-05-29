from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Q
from main.models import Post, PostEncrypt, AuthUser
from datetime import datetime, timedelta
import os
import json

# Create your views here.


def index(request): # Index page
    data = []
    results = Post.objects.filter(date__range=[datetime.now() - timedelta(days=7), datetime.now()]).order_by('-date')
    for info in results[0:20]:
        data.append(info)
    return render(request, 'index.html', {
        'data': data,
        'length': len(results)
    })


def all_post(request): # Show all the post of user
    data = []
    all = Post.objects.all().order_by('-date')[0:20]
    if request.user.is_staff == 0:
        all = Post.objects.filter(poster=request.user.username).order_by('-date')[0:20]
    for info in all:
        data.append(info)
    return render(request, 'allpost.html', {
        'data': data,
    })

def get_more(request):
    data = []
    start = int(request.GET['start'])
    all = Post.objects.all().order_by('-date')[start:start + 20]
    if request.user.is_staff == 0:
        all = Post.objects.filter(poster=request.user.username).order_by('-date')[start:start + 20]
    for info in all:
        data.append([info.name, info.status, info.location, info.date.strftime("%Y-%m-%d"), info.poster, info.pid])
    result = json.dumps({'result': data})
    return HttpResponse(result)


def show_detail(request, id): # Detail page
    try:
        data = Post.objects.get(pid=id)
    except:
        raise Http404
    encrypt = data.postencrypt.encrypt
    return render(request, 'detail.html', {
        "data": data,
        "encrypt": encrypt,
        "ID": id
    })


def search(request):
    result = []
    start = int(request.GET['start'])
    end = int(request.GET['end'])
    key = request.GET['key']
    date = request.GET['date']
    status = request.GET['status']
    length = int(request.GET['needLength'])
    if len(key) > 0:
        if int(date) == 0:
            data = Post.objects.\
                filter(status__in=status).\
                filter(Q(name__icontains=key) | Q(location__icontains=key) | Q(poster__icontains=key)). \
                filter(date__range=[datetime.now() - timedelta(days=7), datetime.now()]).order_by("-date")[start:end]
            if length == 1:
                length = len(Post.objects.only('pid').
                    filter(status__in=status).
                    filter(Q(name__icontains=key) | Q(location__icontains=key) | Q(poster__icontains=key)). \
                    filter(date__range=[datetime.now() - timedelta(days=7), datetime.now()]))
        elif int(date) == 1:
            data = Post.objects.\
                filter(status__in=status).\
                filter(Q(name__icontains=key) | Q(location__icontains=key) | Q(poster__icontains=key)). \
                filter(date__range=[datetime.now() - timedelta(days=30), datetime.now()]).order_by("-date")[start:end]
            if length == 1:
                length = len(Post.objects.only('pid').
                    filter(status__in=status).
                    filter(Q(name__icontains=key) | Q(location__icontains=key) | Q(poster__icontains=key)). \
                    filter(date__range=[datetime.now() - timedelta(days=30), datetime.now()]))
        else:
            data = Post.objects. \
                filter(status__in=status). \
                filter(Q(name__icontains=key) | Q(location__icontains=key) | Q(poster__icontains=key)).order_by("-date")[start:end]
            if length == 1:
                length = len(Post.objects.only('pid').
                    filter(status__in=status).
                    filter(Q(name__icontains=key) | Q(location__icontains=key) | Q(poster__icontains=key)))
    else:
        if int(date) == 0:
            data = Post.objects.\
                filter(status__in=status).\
                filter(date__range=[datetime.now() - timedelta(days=7), datetime.now()]).order_by("-date")[start:end]
            if length == 1:
                length = len(Post.objects.only('pid').
                    filter(status__in=status).
                    filter(date__range=[datetime.now() - timedelta(days=7), datetime.now()]))
        elif int(date) == 1:
            data = Post.objects.\
                filter(status__in=status).\
                filter(date__range=[datetime.now() - timedelta(days=30), datetime.now()]).order_by("-date")[start:end]
            if length == 1:
                length = len(Post.objects.only('pid').
                    filter(status__in=status).
                    filter(date__range=[datetime.now() - timedelta(days=30), datetime.now()]))
        else:
            data = Post.objects.filter(status__in=status).order_by("-date")[start:end]
            if length == 1:
                length = len(Post.objects.only('pid').filter(status__in=status))
    for info in data:
        result.append([info.name, info.status, info.location, info.date.strftime("%Y-%m-%d"), info.poster, info.pid])
    results = json.dumps({'result': result, 'length': length})
    return HttpResponse(results)


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        username = request.POST["username"]
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm"]
        email = request.POST["email"]

        # A second check here to prevent mismatch password confirmation
        if password != confirm_password:
            return render(request, 'register.html', {"error": "2 Passwords do not match"})

        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_staff=False,
            is_superuser=False
        )

        user.set_password(password) # Take care of hashing
        user.save()

        # Jump to Login View then
        # TODO: Prompt
        return HttpResponseRedirect('/login/')

def profile(request):
    return render(request, 'profile.html')

def settings(request):
    return render(request, 'settings.html')


def new_post(request): # Insert new post to database
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
        filename = "default.jpg"
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


def delete_post(request, id): # Delete the chosen post
    encryptObj = PostEncrypt.objects.get(encrypt=id)
    name = encryptObj.id.poster
    user = request.user.username
    if name != user and request.user.is_staff == 0:
        return render(request, 'validate.html', {
            'auth': False
        })
    if encryptObj.id.pic != "default.jpg" and os.path.isfile('static/img/%s' % (encryptObj.id.pic)):
        os.remove('static/img/%s' % (encryptObj.id.pic))
    Post.objects.get(pid=encryptObj.id.pid).delete()
    return render(request, 'validate.html', {
        'auth': True,
        'path': '/allpost',
        'msg': 'You have deleted your post'
    })


def update_post(request, id):
    obj = Post.objects.get(pid=id)
    # Other information of post form
    name = request.POST['objectName']
    obj.name = name
    obj.location = request.POST['location']
    obj.description = request.POST['description']
    obj.contact = request.POST['contact']
    poster = obj.poster
    date = datetime.now()
    oldFile = obj.pic
    if not request.POST.get('default'):
        # Picture upload
        img = request.FILES['photo']
        filetype = img.content_type.split("/")[1]
        if filetype == "jpeg":
            filetype = "jpg"
        filename = "%s-%s-%s.%s" % (name, poster, date.strftime("%Y-%m-%d"), filetype)
        os.remove('static/img/%s' % (oldFile))
        path = "static/img/%s" % (filename)
        with open(path, 'wb+') as destination:
            for chunk in img.chunks():
                destination.write(chunk)
        obj.pic = filename

    obj.save()
    return render(request, "validate.html", {
        'auth': True,
        'path': '/detail/' + id,
        'msg': 'You have updated your post'
    })


def get_key(request): # Get the delete key
    pid = request.POST['id']
    key = PostEncrypt.objects.get(id=pid).encrypt
    return HttpResponse(key)


class EmailAuthBackend(object): # Allow User to login by email
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def change_profile(request):
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    if request.user.is_authenticated:
        user = AuthUser.objects.get(username=request.user.username)
        user.first_name = firstname
        user.last_name = lastname
        user.save()
        return render(request, 'validate.html', {
            'auth': True,
            'path': '/profile',
            'msg': 'You have modified your nickname into %s %s' % (firstname, lastname)
        })
    return render(request, 'validate.html', {
        'auth': False
    })


def change_pass(request):
    old = request.POST['old']
    new = request.POST['new']
    if request.user.check_password(old):
        request.user.set_password(new)
        request.user.save()
        return render(request, "validate.html", {
            'auth': True,
            'path': '/',
            'msg': "You have changed your password"
        })
    return render(request, "validate.html", {
        'auth': True,
        'wrong_pass': True,
        'path': '/settings',
        'msg': "Wrong password! Please try again."
    })

