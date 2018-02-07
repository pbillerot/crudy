"""
    Traitement des VUES
"""
import re
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import resolve
from .models import WhistPartie, WhistJoueur, WhistParticipant, WhistJeu
from . import forms
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def get_ctx(request):
    """ Obtenir le ctx de la session """
    if not request.session.get("ctx", False):
        ctx = {
            "title": "JEU DU WHIST",
            "selected": [],
            "joined": [],
            "folder_id": None,
            "folder_name": None,
            "carte": [],
            "jeu": None,
            "url_view": None,
            "sort": None
        }
        request.session["ctx"] = ctx
    return request.session["ctx"]
def set_ctx(request, ctx):
    """ Mettre à jour le ctx de la session """
    request.session["ctx"] = ctx

def whist_proto(request):
    """ vue proto """
    return render(request, 'whist/whist_proto.html', {})

def whist_home(request):
    """ vue Home """
    ctx = get_ctx(request)
    set_ctx(request, ctx)
    model = WhistPartie
    return render(request, 'whist/whist_home.html', locals())

def whist_select(request, record_id):
    """ Sélection/désélection d'un élément dans une liste """
    ctx = get_ctx(request)
    iid = int(record_id)

    if 0 in ctx["selected"] and iid != 0:
        ctx["selected"].remove(0)

    if iid in ctx["selected"]:
        if iid == 0:
            ctx["selected"] = []
        else:
            while iid in ctx["selected"]:
                ctx["selected"].remove(iid)
    else:
        ctx["selected"].append(iid)

    set_ctx(request, ctx)
    return redirect(ctx["url_view"])

class WhistListView(ListView):
    """
        Gestion des vues
    """
    context_object_name = "objs"
    template_name = "whist/whist_view.html"
    context = None
    objs = None
    # ctx
    ctx = None

    def __init__(self, *args, **kwargs):
        super(WhistListView, self).__init__(*args, **kwargs)
        self.meta = self.Meta()

    class Options:
        # def __init__(self, *args, **kwargs):

        title = "Titre de la vue"
        model = None
        template_name = "whist/whist_view.html"
        # urls définis dans ursl.py
        url_add = None
        url_update = None
        url_delete = None
        url_select = "whist_select" # émis par url_delete
        url_folder = None
        url_join = None
        url_order = None
        url_actions = []
        url_view = None
        # query sur la base
        # liste des champs à afficher dans la vue
        fields = {
            "name": "title"
        }
        filters = {} # filtres du query_set
        order_by = () # liste des colonnes à trier
        # Rendu
        search_in = () # liste des colonnes objet de la recherche, un champ recherche sera présenté

    class Meta(Options):
        pass

    def get_context_data(self, **kwargs):
        """ fourniture des données à la vue """
        self.context = super().get_context_data(**kwargs)
        url = resolve(self.request.path)
        ctx = get_ctx(self.request)
        # raz selected si nouvelle vue
        if ctx["url_view"] != self.meta.url_view:
            ctx["selected"] = []
        self.context["model"] = self.model
        self.context["title"] = self.meta.title
        self.context["url_add"] = self.meta.url_add
        self.context["url_update"] = self.meta.url_update
        self.context["url_delete"] = self.meta.url_delete
        self.context["url_select"] = self.meta.url_select
        self.context["url_folder"] = self.meta.url_folder
        self.context["url_order"] = self.meta.url_order
        self.context["url_join"] = self.meta.url_join
        self.context["url_actions"] = self.meta.url_actions
        self.context["url_view"] = self.meta.url_view
        self.context["search_in"] = self.meta.search_in
        # Récupération des fields correspondants aux objs
        self.context["fields"] = [title for title in self.meta.fields.values()]
        # cochage des enregistrements sélectionnés
        if 0 in ctx["selected"]:
            for obj in self.objs:
                ctx["selected"].append(obj["id"])
        ctx["url_view"] = self.meta.url_view
        set_ctx(self.request, ctx)
        self.context["ctx"] = ctx
        return self.context

    def get_queryset(self):
        """ queryset générique """
        if 'id' not in self.meta.fields:
            self.meta.fields["id"] = "id"
        self.objs = self.meta.model.objects.all()\
        .filter(**self.meta.filters)\
        .order_by(*self.meta.order_by)\
        .values(*self.meta.fields.keys())
        return self.objs

