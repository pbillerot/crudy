# coding: utf-8
"""
    Traitement des VUES
"""
import re
import collections
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import resolve
# from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from crudy.crudy import Crudy
from . import forms
from .models import WhistPartie, WhistJoueur, WhistParticipant, WhistJeu

def p_whist_home(request):
    """ vue Home """
    crudy = Crudy(request, "whist")
    title = crudy.application.get("title")
    form = None
    return render(request, 'p_whist_home.html', locals())

def p_whist_help(request):
    """ Guide """
    crudy = Crudy(request, "whist")
    title = crudy.application.get("title")
    form = None
    return render(request, 'p_whist_help.html', locals())

class WhistListView(ListView):
    """
        Gestion des vues
    """
    context_object_name = "objs"
    template_name = "v_whist_view.html"
    context = None
    objs = []
    qcols = 0
    paginator = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.meta = self.Meta()

    class Options:
        # def __init__(self, *args, **kwargs):

        title = "Titre de la vue"
        model = None
        template_name = "v_whist_view.html"
        application = "whist"
        # urls définis dans ursl.py
        url_add = None
        url_update = None
        url_delete = None
        url_select = None
        url_folder = None
        url_join = None
        url_order = None
        url_actions = []
        url_view = None
        url_param = ""
        # query sur la base
        # liste des champs à afficher dans la vue
        cols = []
        cols_attrs = {}

        filters = {} # filtres du query_set
        order_by = () # liste des colonnes à trier

    class Meta(Options):
        pass

    def get_context_data(self, **kwargs):
        """ fourniture des données à la vue """
        crudy = Crudy(self.request, self.meta.application)
        self.context = super().get_context_data(**kwargs)
        # url = resolve(self.request.path)
        # raz selected si nouvelle vue
        if crudy.url_view != self.meta.url_view:
            crudy.selected = []
        self.context["title"] = self.meta.title
        self.context["crudy"] = crudy
        self.context["cols"] = self.meta.cols
        self.context["form"] = None
        self.context["paginator"] = self.paginator

        # Fourniture des attributs des colonnes dans un dictionnaire
        attrs_model = {
            "title": "",
            "td_class": "mdl-data-table__cell--non-numeric",
            "class": "",
            "type": "text",
        }
        self.context["dico"] =  {}
        for index in self.meta.cols:
            attrs = self.meta.cols_attrs.get(index, attrs_model)
            for key in attrs_model:
                attrs[key] = attrs.get(key, attrs_model[key])
            self.context["dico"][index] = attrs

        # cochage de tous les enregistrements
        if 0 in crudy.selected:
            for obj in self.objs:
                crudy.selected.append(obj["id"])
        # tri des objs dans l'ordre des cols
        crudy.url_view = self.meta.url_view
        crudy.url_return = self.request.path
        crudy.url_join = self.meta.url_join
        crudy.url_param = self.meta.url_param
        crudy.url_actions = self.meta.url_actions
        crudy.url_order = self.meta.url_order
        crudy.url_folder = self.meta.url_folder
        crudy.url_add = self.meta.url_add
        crudy.url_update = self.meta.url_update
        crudy.url_delete = self.meta.url_delete
        crudy.url_select = self.meta.url_select
        crudy.qcols = self.qcols
        return self.context

    def get_queryset(self):
        """ queryset générique """
        if 'id' not in self.meta.cols:
            self.meta.cols.append("id")
        objs = self.meta.model.objects.all()\
        .filter(**self.meta.filters)\
        .order_by(*self.meta.order_by)\
        .values(*self.meta.cols)
        # Tri des colonnes dans l'ordre de cols
        self.objs = []
        for row in objs:
            self.qcols = len(self.meta.cols) -1
            ordered_dict = collections.OrderedDict()
            for col in self.meta.cols:
                ordered_dict[col] = row[col]
            self.objs.append(ordered_dict)

        return self.objs

