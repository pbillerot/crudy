# coding: utf-8
"""
    Traitement des VUES
"""
import re
import collections
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import resolve
# from django.views.decorators.csrf import csrf_tarot_protect
from django.http import JsonResponse
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from crudy.crudy import Crudy
from . import forms
from .models import TarotPartie, TarotJoueur, TarotParticipant, TarotJeu

def p_tarot_home(request):
    """ vue Home """
    crudy = Crudy(request, "tarot")
    title = crudy.application.get("title")
    crudy.url_actions = []
    form = None
    return render(request, 'p_tarot_home.html', locals())

def p_tarot_help(request):
    """ Guide """
    crudy = Crudy(request, "tarot")
    title = crudy.application.get("title")
    crudy.url_actions = []
    form = None
    return render(request, 'p_tarot_help.html', locals())

class TarotListView(ListView):
    """
        Gestion des vues
    """
    context_object_name = "objs"
    template_name = "v_tarot_view.html"
    context = None
    objs = []
    qcols = 0
    paginator = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.meta = self.Meta()
        if 'id' not in self.meta.cols:
            self.meta.cols["id"] = { "hide": True }
            self.meta.cols_ordered.append('id')
        self.meta.cols_list = []
        for key in self.meta.cols_ordered:
            self.meta.cols_list.append((key, self.meta.cols[key]))

    class Options:
        # def __init__(self, *args, **kwargs):

        title = "Titre de la vue"
        model = None
        template_name = "v_tarot_view.html"
        application = "tarot"
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
        cols = {}
        cols_ordered = []
        cols_list = []

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
        self.context["form"] = None
        self.context["paginator"] = self.paginator
        self.context["cols"] = self.meta.cols
        self.context["cols_list"] = self.meta.cols_list

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
        crudy.qcols = len(self.meta.cols) -1
        return self.context

    def get_queryset(self):
        """ queryset générique """
        objs = self.meta.model.objects.all()\
        .filter(**self.meta.filters)\
        .order_by(*self.meta.order_by)\
        .values(*self.meta.cols_ordered)
        # Tri des colonnes dans l'ordre de cols ??? voir si toujours utile en python 3.5
        self.objs = []
        for row in objs:
            ordered_dict = collections.OrderedDict()
            for col in self.meta.cols_ordered:
                ordered_dict[col] = row[col]
            self.objs.append(ordered_dict)

        return self.objs

"""
    Gestion des parties
"""
class TarotPartieSelectView(TarotListView):
    """ Sélection d'une partie """

    class Meta(TarotListView.Options):
        model = TarotPartie

        title = "Sélection / ajout d'une partie"
        url_add = "f_tarot_partie_create"
        url_update = "f_tarot_partie_update"
        url_folder = "f_tarot_partie_folder"
        cols_ordered = ['name']
        cols = {
            "name": {"title":"Partie"},
        }
        order_by = ('name',)
        url_view = "v_tarot_partie_select"
        template_name = "v_tarot_view.html"

    def get_queryset(self):
        """ queryset générique """
        # crudy = Crudy(self.request, "tarot")
        self.objs = self.meta.model.objects.all().filter(owner=self.request.user.username)\
        .filter(**self.meta.filters)\
        .order_by(*self.meta.order_by)\
        .values(*self.meta.cols)
        return self.objs

def f_tarot_partie_folder(request, record_id):
    """ Enregistrement d'une partie dans folder"""
    crudy = Crudy(request, "tarot")
    iid = int(record_id)

    # un seul item à la fois
    if iid == crudy.folder_id:
        crudy.folder_id = None
        crudy.folder_name = None
    else:
        obj = get_object_or_404(TarotPartie, id=iid)
        crudy.folder_id = obj.id
        crudy.folder_name = obj.name

    return redirect("v_tarot_participant_select")

def f_tarot_partie_create(request):
    """ Nouvelle partie """
    crudy = Crudy(request, "tarot")
    title = "Nouvelle Partie"
    model = TarotPartie
    crudy.message = ""
    crudy.is_form_autovalid = False
    if request.POST:
        form = forms.TarotPartieForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            post = form.save(commit=False)
            post.owner = request.user.username
            post.save()
            return redirect(crudy.url_view)
    else:
        form = forms.TarotPartieForm(request=request)
    return render(request, 'f_tarot_form.html', locals())

