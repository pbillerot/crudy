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


    url(r'^participant/select/$', views.folder_required(login_required(views.TarotParticipantSelectView.as_view())), name='v_tarot_participant_select'),
    url(r'^participant/list/$', views.folder_required(login_required(views.TarotParticipantListView.as_view())), name='v_tarot_participant_list'),
    url(r'^participant/join/(.+)/$', views.folder_required(login_required(views.v_tarot_participant_join)), name='v_tarot_participant_join'),
    url(r'^participant/update/(.+)/(.+)/$', views.folder_required(login_required(views.f_tarot_participant_update)), name='f_tarot_participant_update'),
    url(r'^participant/order/(.+)/(.+)/$', views.folder_required(login_required(views.v_tarot_participant_order)), name='v_tarot_participant_order'),
    url(r'^joueur/create/$', views.folder_required(login_required(views.f_tarot_joueur_create)), name='f_tarot_joueur_create'),
    url(r'^joueur/update/(.+)/$', views.folder_required(login_required(views.f_tarot_joueur_update)), name='f_tarot_joueur_update'),
    url(r'^joueur/delete/(.+)$', views.folder_required(login_required(views.f_tarot_joueur_delete)), name='f_tarot_joueur_delete'),

    url(r'^jeu/list/(?P<page>.+)/$', views.folder_required(login_required(views.TarotJeuListView.as_view())), name='v_tarot_jeu_list'),
    url(r'^jeu/sort/(?P<page>.+)/(?P<sort>.+)/$', views.folder_required(login_required(views.TarotJeuListView.as_view())), name='v_tarot_jeu_sort'),
    url(r'^jeu/add/$', views.folder_required(login_required(views.f_tarot_jeu_add)), name='f_tarot_jeu_add'),
    url(r'^jeu/create/(.+)/$', views.folder_required(login_required(views.f_tarot_jeu_create)), name='f_tarot_jeu_create'),
    url(r'^jeu/compute/(.+)/$', views.folder_required(login_required(views.f_tarot_jeu_compute)), name='f_tarot_jeu_compute'),
    url(r'^jeu/pari/(.+)/$', views.folder_required(login_required(views.f_tarot_jeu_pari)), name='f_tarot_jeu_pari'),
    url(r'^jeu/real/(.+)/$', views.folder_required(login_required(views.f_tarot_jeu_real)), name='f_tarot_jeu_real'),
    url(r'^jeu/partenaire/(.+)/(.+)/$', views.folder_required(login_required(views.f_tarot_jeu_partenaire)), name='f_tarot_jeu_partenaire'),
    url(r'^jeu/prime/(.+)/$', views.folder_required(login_required(views.f_tarot_jeu_prime)), name='f_tarot_jeu_prime'),
    url(r'^jeu/participant/(?P<participant_id>.+)/$', views.folder_required(login_required(views.TarotJeuParticipantView.as_view())), name='v_tarot_jeu_participant'),
]
