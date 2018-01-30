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

    url(r'^joueur/list/$', views.WhistJoueurListView.as_view(), name='joueur_list'),
    url(r'^joueur/create/$', views.joueur_create, name='joueur_create'),
    url(r'^joueur/update/(.+)/$', views.joueur_update, name='joueur_update'),
    url(r'^joueur/delete/$', views.joueur_delete, name='joueur_delete'),

    url(r'^participant/list/$', views.WhistParticipantListView.as_view(), name='participant_list'),
    url(r'^participant/create/$', views.participant_create, name='participant_create'),
    url(r'^participant/update/(.+)/$', views.participant_update, name='participant_update'),
    url(r'^participant/delete/$', views.participant_delete, name='participant_delete'),

    url(r'^jeu/list/$', views.WhistJeuListView.as_view(), name='jeu_list'),

    url(r'^proto/$', views.whist_proto, name='whist_proto')
]
