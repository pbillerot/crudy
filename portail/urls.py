from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.p_portail_home, name='p_portail_home'),
    url(r'^help/$', views.p_portail_help, name='p_portail_help'),
]
