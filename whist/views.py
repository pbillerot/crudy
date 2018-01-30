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

def whist_folder(request, record_id):
    """ Sélection d'un item dans une liste """
    ctx = get_ctx(request)
    iid = int(record_id)

    # un seul item à la fois
    if iid in ctx["selected"]:
        ctx["selected"] = []
        ctx["folder_id"] = None
    else:
        ctx["selected"] = []
        ctx["selected"].append(iid)
        ctx["folder_id"] = iid

    set_ctx(request, ctx)
    return redirect(ctx["view_name"])

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
        url_sorter = None
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
        self.context["url_sorter"] = self.meta.url_sorter
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
            "jeu": "Nombre de jeux"
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
            "jeu": "Nombre de jeux"
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
    Gestion des joueurs
"""
class WhistJoueurListView(WhistListView):
    """ Gestion des joueurs """

    class Meta(WhistListView.Options):
        model = WhistJoueur
        title = "Gestion des Joueurs"
        url_add = "joueur_create"
        url_update = "joueur_update"
        url_delete = "joueur_delete"
        fields = {
            "pseudo": "Joueur",
            "email": "Email"
        }
        order_by = ('pseudo',)

def joueur_create(request):
    """ création d'un joueur """
    title = "Nouveau Joueur"
    ctx = get_ctx(request)
    model = WhistJoueur
    url_return = "joueur_list"
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
    url_return = "joueur_list"
    form = forms.WhistJoueurForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect(url_return)
    return render(request, "whist/whist_create.html", locals())

def joueur_delete(request):
    """ suppression des joueurs sélectionnés """
    ctx = get_ctx(request)
    for id in ctx["selected"]:
        obj = get_object_or_404(WhistJoueur, id=id)
        obj.delete()
    ctx["selected"] = []
    set_ctx(request, ctx)
    url_return = "joueur_list"
    return redirect(url_return)

"""
    Gestion des participants
"""
class WhistParticipantListView(WhistListView):
    """ Liste des participants """

    class Meta(WhistListView.Options):
        model = WhistParticipant
        title = "Liste des Participants"
        fields = {
            "joueur__pseudo": "Pseudo",
            "score": "Score",
        }
        order_by = ('partie', 'joueur')
        url_add = "participant_create"
        url_update = "participant_update"
        url_delete = "participant_delete"

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

def participant_create(request):
    """ création d'un participant """
    title = "Nouveau Participant"
    ctx = get_ctx(request)
    model = WhistParticipant
    url_return = "participant_list"
    if request.POST:
        form = forms.WhistParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(url_return)
    else:
        form = forms.WhistParticipantForm()
    return render(request, 'whist/whist_create.html', locals())

def participant_update(request, record_id):
    """ mise à jour d'un participant """
    title = "Modification d'un Participant"
    ctx = get_ctx(request)
    model = WhistParticipant
    obj = get_object_or_404(model, id=record_id)
    url_return = "joueur_list"
    form = forms.WhistParticipantForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect(url_return)
    return render(request, "whist/whist_create.html", locals())

def participant_delete(request, record_id):
    """ suppression des participants sélectionnés """
    ctx = get_ctx(request)
    for record_id in ctx["selected"]:
        obj = get_object_or_404(WhistParticipant, id=record_id)
        obj.delete()
    ctx["selected"] = []
    set_ctx(request, ctx)
    url_return = "participant_list"
    return redirect(url_return)

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