"""
    Gestion des parties
"""
class WhistPartieListView(WhistListView):
    """ Gestion des parties """

    class Meta(WhistListView.Options):
        model = WhistPartie
        title = "Gestion des Parties"
        url_add = "partie_create"
        url_update = "partie_update"
        url_delete = "partie_delete"
        fields = {
            "name": "Partie",
            "cartes": "Nombre de cartes max"
        }
        order_by = ('name',)
        url_view = "partie_list"

class WhistPartieSelectView(WhistListView):
    """ Sélection d'une partie """

    class Meta(WhistListView.Options):
        model = WhistPartie

        title = "Sélection / ajout d'une partie"
        url_add = "partie_create"
        url_update = "partie_update"
        # url_delete = "partie_delete"
        url_folder = "partie_folder"
        fields = {
            "name": "Nom de la partie",
            "cartes": "Nombre de cartes max"
        }
        order_by = ('name',)
        url_view = "partie_select"

def partie_folder(request, record_id):
    """ Enregistrement d'une partie dans folder"""
    ctx = get_ctx(request)
    iid = int(record_id)

    # un seul item à la fois
    if iid == ctx["folder_id"]:
        ctx["folder_id"] = None
        ctx["folder_name"] = None
    else:
        obj = get_object_or_404(WhistPartie, id=iid)
        ctx["folder_id"] = obj.id
        ctx["folder_name"] = obj.name

    set_ctx(request, ctx)
    return redirect(ctx["url_view"])

def partie_create(request):
    """ Nouvelle partie """
    title = "Nouvelle Partie"
    ctx = get_ctx(request)
    model = WhistPartie
    url_view = "partie_select"
    if request.POST:
        form = forms.WhistPartieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(url_view)
    else:
        form = forms.WhistPartieForm()
    return render(request, 'whist/whist_create.html', locals())

def partie_update(request, record_id):
    """ Modification d'une partie """
    title = "Modification d'une Partie"
    ctx = get_ctx(request)
    obj = get_object_or_404(WhistPartie, id=record_id)
    model = WhistPartie
    url_view = "partie_select"
    form = forms.WhistPartieForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect(url_view)
    return render(request, "whist/whist_create.html", locals())

def partie_delete(request, record_id):
    """ suppression des parties sélectionnées """
    ctx = get_ctx(request)
    for record_id in ctx["selected"]:
        obj = get_object_or_404(WhistPartie, id=record_id)
        obj.delete()
    ctx["selected"] = []
    set_ctx(request, ctx)
    url_view = "partie_select"
    return redirect(url_view)

"""
    Gestion des participants
"""
class WhistParticipantSelectView(WhistListView):
    """ Liste des participants """

    class Meta(WhistListView.Options):
        model = WhistJoueur
        title = "Sélection des Participants"
        fields = {
            "pseudo": "Nom du joueur",
            "email": "Email"
        }
        order_by = ('pseudo',)
        url_add = "joueur_create"
        url_update = "joueur_update"
        url_join = "participant_join"
        url_view = "participant_select"

    def get_queryset(self):
        """ queryset générique """
        ctx = get_ctx(self.request)
        if 'id' not in self.meta.fields:
            self.meta.fields["id"] = "id"
        self.objs = self.meta.model.objects.all()\
        .filter(**self.meta.filters)\
        .order_by(*self.meta.order_by)\
        .values(*self.meta.fields.keys())
        # Cochage des participants dans la liste des joueurs
        participants = WhistParticipant.objects.all().filter(partie__id__exact=ctx["folder_id"])
        ctx["joined"] = []
        for obj in self.objs:
            for participant in participants:
                if participant.joueur_id == obj["id"]:
                    ctx["joined"].append(obj["id"])

        set_ctx(self.request, ctx)
        return self.objs