"""
    Gestion des parties
"""
class WhistPartieSelectView(WhistListView):
    """ Sélection d'une partie """

    class Meta(WhistListView.Options):
        model = WhistPartie

        title = "Sélection / ajout d'une partie"
        url_add = "f_partie_create"
        url_update = "f_partie_update"
        url_folder = "f_partie_folder"
        cols = ["name", "cartes"]
        cols_attrs = {
            "name": {"title":"Partie"},
            "cartes": {"title":"Nombre de cartes max", "td_class": "crudy-data-table__cell--text-center"},
        }
        order_by = ('name',)
        url_view = "v_partie_select"
        template_name = "v_whist_view.html"

def f_partie_folder(request, record_id):
    """ Enregistrement d'une partie dans folder"""
    crudy = Crudy(request, "whist")
    iid = int(record_id)

    # un seul item à la fois
    if iid == crudy.folder_id:
        crudy.folder_id = None
        crudy.folder_name = None
    else:
        obj = get_object_or_404(WhistPartie, id=iid)
        crudy.folder_id = obj.id
        crudy.folder_name = obj.name

    return redirect("v_participant_select")

def f_partie_create(request):
    """ Nouvelle partie """
    crudy = Crudy(request, "whist")
    title = "Nouvelle Partie"
    model = WhistPartie
    crudy.message = ""
    if request.POST:
        form = forms.WhistPartieForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            return redirect(crudy.url_view)
    else:
        form = forms.WhistPartieForm(request=request)
    return render(request, 'f_whist_form.html', locals())

def f_partie_update(request, record_id):
    """ Modification d'une partie """
    crudy = Crudy(request, "whist")
    title = "Modification d'une Partie"
    crudy.message = ""
    crudy.url_delete = "f_partie_delete"
    obj = get_object_or_404(WhistPartie, id=record_id)
    model = WhistPartie
    form = forms.WhistPartieForm(request.POST or None, request=request, instance=obj)
    if form.is_valid():
        form.save()
        return redirect(crudy.url_view)
    return render(request, "f_whist_form.html", locals())

def f_partie_delete(request, record_id):
    """ suppression de l'enregistrement """
    crudy = Crudy(request, "whist")
    obj = get_object_or_404(WhistPartie, id=record_id)
    obj.delete()
    return redirect(crudy.url_view)

"""
    Gestion des participants
"""
class WhistParticipantSelectView(WhistListView):
    """ Liste des participants """

    class Meta(WhistListView.Options):
        model = WhistJoueur
        title = "Sélection des Participants"
        cols = ["pseudo", "email"]
        cols_attrs = {
            "pseudo": {"title":"Nom du joueur"},
            "email": {"title":"Email"},
        }
        order_by = ('pseudo',)
        url_add = "f_joueur_create"
        url_update = "f_joueur_update"
        url_join = "v_participant_join"
        url_view = "v_participant_select"

    def get_queryset(self):
        """ queryset générique """
        crudy = Crudy(self.request, "whist")
        if 'id' not in self.meta.cols:
            self.meta.cols.append("id")
        objs = self.meta.model.objects.all()\
        .filter(**self.meta.filters)\
        .order_by(*self.meta.order_by)\
        .values(*self.meta.cols)
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
            self.qcols = len(self.meta.cols) -1
            ordered_dict = collections.OrderedDict()
            for col in self.meta.cols:
                ordered_dict[col] = row[col]  
            self.objs.append(ordered_dict) 

        return self.objs

def v_participant_join(request, record_id):
    """ Sélection d'un participant dans la liste des joueurs """
    crudy = Crudy(request, "whist")
    iid = int(record_id)

    if iid in crudy.joined:
        participant = WhistParticipant.objects.all().filter(partie_id__exact=crudy.folder_id, joueur_id__exact=iid)
        participant.delete()
        # compute_ordre() dans post_delete_whist 
        crudy.joined.remove(iid)
    else:
        participant = WhistParticipant(partie_id=crudy.folder_id, joueur_id=iid)
        participant.save()
        participant.compute_order()
        crudy.joined.append(iid)

    return redirect(crudy.url_view)

def f_joueur_delete(request, record_id):
    """ suppression de l'enregistrement """
    crudy = Crudy(request, "whist")
    obj = get_object_or_404(WhistJoueur, id=record_id)
    obj.delete()
    return redirect(crudy.url_view)


