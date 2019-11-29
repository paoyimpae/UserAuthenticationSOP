from django.conf.urls import url
from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from . import forms
from .views import user_detail, change_password, confirmation, invalid

from .views import UserAll, UserCreate, UserChoose, UserUpdateOrDelete

from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('user', UserViewSet)

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
    # path('get_data/', get_data, name='get_data'),
    
    ### API Part : For Admin Only ###
    path('api/user/all', UserAll.as_view(), name="UserAll"),
    path('api/user/<int:id>', UserChoose.as_view(), name="UserChoose"),
    path('api/user/create', UserCreate.as_view(), name="UserCreate"),
    path('api/user/update/<int:id>', UserUpdateOrDelete.as_view(), name="UserUpdateOrDelete"),
]