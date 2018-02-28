from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.p_whist_home, name='p_whist_home'),
    url(r'^help/$', views.p_whist_help, name='p_whist_help'),

    url(r'^partie/select/$', views.WhistPartieSelectView.as_view(), name='v_partie_select'),
    url(r'^partie/folder/(.+)/$', views.f_partie_folder, name='f_partie_folder'),
    url(r'^partie/create/$', views.f_partie_create, name='f_partie_create'),
    url(r'^partie/update/(.+)/$', views.f_partie_update, name='f_partie_update'),
    url(r'^partie/delete/(.+)$', views.f_partie_delete, name='f_partie_delete'),


    url(r'^participant/select/$', views.WhistParticipantSelectView.as_view(), name='v_participant_select'),
    url(r'^participant/list/$', views.WhistParticipantListView.as_view(), name='v_participant_list'),
    url(r'^participant/join/(.+)/$', views.v_participant_join, name='v_participant_join'),
    url(r'^participant/update/(.+)/(.+)/$', views.f_participant_update, name='f_participant_update'),
    url(r'^participant/order/(.+)/(.+)/$', views.v_participant_order, name='v_participant_order'),
    url(r'^joueur/create/$', views.f_joueur_create, name='f_joueur_create'),
    url(r'^joueur/update/(.+)/$', views.f_joueur_update, name='f_joueur_update'),
    url(r'^joueur/delete/(.+)$', views.f_joueur_delete, name='f_joueur_delete'),

    url(r'^jeu/list/(?P<page>.+)/$', views.WhistJeuListView.as_view(), name='v_jeu_list'),
    url(r'^jeu/sort/(?P<page>.+)/(?P<sort>.+)/$', views.WhistJeuListView.as_view(), name='v_jeu_sort'),
    url(r'^jeu/create/(.+)/$', views.f_jeu_create, name='f_jeu_create'),
    url(r'^jeu/compute/(.+)/$', views.f_jeu_compute, name='f_jeu_compute'),
    url(r'^jeu/pari/(.+)/$', views.f_jeu_pari, name='f_jeu_pari'),
    url(r'^jeu/real/(.+)/$', views.f_jeu_real, name='f_jeu_real'),

]