def participant_join(request, record_id):
    """ Sélection d'un participant dans la liste des joueurs """
    ctx = get_ctx(request)
    iid = int(record_id)

    if iid in ctx["joined"]:
        participant = WhistParticipant.objects.all().filter(partie_id__exact=ctx["folder_id"], joueur_id__exact=iid)
        participant.delete()
        # compute_ordre() dans post_delete_whist 
        ctx["joined"].remove(iid)
    else:
        participant = WhistParticipant(partie_id=ctx["folder_id"], joueur_id=iid)
        participant.save()
        participant.compute_order()
        ctx["joined"].append(iid)

    set_ctx(request, ctx)
    return redirect(ctx["url_view"])

class WhistParticipantListView(WhistListView):
    """ Tri des participants """

    class Meta(WhistListView.Options):
        model = WhistParticipant
        title = "Ordre des Participants autour de la table"
        fields = {
            "joueur__pseudo": "Nom du joueur",
            "donneur": "Donneur initial",
        }
        order_by = ('order', 'joueur__pseudo')
        url_order = "participant_order"
        url_actions = [
            ("jeu_create", "Initialiser les jeux")
        ]
        url_view = "participant_list"

    def get_queryset(self):
        """ queryset générique """
        ctx = get_ctx(self.request)
        if 'id' not in self.meta.fields:
            self.meta.fields["id"] = "id"
        self.objs = self.meta.model.objects.all()\
        .filter(partie_id=ctx["folder_id"])\
        .order_by(*self.meta.order_by)\
        .values(*self.meta.fields.keys())

        ctx["url_participant_update"] = 'participant_update'
        ctx["action_param"] = 0
        set_ctx(self.request, ctx)
        return self.objs

def participant_update(request, record_id, checked):
    """ Mise à jour du donneur """
    ctx = get_ctx(request)
    iid = int(record_id)

    participants = WhistParticipant.objects.all().filter(partie__id=ctx["folder_id"])
    joueur_id = 0
    for participant in participants:
        if participant.id == iid:
            participant.donneur = int(checked)
            if int(checked) == 1:
                joueur_id = participant.joueur_id
        else:
            participant.donneur = 0
        participant.save()

    # Calcul du donneur sur tous les jeux
    jeux = WhistJeu.objects.all().filter(participant__partie__id=ctx["folder_id"]).order_by('jeu', 'participant__order')
    ijeu = 1
    for jeu in jeux:
        if joueur_id == 0:
            joueur_id = jeu.participant.joueur_id
        if jeu.jeu == ijeu and jeu.participant.joueur_id == joueur_id:
            jeu.donneur = 1
            joueur_id = 0
            ijeu = jeu.jeu + 1
        else:
            jeu.donneur = 0
        jeu.save()

    return redirect(ctx["url_view"])

def participant_order(request, record_id, orientation):
    """ On remonte le joueur dans la liste """
    ctx = get_ctx(request)
    iid = int(record_id)

    participant = get_object_or_404(WhistParticipant, id=iid)
    participant.order += int(orientation) * 3
    participant.save()

    return redirect(ctx["url_view"])

def joueur_create(request):
    """ création d'un joueur """
    title = "Nouveau Joueur"
    ctx = get_ctx(request)
    model = WhistJoueur
    url_view = "participant_select"
    if request.POST:
        form = forms.WhistJoueurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(url_view)
    else:
        form = forms.WhistJoueurForm()
    return render(request, 'whist/whist_create.html', locals())

def joueur_update(request, record_id):
    """ mise à jour d'un joueur """
    title = "Modification d'un Joueur"
    ctx = get_ctx(request)
    model = WhistJoueur
    obj = get_object_or_404(model, id=record_id)
    url_view = "participant_select"
    form = forms.WhistJoueurForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect(url_view)
    return render(request, "whist/whist_create.html", locals())