def f_tarot_partie_update(request, record_id):
    """ Modification d'une partie """
    crudy = Crudy(request, "tarot")
    title = "Modification d'une Partie"
    crudy.message = ""
    crudy.url_delete = "f_tarot_partie_delete"
    obj = get_object_or_404(TarotPartie, id=record_id)
    model = TarotPartie
    crudy.is_form_autovalid = False
    form = forms.TarotPartieForm(request.POST or None, request=request, instance=obj)
    if form.is_valid():
        form.save()
        return redirect(crudy.url_view)
    return render(request, "f_tarot_form.html", locals())

def f_tarot_partie_delete(request, record_id):
    """ suppression de l'enregistrement """
    crudy = Crudy(request, "tarot")
    obj = get_object_or_404(TarotPartie, id=record_id)
    obj.delete()
    return redirect(crudy.url_view)

"""
    Gestion des participants
"""
class TarotParticipantSelectView(TarotListView):
    """ Liste des participants """

    class Meta(TarotListView.Options):
        model = TarotJoueur
        title = "Sélection des Participants"
        cols_ordered = ['pseudo']
        cols = {
            "pseudo": {"title":"Nom du joueur"},
        }
        order_by = ('pseudo',)
        url_add = "f_tarot_joueur_create"
        url_update = "f_tarot_joueur_update"
        url_join = "v_tarot_participant_join"
        url_view = "v_tarot_participant_select"

    def get_queryset(self):
        """ queryset générique """
        crudy = Crudy(self.request, "tarot")
        objs = self.meta.model.objects.all().filter(owner=self.request.user.username)\
        .filter(**self.meta.filters)\
        .order_by(*self.meta.order_by)\
        .values(*self.meta.cols_ordered)
        # Cochage des participants dans la liste des joueurs
        participants = TarotParticipant.objects.all().filter(partie__id__exact=crudy.folder_id)
        crudy.joined = []
        for obj in objs:
            for participant in participants:
                if participant.joueur_id == obj["id"]:
                    crudy.joined.append(obj["id"])
        self.objs = []
        # tri des colonnes
        for row in objs:
            ordered_dict = collections.OrderedDict()
            for col in self.meta.cols:
                ordered_dict[col] = row[col]  
            self.objs.append(ordered_dict) 

        return self.objs

def v_tarot_participant_join(request, record_id):
    """ Sélection d'un participant dans la liste des joueurs """
    crudy = Crudy(request, "tarot")
    iid = int(record_id)

    if iid in crudy.joined:
        participant = TarotParticipant.objects.all().filter(partie_id__exact=crudy.folder_id, joueur_id__exact=iid)
        participant.delete()
        # compute_ordre() dans post_delete_tarot 
        crudy.joined.remove(iid)
    else:
        participant = TarotParticipant(partie_id=crudy.folder_id, joueur_id=iid)
        participant.save()
        participant.compute_order()
        crudy.joined.append(iid)

    return redirect(crudy.url_view)

def f_tarot_joueur_delete(request, record_id):
    """ suppression de l'enregistrement """
    crudy = Crudy(request, "tarot")
    obj = get_object_or_404(TarotJoueur, id=record_id)
    obj.delete()
    return redirect(crudy.url_view)


class TarotParticipantListView(TarotListView):
    """ Tri des participants """

    class Meta(TarotListView.Options):
        model = TarotParticipant
        title = "Ordre des Participants autour de la table"
        order_by = ('order', 'joueur__pseudo')
        url_order = "v_tarot_participant_order"
        cols_ordered = ['order','joueur__pseudo','donneur']
        cols = {
            "order": {"title":"Nom du joueur", "hide": True},
            "joueur__pseudo": {"title":"Nom du joueur", "type": "text"},
            "donneur": {"title":"Donneur Initial", "type": "check", "url":"f_tarot_participant_update"},
        }
        url_actions = [
            ("f_tarot_jeu_create", "Initialiser les jeux")
        ]
        url_delete = "v_tarot_participant_list"
        url_view = "v_tarot_participant_list"

    def get_queryset(self):
        """ queryset générique """
        crudy = Crudy(self.request, "tarot")
        objs = self.meta.model.objects.all()\
        .filter(partie_id=crudy.folder_id)\
        .order_by(*self.meta.order_by)\
        .values(*self.meta.cols)
        self.objs = []
        for row in objs:
            ordered_dict = collections.OrderedDict()
            for col in self.meta.cols:
                ordered_dict[col] = row[col]  
            self.objs.append(ordered_dict) 

        crudy.url_participant_update = 'f_tarot_participant_update'
        crudy.action_param = 0

        if len(self.objs) == 0:
            self.meta.url_actions = []

        return self.objs

