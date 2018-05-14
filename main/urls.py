from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('detail/<id>/', views.show_detail),
    path('search/', views.search),
    path('login/', views.login),
    path('register/', views.register)
]