"""
    Gestion des jeux
"""
class WhistJeuListView(WhistListView):
    """ Liste des jeux """

    class Meta(WhistListView.Options):
        model = WhistJeu
        title = "Faites vos Jeux"
        fields = {
            "donneur": "",
            "participant__joueur__pseudo": "Participant",
            # "jeu": "n° du tour",
            "carte": "Carte",
            "pari": "Pari",
            "real": "Réalisé",
            "points": "Point",
            "score": "Score"
        }
        url_view = "jeu_list"
        url_actions = [
            ("jeu_compute", "Calculer les points")
        ]

    def dispatch(self, request, *args, **kwargs):
        """ dispatch is called when the class instance loads """
        self.sort = kwargs.get('sort', None)
        self.page = kwargs.get('page')
        return super().dispatch(request, args, kwargs)

    def get_queryset(self):
        """ fournir les données à afficher dans la vue """
        ctx = get_ctx(self.request)
        # ajout de la colonne id
        if 'id' not in self.meta.fields:
            self.meta.fields["id"] = "id"
        # prise en compte de la colonne à trier en fonction de sort
        if self.sort == "score":
            ctx["sort"] = "score"

        if self.sort == "participant":
            ctx["sort"] = "participant"

        if ctx["sort"] == "score":
            order_by = ('jeu', '-score',)
        else:
            order_by = ('jeu', 'participant__order',)

        jeux_list = self.meta.model.objects.all()\
        .filter(participant__partie__id__exact=ctx["folder_id"])\
        .order_by(*order_by)\
        .values(*self.meta.fields.keys())

        qparticipant = WhistParticipant.objects.all().filter(partie__id__exact=ctx["folder_id"]).count()
        paginator = Paginator(jeux_list, qparticipant)
        
        self.objs = paginator.get_page(self.page)
        ctx["cartes"] = []
        for pp in range(1, paginator.num_pages + 1):
            if pp <= paginator.num_pages / 2:
                ctx["cartes"].append((pp, pp))
            else:
                ctx["cartes"].append((pp, paginator.num_pages - pp + 1))
        ctx["url_jeu_pari"] = "jeu_pari"
        ctx["url_jeu_real"] = "jeu_real"
        ctx["action_param"] = self.page
        ctx["jeu"] = self.page
        ctx["url_sort"] = 'jeu_sort'
        set_ctx(self.request, ctx)
        return self.objs

def jeu_create(request, id):
    """ création des jeux (tours) de la partie """
    ctx = get_ctx(request)
    jeu = WhistJeu()
    jeu.create_jeux(ctx)

    return redirect("jeu_list", 1)

def jeu_compute(request, jeu_id):
    """ Calcul des points du jeux """
    ctx = get_ctx(request)
    jeux = WhistJeu.objects.all()\
    .filter(participant__partie__id=ctx["folder_id"])\
    .order_by("jeu")
    score = {}
    for jeu in jeux:
        joueur_id = jeu.participant.joueur_id
        if jeu.jeu <= int(jeu_id):
            if jeu.pari == jeu.real:
                jeu.points = 10 + 2 * jeu.pari
            else:
                jeu.points = -10
            score[joueur_id] = score.get(joueur_id, 0) + jeu.points
        jeu.score = score[joueur_id]
        jeu.save()

    return redirect("jeu_list", jeu_id)

def jeu_pari(request, id, choice):
    """ Saisie des paris """
    jeu = get_object_or_404(WhistJeu, id=id)
    jeu.pari = choice
    jeu.save()

    url_view = "jeu_list"
    return redirect(url_view, jeu.jeu)

def jeu_real(request, id, choice):
    """ Saisie du réalisé 0 1 2 """
    jeu = get_object_or_404(WhistJeu, id=id)
    jeu.real = choice
    jeu.save()

    url_view = "jeu_list"
    return redirect(url_view, jeu.jeu)