def f_tarot_participant_update(request, record_id, checked):
    """ Mise à jour du donneur """
    crudy = Crudy(request, "tarot")

    participants = TarotParticipant.objects.all().filter(partie__id=crudy.folder_id)
    for participant in participants:
        if participant.id == int(record_id):
             participant.donneur = False if checked == "True" else True
        else:
            participant.donneur = False
        participant.save()

    return redirect(crudy.url_view)

def v_tarot_participant_order(request, record_id, orientation):
    """ On remonte le joueur dans la liste """
    crudy = Crudy(request, "tarot")
    iid = int(record_id)

    participant = get_object_or_404(TarotParticipant, id=iid)
    participant.order += int(orientation) * 3
    participant.save()
    participant.compute_order()

    return redirect(crudy.url_view)

def f_tarot_joueur_create(request):
    """ création d'un joueur """
    crudy = Crudy(request, "tarot")
    title = "Nouveau Joueur"
    crudy.message = ""
    model = TarotJoueur
    crudy.is_form_autovalid = False
    if request.POST:
        form = forms.TarotJoueurForm(request.POST, request=request)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user.username
            post.save()
            return redirect(crudy.url_view)
    else:
        form = forms.TarotJoueurForm(request=request)
    return render(request, 'f_tarot_form.html', locals())

def f_tarot_joueur_update(request, record_id):
    """ mise à jour d'un joueur """
    crudy = Crudy(request, "tarot")
    crudy.url_delete = "f_tarot_joueur_delete"
    title = "Modification d'un Joueur"
    crudy.message = ""
    crudy.is_form_autovalid = False
    obj = get_object_or_404(TarotJoueur, id=record_id)
    form = forms.TarotJoueurForm(request.POST or None, instance=obj, request=request)
    if form.is_valid():
        form.save()
        return redirect(crudy.url_view)
    return render(request, "f_tarot_form.html", locals())

