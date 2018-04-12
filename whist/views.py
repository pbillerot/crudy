# coding: utf-8
"""
    Traitement des VUES
"""
import re
import collections
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import resolve
from django.http import JsonResponse
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from crudy.crudy import Crudy
from crudy.views import CrudyListView
from . import forms
from .models import WhistPartie, WhistJoueur, WhistParticipant, WhistJeu

APP_NAME = "whist"

def folder_required(function):
    def wrap(request, *args, **kwargs):
        crudy = Crudy(request, APP_NAME)
        if crudy.folder_id:
            return function(request, *args, **kwargs)
        else:
            return redirect("v_whist_partie_select")
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

def p_whist_home(request):
    """ vue Home """
    return redirect("p_whist_help")

def p_whist_help(request):
    """ Guide """
    crudy = Crudy(request, APP_NAME)
    title = crudy.application.get("title")
    crudy.url_actions = []
    crudy.layout = "help"
    form = None
    return render(request, 'p_crudy_help.html', locals())

"""
    Gestion des parties
"""
class WhistPartieSelectView(CrudyListView):
    """ Sélection d'une partie """

    class Meta(CrudyListView.Options):
        application = APP_NAME
        model = WhistPartie

        title = "Sélection / ajout d'une partie"
        url_add = "f_whist_partie_create"
        url_folder = "f_whist_partie_folder"
        cols_ordered = ["name", "cartes"]
        cols = {
            "name": {"title":"Partie", "type":"button", "url":"f_whist_partie_update"},
            "cartes": {"title":"Nombre de cartes max", "type": "numeric"},
        }
        order_by = ('name',)
        url_view = "v_whist_partie_select"

    def get_queryset(self):
        """ queryset générique """
        self.objs = self.meta.model.objects.all().filter(owner=self.request.user.username)\
        .filter(**self.meta.filters)\
        .order_by(*self.meta.order_by)\
        .values(*self.meta.cols_ordered)
        return self.objs


def f_whist_partie_folder(request, record_id):
    """ Sélection d'une partie dans folder"""
    crudy = Crudy(request, APP_NAME)
    crudy.layout = "form"

    obj = get_object_or_404(WhistPartie, id=record_id)
    crudy.folder_id = obj.id
    crudy.folder_name = obj.name
    return redirect("v_whist_participant_select")

def f_whist_partie_create(request):
    """ Nouvelle partie """
    crudy = Crudy(request, APP_NAME)
    crudy.layout = "form"
    title = "Nouvelle Partie"
    model = WhistPartie
    crudy.message = ""
    if request.POST:
        form = forms.WhistPartieForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            post = form.save(commit=False)
            post.owner = request.user.username
            post.name = post.name.upper()
            post.save()
            return redirect("v_whist_partie_select")
    else:
        form = forms.WhistPartieForm(request=request)
    return render(request, 'f_crudy_form.html', locals())

