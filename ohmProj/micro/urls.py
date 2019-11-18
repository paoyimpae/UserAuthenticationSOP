from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('logout/', views.my_logout, name='logout'),
    path('login/', views.my_login, name='login')
]