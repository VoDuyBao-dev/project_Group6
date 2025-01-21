from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('signin/', views.Sign_in, name= 'Sign_in'),
    path('signup/', views.Sign_up, name= 'Sign_up'),
    path('forgotpassword/', views.Forgot_password, name= 'Forgot_password'),
    path('newpassword/', views.New_password, name= 'New_password'),
]
