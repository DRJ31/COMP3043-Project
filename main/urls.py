from django.urls import path, include
from django.views.i18n import set_language
from django.conf.urls.i18n import i18n_patterns
from . import views

urlpatterns = [
    path('', views.index),
    path('detail/<id>/', views.show_detail),
    path('search/', views.search),
    path('i18n/', include('django.conf.urls.i18n')),
]

# urlpatterns += i18n_patterns(
#     # path('', views.index, name="index"),
#     path('detail/<id>/', views.show_detail, name="detail"),
# )