"""
    Gestion des jeux
"""
class TarotJeuListView(TarotListView):
    """ Liste des jeux """

    class Meta(TarotListView.Options):
        model = TarotJeu
        title = "Faites vos Jeux"
        cols_ordered = ['donneur','participant__joueur__pseudo','medal','score','pari','partenaire','real','primes'\
        ,'ptbout','poignee1','poignee2','poignee3','misere1','misere2','grchelem','gchelem','ptchelem','pchelem','ppchelem','points','modified']
        cols = {
            "donneur": {"title":"", "type": "position", "tooltip": "Le donneur pour ce tour"},
            "participant__joueur__pseudo": {"title":"Participant", "type":"medal"},
            "medal": {"hide":True},
            "score": {"title":"Score", "type":"number"},
            "pari": {"title":"Enchères", "type":"radio", "url": "f_tarot_jeu_pari",
                "list": [("...","..."), ("PT","Petite"), ("PC","Pouce"), ("GA","Garde"), ("GS","Garde Sans"), ("GC","Garde Contre")]},
            "partenaire": {"title":"Avec", "type":"check", "url": "f_tarot_jeu_partenaire"},
            "real": {"title":"Réal", "type":"point", "url": "f_tarot_jeu_real",
                "list": [(-30,"- 30"),(-20,"- 20"),(-10,"- 10"),(-1,"- 0"),(0,"0")\
                ,(+1,"+ 0"),(+10,"+ 10"),(+20,"+ 20"),(+30,"+ 30"),(+40,"+ 40"),(+50,"+ 50"),(+60,"+ 60")]},
            "primes": {"title":"Primes", "type":"category", "url": "f_tarot_jeu_prime", "category": "prime"},
            # primes
            "ptbout": {"hide": True, "title":"Petit au bout", "type":"check", "url": "f_tarot_jeu_prime", "category": "prime"},
            "poignee1": {"hide": True, "title": "Poignée", "type":"check", "category": "prime"},
            "poignee2": {"hide": True, "title": "Double Poignée", "type":"check", "category": "prime"},
            "poignee3": {"hide": True, "title": "Triple Poignée", "type":"check", "category": "prime"},
            "misere1": {"hide": True, "title": "Misère d'Atout", "type":"check", "category": "prime"},
            "misere2": {"hide": True, "title": "Misère de Tête", "type":"check", "category": "prime"},
            "grchelem": {"hide": True, "title": "Grand Chelem", "type":"check", "category": "prime"},
            "gchelem": {"hide": True, "title": "Grand Chelem non annoncé", "type":"check", "category": "prime"},
            "gpchelem": {"hide": True, "title": "Grand Chelem perdu", "type":"check", "category": "prime"},
            "ptchelem": {"hide": True, "title": "Petit Chelem", "type":"check", "category": "prime"},
            "pchelem": {"hide": True, "title": "Petit Chelem non annoncé", "type":"check", "category": "prime"},
            "ppchelem": {"hide": True, "title": "Petit Chelem perdu", "type":"check", "category": "prime"},

            "points": {"title":"Points", "type":"number"},
            "modified": {"hide": True},
        }
        url_view = "v_tarot_jeu_list"
        url_add = "f_tarot_jeu_add"
        url_actions = [
            ("f_tarot_jeu_compute", "Calculer les points")
        ]

    def dispatch(self, request, *args, **kwargs):
        """ dispatch is called when the class instance loads """
        self.sort = kwargs.get('sort', None)
        self.page = kwargs.get('page')
        return super().dispatch(request, args, kwargs)

    def get_queryset(self):
        """ fournir les données à afficher dans la vue """
        crudy = Crudy(self.request, "tarot")
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
        .values(*self.meta.cols_ordered)

        # Tri des colonnes dans l'ordre de cols
        objects_list = []
        b_calcul_realised = False
        crudy.modified = False
        for row in objs:
            # on remplit la colonne ptbout avec la catégorie prime
            primes = []
            for key, col in self.meta.cols_list:
                if col.get("category") == "prime":
                    if row[key]:
                        primes.append((col.get("title")))
            if len(primes) == 0:
                primes.append(("0"))
            row["primes"] = primes
            # raz real si pas d'enchère
            if row["pari"] == ".":
                row["real"] = 99
            ordered_dict = collections.OrderedDict()
            ordered_dict["id"] = row["id"]
            for col in self.meta.cols_ordered:
                ordered_dict[col] = row[col]
            # objects_list.append(ordered_dict)
            objects_list.append(row)

        qparticipant = TarotParticipant.objects.all().filter(partie__id__exact=crudy.folder_id).count()
        if qparticipant > 0:
            self.paginator = Paginator(objects_list, qparticipant)
            self.objs = self.paginator.get_page(self.page)
            for row in self.objs:
                if row.get("points") != 0:
                    b_calcul_realised = True
                if row.get("modified"):
                    crudy.modified = True
            crudy.action_param = self.page
            crudy.jeu = int(self.page)
            crudy.url_sort = 'v_tarot_jeu_sort'
            partie = get_object_or_404(TarotPartie, id=crudy.folder_id)
            crudy.jeu_current = partie.jeu

        # on cache la colonne partenaire si jeu à 4 ou 3
        if qparticipant == 3 or qparticipant == 4:
            self.meta.cols["partenaire"]["hide"] = True
        else:
            self.meta.cols["partenaire"]["hide"] = False

        if not crudy.modified:
            self.meta.url_actions = []

        if not b_calcul_realised or int(self.page) != self.paginator.num_pages or crudy.modified:
            self.meta.url_add = None
        crudy.url_sort = 'v_tarot_jeu_sort'
        return self.objs

def f_tarot_jeu_create(request, id):
    """ création des jeux (tours) de la partie """
    crudy = Crudy(request, "tarot")
    jeu = TarotJeu()
    jeu.create_jeux(crudy)

    return redirect("v_tarot_jeu_list", 1)

def f_tarot_jeu_add(request):
    """ ajout d'un jeu dans la partie """
    crudy = Crudy(request, "tarot")
    jeu = TarotJeu()
    jeu.add_jeux(crudy)

    partie = get_object_or_404(TarotPartie, id=crudy.folder_id)
    return redirect("v_tarot_jeu_list", partie.jeu)

