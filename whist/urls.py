from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^$', views.p_whist_home, name='p_whist_home'),
    url(r'^help/$', views.p_whist_help, name='p_whist_help'),

    url(r'^partie/select/$', login_required(views.WhistPartieSelectView.as_view()), name='v_whist_partie_select'),
    url(r'^partie/folder/(.+)/$', login_required(views.f_whist_partie_folder), name='f_whist_partie_folder'),
    url(r'^partie/create/$', login_required(views.f_whist_partie_create), name='f_whist_partie_create'),
    url(r'^partie/update/(.+)/$', login_required(views.f_whist_partie_update), name='f_whist_partie_update'),
    url(r'^partie/delete/(.+)$', login_required(views.f_whist_partie_delete), name='f_whist_partie_delete'),

    url(r'^participant/select/$', views.folder_required(login_required(views.WhistParticipantSelectView.as_view())), name='v_whist_participant_select'),
    url(r'^participant/list/$', views.folder_required(login_required(views.WhistParticipantListView.as_view())), name='v_whist_participant_list'),
    url(r'^participant/join/(.+)/$', views.folder_required(login_required(views.v_whist_participant_join)), name='v_whist_participant_join'),
    url(r'^participant/update/(.+)/(.+)/$', views.folder_required(login_required(views.f_whist_participant_update)), name='f_whist_participant_update'),
    url(r'^participant/order/(.+)/(.+)/$', views.folder_required(login_required(views.v_whist_participant_order)), name='v_whist_participant_order'),
    url(r'^joueur/create/$', views.folder_required(login_required(views.f_whist_joueur_create)), name='f_whist_joueur_create'),
    url(r'^joueur/update/(.+)/$', views.folder_required(login_required(views.f_whist_joueur_update)), name='f_whist_joueur_update'),
    url(r'^joueur/delete/(.+)$', views.folder_required(login_required(views.f_whist_joueur_delete)), name='f_whist_joueur_delete'),

    url(r'^jeu/list/(?P<page>.+)/$', views.folder_required(login_required(views.WhistJeuListView.as_view())), name='v_whist_jeu_list'),
    url(r'^jeu/sort/(?P<page>.+)/(?P<sort>.+)/$', views.folder_required(login_required(views.WhistJeuListView.as_view())), name='v_whist_jeu_sort'),
    url(r'^jeu/create/(.+)/$', views.folder_required(login_required(views.f_whist_jeu_create)), name='f_whist_jeu_create'),
    url(r'^jeu/compute/(.+)/$', views.folder_required(login_required(views.f_whist_jeu_compute)), name='f_whist_jeu_compute'),
    url(r'^jeu/pari/(.+)/$', views.folder_required(login_required(views.f_whist_jeu_pari)), name='f_whist_jeu_pari'),
    url(r'^jeu/real/(.+)/$', views.folder_required(login_required(views.f_whist_jeu_real)), name='f_whist_jeu_real'),
    url(r'^jeu/participant/(?P<participant_id>.+)/$', views.folder_required(login_required(views.WhistJeuParticipantView.as_view())), name='v_whist_jeu_participant'),


]
