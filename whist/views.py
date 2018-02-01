"""
    Traitement des VUES
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import resolve
from .models import WhistPartie, WhistJoueur, WhistParticipant, WhistJeu
from . import forms
from django.views.generic import ListView

def get_ctx(request):
    """ Obtenir le ctx de la session """
    if not request.session.get("ctx", False):
        ctx = {
            "title": "JEU DU WHIST",
            "selected": [],
            "joined": [],
            "view_name": None,
            "folder_id": None,
            "folder_name": None,
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
    ctx["view_name"] = ""
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
    return redirect(ctx["view_name"])

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
        url_ascend = None
        url_descend = None
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
        if ctx["view_name"] != url.view_name:
            ctx["selected"] = []
        self.context["model"] = self.model
        self.context["title"] = self.meta.title
        self.context["url_add"] = self.meta.url_add
        self.context["url_update"] = self.meta.url_update
        self.context["url_delete"] = self.meta.url_delete
        self.context["url_select"] = self.meta.url_select
        self.context["url_folder"] = self.meta.url_folder
        self.context["url_ascend"] = self.meta.url_ascend
        self.context["url_descend"] = self.meta.url_descend
        self.context["url_join"] = self.meta.url_join
        self.context["search_in"] = self.meta.search_in
        # Récupération des fields correspondants aux objs
        self.context["fields"] = [title for title in self.meta.fields.values()]
        # cochage des enregistrements sélectionnés
        if 0 in ctx["selected"]:
            for obj in self.objs:
                ctx["selected"].append(obj["id"])
        ctx["view_name"] = url.view_name
        set_ctx(self.request, ctx)
        self.context["ctx"] = ctx
        return self.context

    def get_queryset(self):
        """ queryset générique """
        ctx = get_ctx(self.request)
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
    return redirect(ctx["view_name"])

def partie_create(request):
    """ Nouvelle partie """
    title = "Nouvelle Partie"
    ctx = get_ctx(request)
    model = WhistPartie
    url_return = "partie_select"
    if request.POST:
        form = forms.WhistPartieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(url_return)
    else:
        form = forms.WhistPartieForm()
    return render(request, 'whist/whist_create.html', locals())

def partie_update(request, record_id):
    """ Modification d'une partie """
    title = "Modification d'une Partie"
    ctx = get_ctx(request)
    obj = get_object_or_404(WhistPartie, id=record_id)
    model = WhistPartie
    url_return = "partie_select"
    form = forms.WhistPartieForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect(url_return)
    return render(request, "whist/whist_create.html", locals())

def partie_delete(request, record_id):
    """ suppression des parties sélectionnées """
    ctx = get_ctx(request)
    for record_id in ctx["selected"]:
        obj = get_object_or_404(WhistPartie, id=record_id)
        obj.delete()
    ctx["selected"] = []
    set_ctx(request, ctx)
    url_return = "partie_select"
    return redirect(url_return)

"""
    Gestion des participants
"""
class WhistParticipantListView(WhistListView):
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

        return self.objs

class WhistParticipantOrderView(WhistListView):
    """ Tri des participants """

    class Meta(WhistListView.Options):
        model = WhistParticipant
        title = "Ordre des Participants autour de la table"
        fields = {
            "joueur__pseudo": "Nom du joueur",
            "order": "Ordre",
        }
        order_by = ('order', 'joueur__pseudo')
        url_ascend = "participant_ascend"
        url_descend = "participant_descend"

    def get_queryset(self):
        """ queryset générique """
        ctx = get_ctx(self.request)
        if 'id' not in self.meta.fields:
            self.meta.fields["id"] = "id"
        self.objs = self.meta.model.objects.all()\
        .filter(partie_id__exact=ctx["folder_id"])\
        .order_by(*self.meta.order_by)\
        .values(*self.meta.fields.keys())
        return self.objs

def participant_ascend(request, record_id):
    """ On remonte le joueur dans la liste """
    ctx = get_ctx(request)
    iid = int(record_id)

    participant = get_object_or_404(WhistParticipant, id=iid)
    participant.order -= 3
    participant.save()

    set_ctx(request, ctx)
    return redirect(ctx["view_name"])

def participant_descend(request, record_id):
    """ On descend le joueur dans la liste """
    ctx = get_ctx(request)
    iid = int(record_id)

    participant = get_object_or_404(WhistParticipant, id=iid)
    participant.order += 3
    participant.save()

    set_ctx(request, ctx)
    return redirect(ctx["view_name"])

def participant_join(request, record_id):
    """ Sélection d'un participant dans la liste des joueurs """
    ctx = get_ctx(request)
    iid = int(record_id)

    if iid in ctx["joined"]:
        participant = WhistParticipant.objects.all().filter(partie_id__exact=ctx["folder_id"], joueur_id__exact=iid)
        participant.delete()
        ctx["joined"].remove(iid)
    else:
        participant = WhistParticipant(partie_id=ctx["folder_id"], joueur_id=iid)
        participant.save()
        ctx["joined"].append(iid)

    set_ctx(request, ctx)
    return redirect(ctx["view_name"])

def joueur_create(request):
    """ création d'un joueur """
    title = "Nouveau Joueur"
    ctx = get_ctx(request)
    model = WhistJoueur
    url_return = "participant_list"
    if request.POST:
        form = forms.WhistJoueurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(url_return)
    else:
        form = forms.WhistJoueurForm()
    return render(request, 'whist/whist_create.html', locals())

def joueur_update(request, record_id):
    """ mise à jour d'un joueur """
    title = "Modification d'un Joueur"
    ctx = get_ctx(request)
    model = WhistJoueur
    obj = get_object_or_404(model, id=record_id)
    url_return = "participant_list"
    form = forms.WhistJoueurForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect(url_return)
    return render(request, "whist/whist_create.html", locals())

"""
    Gestion des jeux
"""
class WhistJeuListView(WhistListView):
    """ Liste des jeux """

    class Meta(WhistListView.Options):
        model = WhistJeu
        title = "Liste des Jeux"
        fields = {
            # "partie__name": "Partie",
            "joueur__pseudo": "Nom du joueur",
            "jeu": "N° du jeu",
            "pari": "Pari",
            "real": "Réalisé",
            "points": "Points",
            "score": "Score"
        }
        order_by = ('partie', 'jeu', '-points')

    def get_queryset(self):
        """ fournir les données à afficher dans la vue """
        ctx = get_ctx(self.request)
        if 'id' not in self.meta.fields:
            self.meta.fields["id"] = "id"
        self.objs = self.meta.model.objects.all()\
        .filter(partie__id__exact=ctx["folder_id"])\
        .order_by(*self.meta.order_by)\
        .values(*self.meta.fields.keys())
        return self.objs
