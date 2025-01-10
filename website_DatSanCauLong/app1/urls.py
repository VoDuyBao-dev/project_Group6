from django.contrib import admin
from django.urls import path, include
from . import views
from .views import GetAllUserAPIView

urlpatterns = [
    path('', views.home, name= 'home'),
    path('base/', views.base, name= 'base'),
    path('getuser/', views.GetAllUserAPIView.as_view(), name= 'getuser'),
]
