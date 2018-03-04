from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.p_portail_home, name='p_portail_home'),
    url(r'^login$', views.f_portail_login, name='p_portail_login'),
    url(r'^logout$', views.f_portail_logout, name='p_portail_logout'),
    url(r'^help/$', views.p_portail_help, name='p_portail_help'),
]
