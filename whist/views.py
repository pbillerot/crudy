"""
    Traitement des VUES
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import resolve
from .models import WhistPartie, WhistJoueur, WhistParticipant, WhistJeu
from . import forms
from django.views.generic import ListView, DetailView

def get_ctx(request):
    """ Obtenir le ctx de la session """
    if not request.session.get("ctx", False):
        ctx = {
            "title": "JEU DU WHIST",
            "selected": [],
            "view_name": None
        }
        request.session["ctx"] = ctx
    return request.session["ctx"]
def set_ctx(request, ctx):
    """ Mettre à jour le ctx de la session """
    request.session["ctx"] = ctx

def whist_proto(request):
    return render(request, 'whist/whist_proto.html', {})
def whist_home(request):
    ctx = get_ctx(request)
    model = WhistPartie
    return render(request, 'whist/whist_home.html', locals())

def whist_select(request, id):
    """ Sélection/désélection d'un élément dans une liste """
    ctx = get_ctx(request)
    iid = int(id)

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
    #
    # PARAMETRES à personnaliser dans les classes filles
    #
    #
    context = None
    objs = None
    # urls définis dans ursl.py
    url_add = None
    url_update = None
    url_delete = None
    # query sur la base
    fields = [] # liste des champs à afficher dans la vue
    filters = {} # filtres du query_set
    order_by = () # liste des colonnes à trier
    # Rendu
    with_selector = False # avec une coche pour sélectionner la ligne
    search_in = () # liste des colonnes objet de la recherche, un champ recherche sera présenté

    def get_context_data(self, **kwargs):
        """ fourniture des données à la vue """
        self.context = super().get_context_data(**kwargs)
        ctx = get_ctx(self.request)
        url = resolve(self.request.path)
        # raz selected si nouvelle vue
        if ctx["view_name"] != url.view_name:
            ctx["selected"] = []
        self.context["model"] = self.model
        self.context["fields"] = []
        # on range les champs dans context["fields"] dans le m ordre que les objs
        fields_obj = self.model._meta.get_fields(include_hidden=True)
        for field_name in self.fields:
            for field in fields_obj:
                if field.name == field_name:
                    self.context["fields"].append(field)
        self.context["url_add"] = self.url_add
        self.context["url_update"] = self.url_update
        self.context["url_delete"] = self.url_delete
        self.context["url_select"] = "whist_select" # nom de la vue dans urls.py
        self.context["select_all"] = "select_all" # pour tester une variable plutôt qu'une valeur statique dans .html
        self.context["with_selector"] = self.with_selector
        self.context["search_in"] = self.search_in
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
        if 'id' not in self.fields:
            self.fields.append("id")
        self.objs = self.model.objects.all()\
        .filter(**self.filters)\
        .order_by(*self.order_by)\
        .values(*self.fields)
        return self.objs

"""
    Gestion des parties
"""
class WhistPartieListView(WhistListView):
    """ liste des parties """
    model = WhistPartie
    url_add = "partie_create"
    url_update = "partie_update"
    url_delete = "partie_delete"
    with_selector = True
    fields = ['name', 'date', 'jeu']
    filtersx = {
        "name__icontains": "2017"
    }
    order_by = ('name',)
    search_in = ('name',)

class WhistParticipantListView(WhistListView):
    """
        Gestion des participants
    """
    model = WhistParticipant
    fields = ['partie', 'joueur', 'score']
    order_by = ('partie', 'joueur')

class WhistJeuListView(WhistListView):
    """
        Gestion des jeux
    """
    model = WhistJeu
    fields = ['partie', 'joueur', 'jeu', 'pari', 'real', 'points', 'score']
    order_by = ('partie', 'jeu', '-points')
    with_selector = True

def partie_create(request):
    ctx = get_ctx(request)
    model = WhistPartie
    if request.POST:
        form = forms.WhistPartieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('partie_list')
    else:
        form = forms.WhistPartieForm()
    return render(request, 'whist/whist_create.html', locals())

def partie_update(request, id):
    ctx = get_ctx(request)
    obj = get_object_or_404(WhistPartie, id=id)
    model = WhistPartie
    form = forms.WhistPartieForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('partie_list')
    return render(request, "whist/whist_create.html", locals())

def partie_delete(request, id):
    obj = get_object_or_404(WhistPartie, id=id)
    obj.delete()
    return redirect('partie_list')

"""
    Gestion des joueurs
"""
class WhistJoueurListView(WhistListView):
    """ Liste des joueurs """
    model = WhistJoueur
    url_add = "joueur_create"
    url_update = "joueur_update"
    url_delete = "joueur_delete"
    fields = ['pseudo', 'email']
    order_by = ('pseudo',)

def joueur_create(request):
    """ création d'un joueur """
    ctx = get_ctx(request)
    model = WhistJoueur
    if request.POST:
        form = forms.WhistJoueurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('joueur_list')
    else:
        form = forms.WhistJoueurForm()
    return render(request, 'whist/whist_create.html', locals())

def joueur_update(request, id):
    """ mise à jour d'un joueur """
    ctx = get_ctx(request)
    model = WhistJoueur
    obj = get_object_or_404(model, id=id)
    form = forms.WhistJoueurForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        return redirect('joueur_list')
    return render(request, "whist/whist_create.html", locals())

def joueur_delete(request, id):
    """ suppression d'un joueur """
    obj = get_object_or_404(WhistJoueur, id=id)
    obj.delete()
    return redirect('joueur_list')