class WhistParticipantListView(WhistListView):
    """ Tri des participants """

    class Meta(WhistListView.Options):
        model = WhistParticipant
        title = "Ordre des Participants autour de la table"
        cols = ["joueur__pseudo", "donneur"]
        order_by = ('order', 'joueur__pseudo')
        url_order = "v_participant_order"
        cols_attrs = {
            "joueur__pseudo": {"title":"Nom du joueur"},
            "donneur": {"title":"Donneur initial", "td_class": "crudy-data-table__cell--text-center"},
        }
        url_actions = [
            ("f_jeu_create", "Initialiser les jeux")
        ]
        url_delete = "v_participant_list"
        url_view = "v_participant_list"

    def get_queryset(self):
        """ queryset générique """
        crudy = Crudy(self.request, "whist")
        if 'id' not in self.meta.cols:
            self.meta.cols.append("id")
        objs = self.meta.model.objects.all()\
        .filter(partie_id=crudy.folder_id)\
        .order_by(*self.meta.order_by)\
        .values(*self.meta.cols)
        self.objs = []
        for row in objs:
            self.qcols = len(self.meta.cols) -1
            ordered_dict = collections.OrderedDict()
            for col in self.meta.cols:
                ordered_dict[col] = row[col]  
            self.objs.append(ordered_dict) 

        crudy.url_participant_update = 'f_participant_update'
        crudy.action_param = 0
        return self.objs

def f_participant_update(request, record_id, checked):
    """ Mise à jour du donneur """
    crudy = Crudy(request, "whist")
    iid = int(record_id)

    participants = WhistParticipant.objects.all().filter(partie__id=crudy.folder_id)
    joueur_id = 0
    for participant in participants:
        if participant.id == iid:
            participant.donneur = int(checked)
            if int(checked) == 1:
                joueur_id = participant.joueur_id
        else:
            participant.donneur = 0
        participant.save()

    return redirect(crudy.url_view)

def v_participant_order(request, record_id, orientation):
    """ On remonte le joueur dans la liste """
    crudy = Crudy(request, "whist")
    iid = int(record_id)

    participant = get_object_or_404(WhistParticipant, id=iid)
    participant.order += int(orientation) * 3
    participant.save()
    participant.compute_order()

    return redirect(crudy.url_view)

def f_joueur_create(request):
    """ création d'un joueur """
    crudy = Crudy(request, "whist")
    title = "Nouveau Joueur"
    crudy.message = ""
    model = WhistJoueur
    if request.POST:
        form = forms.WhistJoueurForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            return redirect(crudy.url_view)
    else:
        form = forms.WhistJoueurForm(request=request)
    return render(request, 'f_whist_form.html', locals())

def f_joueur_update(request, record_id):
    """ mise à jour d'un joueur """
    crudy = Crudy(request, "whist")
    crudy.url_delete = "f_joueur_delete"
    title = "Modification d'un Joueur"
    crudy.message = ""
    obj = get_object_or_404(WhistJoueur, id=record_id)
    form = forms.WhistJoueurForm(request.POST or None, instance=obj, request=request)
    if form.is_valid():
        form.save()
        return redirect(crudy.url_view)
    return render(request, "f_whist_form.html", locals())