encheres = {
    "PT": 10,
    "PC": 20,
    "GA": 40,
    "GS": 60,
    "GC": 80,
}
primes = {
    "ptbout": 10,
    "misere1": 10,
    "misere2": 10,
    "poignee1": 20,
    "poignee2": 30,
    "poignee3": 40,
    "grchelem": 400,
    "gchelem": 200,
    "gpchelem": -200,
    "ptchelem": 200,
    "pchelem": 100,
    "ppchelem": -100,
}

def f_tarot_jeu_compute(request, ijeu):
    """ Calcul des points du jeux, du score et du rang du joueur """
    crudy = Crudy(request, "tarot")
    jeux = TarotJeu.objects.all().filter(participant__partie__id=crudy.folder_id).order_by("jeu","-pari")
    participants = TarotParticipant.objects.all().filter(partie__id=crudy.folder_id)

    score = {}
    miseres = {}
    points = 0
    ijeu = 0

    # CALCUL DES POINTS 
    for jeu in jeux:
        if ijeu != jeu.jeu: # changement de jeu
            # enregistrement des points et score des joueurs
            if ijeu != 0:
                jjs = TarotJeu.objects.all().filter(participant__partie__id=crudy.folder_id, jeu=ijeu)
                for jj in jjs:
                    jj.points = 0
                    if jj.prenneur:
                        if participants.count() == 3:
                            jj.points = points * 1 # car ausi partenaire
                        elif participants.count() == 4:
                            jj.points = points * 2 # car ausi partenaire
                        elif participants.count() == 5:
                            jj.points = points * 2
                        elif participants.count() == 6:
                            jj.points = points * 2
                    if jj.partenaire:
                        if jj.prenneur and participants.count() > 4:
                            jj.points += points * 2
                        else:
                            jj.points += points
                    if not jj.prenneur and not jj.partenaire:
                        jj.points = points * -1
                    # misères
                    for j_id in miseres:
                        if j_id == jj.participant.id:
                            jj.points += miseres[j_id] * (participants.count() -1)
                        else:
                            jj.points += miseres[j_id] * -1
                    if participants.count() == 6 and jj.donneur:
                        jj.points = 0
                    score[jj.participant.id] = score.get(jj.participant.id, 0) + jj.points
                    jj.score = score[jj.participant.id]
                    jj.save()
            # on prépare le tour suivant
            miseres = {}
            points = 0
            ijeu = jeu.jeu

        # Calcul de la donne à répartir sur les joueurs
        if jeu.prenneur:
            points = encheres[jeu.pari]
            if jeu.real > 0:
                if jeu.real == 1:
                    points = points
                else:
                    points = points + jeu.real
            else:
                if jeu.real == -1:
                    points = points * -1
                else:
                    points = points * -1 + jeu.real
        if jeu.prenneur or jeu.partenaire:
            if jeu.ptbout:
                points = points + 10
            if jeu.real > 0:
                if jeu.poignee1: 
                    points = points + 20
                if jeu.poignee2: 
                    points = points + 30
                if jeu.poignee3: 
                    points = points + 40
                if jeu.ptchelem:
                    points = points + 200
                if jeu.pchelem:
                    points = points + 100
                if jeu.grchelem:
                    points = points + 400
                if jeu.gchelem:
                    points = points + 200
            else:
                if jeu.gpchelem:
                    points = points - 200
                if jeu.ppchelem:
                    points = points - 100
        else:
            if jeu.ptbout:
                points = points - 10

        # misères
        if jeu.misere1: 
            miseres[jeu.participant.id] = miseres.get(jeu.participant.id, 0) + 10
        if jeu.misere2: 
            miseres[jeu.participant.id] = miseres.get(jeu.participant.id, 0) + 10

    # DERNIER TOUR
    if ijeu != 0:
        # enregistrement des points et score des joueurs
        # on refait une boucle
        jjs = TarotJeu.objects.all().filter(participant__partie__id=crudy.folder_id, jeu=ijeu)
        for jj in jjs:
            jj.points = 0
            if jj.prenneur:
                if participants.count() == 3:
                    jj.points = points * 1
                elif participants.count() == 4:
                    jj.points = points * 2
                elif participants.count() == 5:
                    jj.points = points * 2
                elif participants.count() == 6:
                    jj.points = points * 2
            if jj.partenaire:
                if jj.prenneur and participants.count() > 4:
                    jj.points += points * 2
                else:
                    jj.points += points
            if not jj.prenneur and not jj.partenaire:
                jj.points = points * -1
            # misères
            for j_id in miseres:
                if j_id == jj.participant.id:
                    jj.points += miseres[j_id] * (participants.count() -1)
                else:
                    jj.points += miseres[j_id] * -1
            if participants.count() == 6 and jj.donneur:
                jj.points = 0
            score[jj.participant.id] = score.get(jj.participant.id, 0) + jj.points
            jj.score = score[jj.participant.id]
            jj.save()

    # Attribution des médailles
    jeux = TarotJeu.objects.all()\
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
                last_jeu = get_object_or_404(TarotJeu, pk=last_pk)
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
        jeu.modified = False
        jeu.save()
    # Médaille de chocolat
    if last_pk != 0:
        last_jeu = get_object_or_404(TarotJeu, pk=last_pk)
        last_jeu.medal = 9
        last_jeu.save()

    # maj du score des participants
    for j_id in score:
        participant = get_object_or_404(TarotParticipant, id=j_id)
        participant.score = score.get(j_id)
        participant.save()
    
    return redirect("v_tarot_jeu_list", ijeu)

