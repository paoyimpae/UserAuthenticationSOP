from django.conf.urls import url
from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from . import forms
from .views import user_detail, change_password, confirmation, invalid

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('logout/', views.my_logout, name='logout'),
    path('login/', LoginView.as_view(authentication_form=forms.OTPAuthenticationForm), name='login'),
    path('edit_profile/', views.edit_profile, name='edit'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('user_detail/', user_detail, name='user_detail'),
    path('password/', change_password, name='change_password'),
    path('confirmation/', confirmation, name='confirmation'),
    path('invalid/', invalid, name='invalid'),
]