"""
    Gestion des jeux
"""
class WhistJeuListView(WhistListView):
    """ Liste des jeux """

    class Meta(WhistListView.Options):
        model = WhistJeu
        title = "Faites vos Jeux"
        cols = ["donneur", "participant__joueur__pseudo", "medal", "score", "carte", "pari", "real", "points"]
        cols_attrs = {
            "donneur": {"title":""},
            "participant__joueur__pseudo": {"title":"Participant"},
            "medal": {"title":"M", "td_class": "crudy-data-table__cell--text-center"},
            "score": {"title":"Score", "td_class": "crudy-data-table__cell--text-center"},
            "carte": {"title":"Carte", "td_class": "crudy-data-table__cell--text-center"},
            "pari": {"title":"Pari", "td_class": "crudy-data-table__cell--text-center"},
            "real": {"title":"Réalisé", "td_class": "crudy-data-table__cell--text-center"},
            "points": {"title":"Point", "td_class": "crudy-data-table__cell--text-center"},
        }

        url_view = "v_jeu_list"
        url_actions = [
            ("f_jeu_compute", "Calculer les points")
        ]

    def dispatch(self, request, *args, **kwargs):
        """ dispatch is called when the class instance loads """
        self.sort = kwargs.get('sort', None)
        self.page = kwargs.get('page')
        return super().dispatch(request, args, kwargs)

    def get_queryset(self):
        """ fournir les données à afficher dans la vue """
        crudy = Crudy(self.request, "whist")
        # ajout de la colonne id
        if 'id' not in self.meta.cols:
            self.meta.cols.append("id")
        # prise en compte de la colonne à trier en fonction de sort
        if self.sort == "score":
            crudy.sort = "score"

        if self.sort == "participant":
            crudy.sort = "participant"

        if crudy.sort == "score":
            order_by = ('jeu', '-score',)
        else:
            order_by = ('jeu', 'participant__order',)

        objs = self.meta.model.objects.all()\
        .filter(participant__partie__id__exact=crudy.folder_id)\
        .order_by(*order_by)\
        .values(*self.meta.cols)

        # Tri des colonnes dans l'ordre de cols
        objects_list = []
        for row in objs:
            self.qcols = len(self.meta.cols) -1
            ordered_dict = collections.OrderedDict()
            for col in self.meta.cols:
                ordered_dict[col] = row[col]  
            objects_list.append(ordered_dict) 

        qparticipant = WhistParticipant.objects.all().filter(partie__id__exact=crudy.folder_id).count()
        paginator = Paginator(objects_list, qparticipant)
        
        self.objs = paginator.get_page(self.page)
        self.paginator = True # pour le template
        # comptage de nombre de plis demandés et réalisés
        qplis = 0
        qreal = 0
        qcarte = 0
        for obj in self.objs:
            qplis += obj["pari"]
            qreal += obj["real"]
            qcarte = obj["carte"]
        crudy.cartes = []
        for pp in range(1, paginator.num_pages + 1):
            if pp <= paginator.num_pages / 2:
                crudy.cartes.append((pp, pp))
            else:
                crudy.cartes.append((pp, paginator.num_pages - pp + 1))
        crudy.url_jeu_pari = "f_jeu_pari"
        crudy.url_jeu_real = "f_jeu_real"
        crudy.action_param = self.page
        crudy.jeu = int(self.page)
        crudy.url_sort = 'v_jeu_sort'
        partie = get_object_or_404(WhistPartie, id=crudy.folder_id)
        crudy.jeu_current = partie.jeu
        if int(crudy.jeu) > partie.jeu + 1:
            self.meta.url_actions = []
        if qreal != qcarte:
            self.meta.url_actions = []

        self.meta.cols_attrs["pari"]["subtitle"] = "%s / %s" % (qplis, qcarte)
        self.meta.cols_attrs["real"]["subtitle"] = "%s / %s" % (qreal, qcarte)
        return self.objs

def f_jeu_create(request, id):
    """ création des jeux (tours) de la partie """
    crudy = Crudy(request, "whist")
    jeu = WhistJeu()
    jeu.create_jeux(crudy)

    return redirect("v_jeu_list", 1)

def f_jeu_compute(request, ijeu):
    """ Calcul des points du jeux, du score et du rang du joueur """
    crudy = Crudy(request, "whist")
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
        partie.save()

    return redirect("v_jeu_list", partie.jeu)

def f_jeu_pari(request, record_id):
    """ Saisie pari d'un joueur """
    crudy = Crudy(request, "whist")
    crudy.is_form_autovalid = True
    obj = get_object_or_404(WhistJeu, id=record_id)
    title = "Pari de %s" % (obj.participant.joueur.pseudo.upper())
    crudy.message = "**%s**, Combien penses-tu faire de plis ?" % (obj.participant.joueur.pseudo.upper())
    form = forms.WhistJeuPariForm(request.POST or None, request=request, instance=obj)
    if form.is_valid():
        form.save()
        return redirect(crudy.url_view, obj.jeu)
    return render(request, "f_whist_form.html", locals())

def f_jeu_real(request, record_id):
    """ Saisie du réalisé 0 1 2 """
    crudy = Crudy(request, "whist")
    crudy.is_form_autovalid = True
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
        return redirect(crudy.url_view, obj.jeu)
    return render(request, "f_whist_form.html", locals())
