from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^$', views.whist_home, name='whist_home'),
    url(r'^whist/select/(.+)/$', views.whist_select, name='whist_select'),

    url(r'^partie/list/$', views.WhistPartieListView.as_view(), name='partie_list'),
    url(r'^partie/select/$', views.WhistPartieSelectView.as_view(), name='partie_select'),
    url(r'^partie/folder/(.+)/$', views.partie_folder, name='partie_folder'),
    url(r'^partie/create/$', views.partie_create, name='partie_create'),
    url(r'^partie/update/(.+)/$', views.partie_update, name='partie_update'),
    url(r'^partie/delete/$', views.partie_delete, name='partie_delete'),


    url(r'^participant/select/$', views.WhistParticipantSelectView.as_view(), name='participant_select'),
    url(r'^participant/list/$', views.WhistParticipantListView.as_view(), name='participant_list'),
    url(r'^participant/join/(.+)/$', views.participant_join, name='participant_join'),
    url(r'^participant/update/(.+)/(.+)/$', views.participant_update, name='participant_update'),
    url(r'^participant/order/(.+)/(.+)/$', views.participant_order, name='participant_order'),
    url(r'^joueur/create/$', views.joueur_create, name='joueur_create'),
    url(r'^joueur/update/(.+)/$', views.joueur_update, name='joueur_update'),

    url(r'^jeu/list/(?P<page>.+)/$', views.WhistJeuListView.as_view(), name='jeu_list'),
    url(r'^jeu/sort/(?P<page>.+)/(?P<sort>.+)/$', views.WhistJeuListView.as_view(), name='jeu_sort'),
    url(r'^jeu/create/(.+)/$', views.jeu_create, name='jeu_create'),
    url(r'^jeu/compute/(.+)/$', views.jeu_compute, name='jeu_compute'),
    url(r'^jeu/pari/(.+)/(.+)/$', views.jeu_pari, name='jeu_pari'),
    url(r'^jeu/real/(.+)/(.+)/$', views.jeu_real, name='jeu_real'),

    url(r'^proto/$', views.whist_proto, name='whist_proto')
]