def f_tarot_jeu_pari(request, record_id):
    """ Saisie pari d'un joueur """
    crudy = Crudy(request, "tarot")
    crudy.is_form_autovalid = True
    obj = get_object_or_404(TarotJeu, id=record_id)
    title = "Enchère de %s" % (obj.participant.joueur.pseudo.upper())
    form = forms.TarotJeuPariForm(request.POST or None, request=request, instance=obj)
    if form.is_valid():
        form.save()
        jeu_courant = get_object_or_404(TarotJeu, id=record_id)
        jeu_courant.prenneur = True
        jeu_courant.partenaire = True
        jeu_courant.real = 0
        jeu_courant.modified = True
        jeu_courant.save()
        if jeu_courant.pari != "...":
            # Nettoyage des enchères des autres joueurs
            jeux = TarotJeu.objects.all().filter(participant__partie__id=obj.participant.partie_id, jeu=obj.jeu)
            for jeu in jeux:
                if jeu.id != jeu_courant.id:
                    jeu.pari = "..."
                    jeu.real = 99
                    jeu.save()
        return redirect(crudy.url_view, obj.jeu)
    return render(request, "f_tarot_form.html", locals())

def f_tarot_jeu_real(request, record_id):
    """ Saisie du réalisé 0 1 2 """
    crudy = Crudy(request, "tarot")
    crudy.is_form_autovalid = True
    obj = get_object_or_404(TarotJeu, id=record_id)
    title = "Nombre de points réalisé par %s" % (obj.participant.joueur.pseudo.upper())
    form = forms.TarotJeuRealForm(request.POST or None, request=request, instance=obj)
    if form.is_valid():
        form.save()
        obj.modified = True
        obj.save()
        return redirect(crudy.url_view, obj.jeu)
    return render(request, "f_tarot_form.html", locals())

def f_tarot_jeu_partenaire(request, record_id, checked):
    """ Saisie du partenaire """
    crudy = Crudy(request, "tarot")
    tarotJeu = get_object_or_404(TarotJeu, id=record_id)
    jeux = TarotJeu.objects.all().filter(participant__partie_id=tarotJeu.participant.partie_id, jeu=tarotJeu.jeu)
    for jeu in jeux:
        if jeu.id == int(record_id):
            jeu.partenaire = False if checked == "True" else True
        else:
            jeu.partenaire = False
        jeu.modified = True
        jeu.save()

    return redirect(crudy.url_view, tarotJeu.jeu)

def f_tarot_jeu_prime(request, record_id):
    """ Saisie des primes """
    crudy = Crudy(request, "tarot")
    crudy.is_form_autovalid = False
    obj = get_object_or_404(TarotJeu, id=record_id)
    title = "Saisie des primes pour %s" % (obj.participant.joueur.pseudo.upper())
    form = forms.TarotJeuPrimeForm(request.POST or None, request=request, instance=obj)
    if form.is_valid():
        form.save()
        obj.modified = True
        obj.save()
        # un seul ptbout par jeu
        if obj.ptbout:
            jeux = TarotJeu.objects.all().filter(participant__partie__id=obj.participant.partie_id, jeu=obj.jeu)
            for jeu in jeux:
                if jeu.id != obj.id:
                    jeu.ptbout = False
                    jeu.save()

        return redirect(crudy.url_view, obj.jeu)
    return render(request, "f_tarot_form.html", locals())
