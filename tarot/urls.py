from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^$', views.p_tarot_home, name='p_tarot_home'),
    url(r'^help/$', views.p_tarot_help, name='p_tarot_help'),

    url(r'^partie/select/$', login_required(views.TarotPartieSelectView.as_view()), name='v_tarot_partie_select'),
    url(r'^partie/folder/(.+)/$', login_required(views.f_tarot_partie_folder), name='f_tarot_partie_folder'),
    url(r'^partie/create/$', login_required(views.f_tarot_partie_create), name='f_tarot_partie_create'),
    url(r'^partie/update/(.+)/$', login_required(views.f_tarot_partie_update), name='f_tarot_partie_update'),
    url(r'^partie/delete/(.+)$', login_required(views.f_tarot_partie_delete), name='f_tarot_partie_delete'),


    url(r'^participant/select/$', login_required(views.TarotParticipantSelectView.as_view()), name='v_tarot_participant_select'),
    url(r'^participant/list/$', login_required(views.TarotParticipantListView.as_view()), name='v_tarot_participant_list'),
    url(r'^participant/join/(.+)/$', login_required(views.v_tarot_participant_join), name='v_tarot_participant_join'),
    url(r'^participant/update/(.+)/(.+)/$', login_required(views.f_tarot_participant_update), name='f_tarot_participant_update'),
    url(r'^participant/order/(.+)/(.+)/$', login_required(views.v_tarot_participant_order), name='v_tarot_participant_order'),
    url(r'^joueur/create/$', login_required(views.f_tarot_joueur_create), name='f_tarot_joueur_create'),
    url(r'^joueur/update/(.+)/$', login_required(views.f_tarot_joueur_update), name='f_tarot_joueur_update'),
    url(r'^joueur/delete/(.+)$', login_required(views.f_tarot_joueur_delete), name='f_tarot_joueur_delete'),

    url(r'^jeu/list/(?P<page>.+)/$', login_required(views.TarotJeuListView.as_view()), name='v_tarot_jeu_list'),
    url(r'^jeu/sort/(?P<page>.+)/(?P<sort>.+)/$', login_required(views.TarotJeuListView.as_view()), name='v_tarot_jeu_sort'),
    url(r'^jeu/add/$', login_required(views.f_tarot_jeu_add), name='f_tarot_jeu_add'),
    url(r'^jeu/create/(.+)/$', login_required(views.f_tarot_jeu_create), name='f_tarot_jeu_create'),
    url(r'^jeu/compute/(.+)/$', login_required(views.f_tarot_jeu_compute), name='f_tarot_jeu_compute'),
    url(r'^jeu/pari/(.+)/$', login_required(views.f_tarot_jeu_pari), name='f_tarot_jeu_pari'),
    url(r'^jeu/real/(.+)/$', login_required(views.f_tarot_jeu_real), name='f_tarot_jeu_real'),
    url(r'^jeu/partenaire/(.+)/(.+)/$', login_required(views.f_tarot_jeu_partenaire), name='f_tarot_jeu_partenaire'),
    url(r'^jeu/prime/(.+)/$', login_required(views.f_tarot_jeu_prime), name='f_tarot_jeu_prime'),
]
