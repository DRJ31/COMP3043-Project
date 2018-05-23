from django.urls import path
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
    path('settings/', views.profile), # TODO
    path('newpost/', views.new_post),
    path('delete/<id>', views.delete_post)
]
