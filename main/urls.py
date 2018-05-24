from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index),
    path('detail/<id>/', views.show_detail),
    path('search/', views.search),
    path('login/', auth_views.LoginView.as_view(template_name='signin.html')),
    path('logout/', auth_views.LogoutView.as_view(next_page='/')),
    path('register/', views.register),
    path('profile/', views.profile),
    path('settings/', views.settings),
    path('newpost/', views.new_post),
    re_path(r'^delete/(?P<id>[0-9A-Za-z_$\/+=]+)/$', views.delete_post),
    path('update/<id>/', views.update_post),
    path('allpost/', views.all_post),
    path('getkey/', views.get_key),
    path('changenickname/', views.change_nickname),
    path('changepassword/', views.change_pass)
]
