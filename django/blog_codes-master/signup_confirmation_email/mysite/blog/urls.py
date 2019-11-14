from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name='home'),
    # url(r'^login/$', auth_views.LoginView.as_view(template_name='home.html'),
    #     {'next_page': 'home'}, name='login'),
    # url(r'^logout/$', views.logout,
    #     {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('login/', auth_views.LoginView.as_view(template_name='home.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='home.html'), name='logout'),
]