def f_whist_partie_update(request, record_id):
    """ Modification d'une partie """
    crudy = Crudy(request, APP_NAME)
    crudy.layout = "form"
    title = "Modification d'une Partie"
    crudy.message = ""
    crudy.url_delete = "f_whist_partie_delete"
    obj = get_object_or_404(WhistPartie, id=record_id)
    model = WhistPartie
    form = forms.WhistPartieForm(request.POST or None, request=request, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("v_whist_partie_select")
    return render(request, "f_crudy_form.html", locals())

def f_whist_partie_delete(request, record_id):
    """ suppression de l'enregistrement """
    crudy = Crudy(request, APP_NAME)
    obj = get_object_or_404(WhistPartie, id=record_id)
    obj.delete()
    return redirect("v_whist_partie_select")

"""
    Gestion des participants
"""
class WhistParticipantSelectView(CrudyListView):
    """ Liste des participants """

    class Meta(CrudyListView.Options):
        application = APP_NAME
        model = WhistJoueur
        title = "Sélection des Participants"
        cols_ordered = ["pseudo"]
        cols = {
            "pseudo": {"title":"Nom du joueur", "type":"button", "url":"f_whist_joueur_update"},
        }
        order_by = ('pseudo',)
        url_add = "f_whist_joueur_create"
        url_join = "v_whist_participant_join"
        url_view = "v_whist_participant_select"
        help_page = "i_whist_participant_select.md"

    def get_queryset(self):
        """ queryset générique """
        crudy = Crudy(self.request, "whist")
        objs = self.meta.model.objects.all().filter(owner=self.request.user.username)\
        .filter(**self.meta.filters)\
        .order_by(*self.meta.order_by)\
        .values(*self.meta.cols_ordered)
        # Cochage des participants dans la liste des joueurs
        participants = WhistParticipant.objects.all().filter(partie__id__exact=crudy.folder_id)
        crudy.joined = []
        for obj in objs:
            for participant in participants:
                if participant.joueur_id == obj["id"]:
                    crudy.joined.append(obj["id"])
        self.objs = []
        # tri des colonnes
        for row in objs:
            ordered_dict = collections.OrderedDict()
            for col in self.meta.cols_ordered:
                ordered_dict[col] = row[col]  
            self.objs.append(ordered_dict) 

        return self.objs

def v_whist_participant_join(request, record_id):
    """ Création d'un participant à partir de la sélection dans la vue des joueurs """
    crudy = Crudy(request, APP_NAME)
    iid = int(record_id)

    if iid in crudy.joined:
        participant = WhistParticipant.objects.all().filter(partie_id=crudy.folder_id, joueur_id=iid)
        participant.delete()
        crudy.joined.remove(iid)
    else:
        participant = WhistParticipant(partie_id=crudy.folder_id, joueur_id=iid)
        participant.save()
        participant.compute_order()
        crudy.joined.append(iid)

    return redirect("v_whist_participant_select")

def f_whist_joueur_create(request):
    """ création d'un joueur """
    crudy = Crudy(request, APP_NAME)
    crudy.layout = "form"
    title = "Nouveau Joueur"
    crudy.message = ""
    model = WhistJoueur
    if request.POST:
        form = forms.WhistJoueurForm(request.POST, request=request)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user.username
            post.pseudo = post.pseudo.upper()
            post.save()
            return redirect("v_whist_participant_select")
    else:
        form = forms.WhistJoueurForm(request=request)
    return render(request, 'f_crudy_form.html', locals())

def f_whist_joueur_update(request, record_id):
    """ mise à jour d'un joueur """
    crudy = Crudy(request, APP_NAME)
    crudy.layout = "form"
    crudy.url_delete = "f_whist_joueur_delete"
    title = "Modification d'un Joueur"
    crudy.message = ""
    obj = get_object_or_404(WhistJoueur, id=record_id)
    form = forms.WhistJoueurForm(request.POST or None, instance=obj, request=request)
    if form.is_valid():
        form.save()
        return redirect("v_whist_participant_select")
    return render(request, "f_crudy_form.html", locals())

def f_whist_joueur_delete(request, record_id):
    """ suppression de l'enregistrement """
    crudy = Crudy(request, APP_NAME)
    obj = get_object_or_404(WhistJoueur, id=record_id)
    obj.delete()
    return redirect("v_whist_participant_select")

class WhistParticipantListView(CrudyListView):
    """ Tri des participants """

    class Meta(CrudyListView.Options):
        application = APP_NAME
        model = WhistParticipant
        title = "Ordre des Participants autour de la table"
        cols_ordered = ["joueur__pseudo", "donneur"]
        order_by = ('order', 'joueur__pseudo')
        url_order = "v_whist_participant_order"
        cols = {
            "order": {"title":"Nom du joueur", "hide": True},
            "joueur__pseudo": {"title":"Nom du joueur", "type": "button", "disabled": True},
            "donneur": {"title":"Donneur Initial", "type": "check", "url":"f_whist_participant_update"},
        }
        url_actions = [
            ("f_whist_jeu_create", "Initialiser les jeux")
        ]
        url_view = "v_whist_participant_list"
        help_page = "i_whist_participant_list.md"

    def get_queryset(self):
        """ queryset générique """
        crudy = Crudy(self.request, APP_NAME)
        objs = self.meta.model.objects.all()\
        .filter(partie_id=crudy.folder_id)\
        .order_by(*self.meta.order_by)\
        .values(*self.meta.cols_ordered)
        self.objs = []
        for row in objs:
            ordered_dict = collections.OrderedDict()
            for col in self.meta.cols_ordered:
                ordered_dict[col] = row[col]  
            self.objs.append(ordered_dict) 

        crudy.url_participant_update = 'f_whist_participant_update'
        crudy.action_param = 0
        if len(self.objs) == 0:
            self.meta.url_actions = []

        return self.objs

def f_whist_participant_update(request, record_id, checked):
    """ Mise à jour du donneur """
    crudy = Crudy(request, APP_NAME)

    participants = WhistParticipant.objects.all().filter(partie__id=crudy.folder_id)
    for participant in participants:
        if participant.id == int(record_id):
             participant.donneur = False if checked == "True" else True
        else:
            participant.donneur = False
        participant.save()

    return redirect("v_whist_participant_list")

def v_whist_participant_order(request, record_id, orientation):
    """ On remonte le joueur dans la liste """
    crudy = Crudy(request, APP_NAME)
    iid = int(record_id)

    participant = get_object_or_404(WhistParticipant, id=iid)
    participant.order += int(orientation) * 3
    participant.save()
    participant.compute_order()

    return redirect("v_whist_participant_list")

"""
    Gestion des jeux
"""
class WhistJeuListView(CrudyListView):
    """ Liste des jeux """

    class Meta(CrudyListView.Options):
        application = APP_NAME
        model = WhistJeu
        title = "Faites vos Jeux"
        cols_ordered = ["donneur", "participant__joueur__pseudo", 'participant__id', "medal", "score", "carte", "pari", "real", "points"]
        cols = {
            "donneur": {"title":"", "type": "position", "tooltip": "Le donneur pour ce tour"},
            "participant__joueur__pseudo": {"title":"Participant", "type":"medal", "url":"v_whist_jeu_participant"},
            "participant__id": {"hide": True},
            "medal": {"hide":True},
            "score": {"title":"Score", "type":"number", "sort":"v_whist_jeu_sort"},
            "carte": {"title":"Cartes", "type":"numeric"},
            "pari": {"title":"Paris", "type":"button", "url":"f_whist_jeu_pari"},
            "real": {"title":"Réalisé", "type":"button", "url":"f_whist_jeu_real"},
            "points": {"title":"Points", "type":"number"},
            "param": {"medal": "participant__id"},
        }

        url_view = "v_whist_jeu_list"

    def dispatch(self, request, *args, **kwargs):
        """ dispatch is called when the class instance loads """
        self.sort = kwargs.get('sort', None)
        self.page = kwargs.get('page')
        return super().dispatch(request, args, kwargs)

    def get_queryset(self):
        """ fournir les données à afficher dans la vue """
        crudy = Crudy(self.request, APP_NAME)
        # prise en compte de la colonne à trier en fonction de sort
        if self.sort == "score":
            crudy.sort = "score"

        if self.sort == "participant":
            crudy.sort = "participant"

        if crudy.sort == "score":
            order_by = ('jeu', '-score',)
        else:
            order_by = ('jeu', 'participant__order',)

        partie = get_object_or_404(WhistPartie, id=crudy.folder_id)
        crudy.modified = partie.modified

        objs = self.meta.model.objects.all()\
        .filter(participant__partie__id__exact=crudy.folder_id)\
        .order_by(*order_by)\
        .values(*self.meta.cols_ordered)

        # Tri des colonnes dans l'ordre de cols
        objects_list = []
        for row in objs:
            ordered_dict = collections.OrderedDict()
            for col in self.meta.cols_ordered:
                ordered_dict[col] = row[col]  
            objects_list.append(ordered_dict) 

        qparticipant = WhistParticipant.objects.all().filter(partie__id__exact=crudy.folder_id).count()
        self.objs = None
        if qparticipant > 0:
            self.paginator = Paginator(objects_list, qparticipant)
            
            self.objs = self.paginator.get_page(self.page)
            # comptage de nombre de plis demandés et réalisés
            qplis = 0
            qreal = 0
            qcarte = 0
            for obj in self.objs:
                qplis += obj["pari"]
                qreal += obj["real"]
                qcarte = obj["carte"]

            crudy.cartes = []
            for pp in range(1, self.paginator.num_pages + 1):
                if pp <= self.paginator.num_pages / 2:
                    crudy.cartes.append((pp, pp))
                else:
                    crudy.cartes.append((pp, self.paginator.num_pages - pp + 1))
            crudy.action_param = self.page
            crudy.jeu = int(self.page)
            partie = get_object_or_404(WhistPartie, id=crudy.folder_id)
            crudy.jeu_current = partie.jeu
            if int(crudy.jeu) > partie.jeu + 1:
                self.meta.url_actions = []
            if qreal != qcarte:
                self.meta.url_actions = []

            self.meta.cols["pari"]["subtitle"] = "%s / %s" % (qplis, qcarte)
            self.meta.cols["real"]["subtitle"] = "%s / %s" % (qreal, qcarte)
        else:
            self.meta.url_actions = []

        self.meta.url_actions = []
        if crudy.modified:
            self.meta.url_actions.append(("f_whist_jeu_compute", "Calculer les points"))

        crudy.url_sort = 'v_whist_jeu_sort'
        return self.objs

def f_whist_jeu_create(request, id):
    """ création des jeux (tours) de la partie """
    crudy = Crudy(request, APP_NAME)
    jeu = WhistJeu()
    jeu.create_jeux(crudy)

    return redirect("v_whist_jeu_list", 1)

def f_whist_jeu_compute(request, ijeu):
    """ Calcul des points du jeux, du score et du rang du joueur """
    crudy = Crudy(request, APP_NAME)
    jeux = WhistJeu.objects.all()\
    .filter(participant__partie__id=crudy.folder_id)\
    .order_by("jeu")
    score = {}
    for jeu in jeux:
        joueur_id = jeu.participant.joueur_id
        if jeu.jeu <= int(ijeu):
            if jeu.pari == jeu.real:
                jeu.points = 10 + 2 * jeu.pari
            else:
                jeu.points = -10
            score[joueur_id] = score.get(joueur_id, 0) + jeu.points
        jeu.score = score[joueur_id]
        jeu.save()
    # Attribution des médailles
    jeux = WhistJeu.objects.all()\
    .filter(participant__partie__id=crudy.folder_id)\
    .order_by("jeu", "-score")
    gold = 1000
    silver = 1000
    bronze = 1000
    rupt_jeu = 0
    last_pk = 0
    for jeu in jeux:
        if rupt_jeu != jeu.jeu:
            # changement de jeu
            rupt_jeu = jeu.jeu
            gold = 1000
            silver = 1000
            bronze = 1000
            # Médaille de chocolat
            if last_pk != 0:
                last_jeu = get_object_or_404(WhistJeu, pk=last_pk)
                last_jeu.medal = 9
                last_jeu.save()
        last_pk = jeu.pk
        jeu.medal = 0
        if gold == 1000:
            gold = jeu.score
            jeu.medal = 1
        elif gold == jeu.score:
            jeu.medal = 1
        elif silver == 1000:
            silver = jeu.score
            jeu.medal = 2
        elif silver == jeu.score:
            jeu.medal = 2
        elif bronze == 1000:
            bronze = jeu.score
            jeu.medal = 3
        elif bronze == jeu.score:
            jeu.medal = 3
        jeu.save()
    # Médaille de chocolat
    if last_pk != 0:
        last_jeu = get_object_or_404(WhistJeu, pk=last_pk)
        last_jeu.medal = 9
        last_jeu.save()
    # maj partie jeu en cours
    partie = get_object_or_404(WhistPartie, id=crudy.folder_id)
    if partie.jeu == int(ijeu) and int(ijeu) <= last_jeu.jeu:
        partie.jeu = int(ijeu) + 1
    partie.modified = False
    partie.save()

    return redirect("v_whist_jeu_list", partie.jeu)

def f_whist_jeu_pari(request, record_id):
    """ Saisie pari d'un joueur """
    crudy = Crudy(request, APP_NAME)
    obj = get_object_or_404(WhistJeu, id=record_id)
    title = "Pari de %s" % (obj.participant.joueur.pseudo.upper())
    crudy.message = "**%s**, Combien penses-tu faire de plis ?" % (obj.participant.joueur.pseudo.upper())
    form = forms.WhistJeuPariForm(request.POST or None, request=request, instance=obj)
    if form.is_valid():
        form.save()
        return redirect(crudy.url_view, obj.jeu)
    return render(request, "f_crudy_form.html", locals())

def f_whist_jeu_real(request, record_id):
    """ Saisie du réalisé 0 1 2 """
    crudy = Crudy(request, APP_NAME)
    obj = get_object_or_404(WhistJeu, id=record_id)
    title = "Réalisé de %s" % (obj.participant.joueur.pseudo.upper())
    if obj.pari > 1:
        crudy.message = "**%s**, combien de plis as-tu réalisé ? (**%d** plis avaient été demandés) ?"\
        % (obj.participant.joueur.pseudo.upper(), obj.pari)
    else:
        crudy.message = "**%s**, combien de plis as-tu réalisé ? (**%d** pli avait été demandé) ?"\
        % (obj.participant.joueur.pseudo.upper(), obj.pari)
    form = forms.WhistJeuRealForm(request.POST or None, request=request, instance=obj)
    if form.is_valid():
        form.save()
        partie = get_object_or_404(WhistPartie, id=crudy.folder_id)
        partie.modified = True
        partie.save()
        return redirect(crudy.url_view, obj.jeu)
    return render(request, "f_crudy_form.html", locals())

class WhistJeuParticipantView(CrudyListView):
    """ Liste des jeux par joueur """
    class Meta(CrudyListView.Options):
        application = APP_NAME
        model = WhistJeu
        title = "Faites vos Jeux"
        cols_ordered = ['jeu', "participant__joueur__pseudo", "medal", "score", "carte", "pari", "real", "points"]
        cols = {
            "jeu": {"title": "Jeu", "type":"numeric"},
            "participant__joueur__pseudo": {"title":"Participant", "type":"medal", "url":"v_whist_jeu_list"},
            "medal": {"hide":True},
            "score": {"title":"Score", "type":"number"},
            "carte": {"title":"Cartes", "type":"numeric"},
            "pari": {"title":"Paris", "type":"button", "url":"f_whist_jeu_pari", "disabled": True},
            "real": {"title":"Réalisé", "type":"button", "url":"f_whist_jeu_real", "disabled": True},
            "points": {"title":"Points", "type":"number"},
            "param": {"medal": "jeu"},
        }

        url_view = "v_whist_jeu_participant"

    def dispatch(self, request, *args, **kwargs):
        """ dispatch is called when the class instance loads """
        self.participant_id = kwargs.get('participant_id')
        return super().dispatch(request, args, kwargs)

    def get_queryset(self):
        """ fournir les données à afficher dans la vue """
        crudy = Crudy(self.request, APP_NAME)
        self.meta.url_back = "/whist/jeu/list/%s" % self.participant_id
        partie = get_object_or_404(WhistPartie, id=crudy.folder_id)

        objs = WhistJeu.objects.all()\
        .filter(participant__partie__id=crudy.folder_id, participant__id=self.participant_id, jeu__lt=partie.jeu)\
        .order_by('jeu')\
        .values(*self.meta.cols_ordered)

        # Tri des colonnes dans l'ordre de cols
        participant_name = ""
        self.objs = []
        for row in objs:
            participant_name = row["participant__joueur__pseudo"]
            ordered_dict = collections.OrderedDict()
            for col in self.meta.cols_ordered:
                ordered_dict[col] = row[col]  
            self.objs.append(ordered_dict) 

        self.meta.title = 'Jeux de "%s"' % participant_name

        return self.objs
