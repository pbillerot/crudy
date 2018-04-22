import collections
from django.views.generic import ListView
from .crudy import Crudy

class CrudyListView(ListView):
    """
        Gestion des vues
    """
    context_object_name = "objs"
    template_name = "v_crudy_view.html"
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
        template_name = "v_crudy_view.html"
        application = "CRUDY"
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
        url_return = None
        url_param = ""
        url_back = None
        url_next_page = None # page suivante logique
        whist_carte = None
        # query sur la base
        # liste des champs à afficher dans la vue
        cols = {}
        cols_ordered = []
        cols_list = []

        filters = {} # filtres du query_set
        order_by = () # liste des colonnes à trier

        help_page = None # nom du fichier markdown

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
        self.context["whist_carte"] = self.meta.whist_carte

        # cochage de tous les enregistrements
        if 0 in crudy.selected:
            for obj in self.objs:
                crudy.selected.append(obj["id"])
        # tri des objs dans l'ordre des cols
        crudy.url_view = self.meta.url_view
        crudy.url_back = self.meta.url_back
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
        crudy.url_next_page = self.meta.url_next_page
        crudy.qcols = len(self.meta.cols) -1
        crudy.layout = "view"
        crudy.help_page = self.meta.help_page
        return self.context

    def get_queryset(self):
        """ queryset générique """
        self.objs = self.meta.model.objects.all()\
        .filter(**self.meta.filters)\
        .order_by(*self.meta.order_by)\
        .values(*self.meta.cols_ordered)
        # tri des colonnes si version python 3.5
        self.sort_cols()
        return self.objs

    def sort_cols(self):
        """ Tri des colonnes du dataset self.objs dans le même ordre que cols_ordered """
        objs = []
        for row in self.objs:
            ordered_dict = collections.OrderedDict()
            for col in self.meta.cols_ordered:
                ordered_dict[col] = row[col]
            objs.append(ordered_dict)
        self.objs = objs
        return True

