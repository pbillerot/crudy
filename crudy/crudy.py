# coding: utf-8
""" Gestion du contexte de CRUDY """
import sys
CRUDY_VERSION = "1.22 du 13 avril 2018"

class Crudy():
    ## Dictionnaire des applications
    apps = {
        "portail": {
            "id": "portail",
            "title": "Tapis Vert",
            "resume": """L'outil pour compter les points des jeux de cartes""",
            "logo": "filter_none",
            "menu_title": "Choix des applications",
            "url_name": "p_portail_home",
            "image": "images/portail/carte.png",
        },
        "whist": {
            "id": "whist",
            "title": "Tapis Vert pour le Whist",
            "resume": """Compter les points du Whist""",
            "logo": "filter_1",
            "menu_title": "Whist",
            "url_name": "p_whist_home",
            "image": "images/whist/Brewtnall_The-Whist-Party.jpg",
        },
        "tarot": {
            "id": "tarot",
            "title": "Tapis Vert pour le Tarot",
            "resume": """Compter les points du Tarot""",
            "logo": "filter_3",
            "menu_title": "Tarot",
            "url_name": "p_tarot_home",
            "image": "images/tarot/tarot2.jpg",
            "menu": [
                # Libellé du menu, icone, url_name, paramètre(s) url
                ("Choix des Participants", "group", "v_tarot_participant_select", ""),
                ("Ordonner les Participants", "sort", "v_tarot_participant_list", ""),
                ("Faites vos jeux", "video_library", "v_tarot_jeu_list", "1"),
            ]
        },
    }

    # Contexte de la session
    ctx = {
        "app_id": None,
        "folder_id": None,
        "folder_name": None,
        "jeu": 0,
        "jeu_current": 0,
        "url_view": None,
        "sort": None,
        "url_return": None,
        #
        "selected": [],
        "joined": [],
        "carte": [],
        "action_param": None,
        "url_actions": None,
        "url_delete": None,
        "url_jeu_pari": None,
        "url_jeu_real": None,
        "url_participant": None,
        "url_participant_update": None,
        "url_sort": None,
        "url_join": None,
        "url_folder": None,
        "url_back": None,
        "qcols": None,
        "form_autovalid": False,
        "message": None,
        "modified": False,
        "layout": None, # portail, help, view, form
        "add_title": "Ajouter",
        "help_page": None
    }
    request = None
    request_context = None

    def __init__(self, request, app_id="portail"):
        """ Récupération du contexte de la session """
        self.request = request

        # Contexte de la request
        # self.request_context = RequestContext(request)
        # if self.request_context.get("crudy_ctx", None):
        #     self.request.session["crudy_ses") = self.request_context.get("crudy_ctx")
        # else:
        #     self.request_context["crudy_ctx") = self.request.session["crudy_ses")
        # contexte de la session

        # print("request:   ", request.COOKIES)
        # print("session:   ", request.user, request.session)
        # print("folder :   ", request.session.get("crudy_ses", {"folder_name": None}).get("folder_name"))
        # if not self.request.session.get("crudy_ses", None):
        #     self.request.session["crudy_ses"] = self.ctx.copy()

        self.application = app_id

    def read(self, key):
        """ Lecture d'une variable dans le contexte de la session """
        # print("read  :   ", self.request.user, self.request.session, key, self.request.session.get(key))
        return self.request.session.get(key)

    def write(self, key, value):
        """ Enregistrement d'une variable dans le contexte de la session """
        self.request.session[key] = value
        # print("write  :   ", self.request.user, self.request.session, key, value, self.request.session.get(key))

    @property
    def applications(self):
        """ Retourne la liste des applications """
        application_list = []
        for key in self.apps:
            application_list.append((key, self.apps[key]))
        return application_list

    @property
    def application(self):
        return self.apps.get(self.read("app_id"))
    @application.setter
    def application(self, value):
        self.write("app_id", value)
    @property
    def application_help(self):
        return "i_%s_help.md" % self.read("app_id")
    @property
    def application_menu(self):
        return "i_%s_menu.html" % self.read("app_id")

    @property
    def selected(self):
        return self.read("selected")
    @selected.setter
    def selected(self, value):
        self.write("selected", value)


    @property
    def joined(self):
        return self.read("joined")
    @joined.setter
    def joined(self, value):
        self.write("joined", value)


    @property
    def folder_id(self):
        return self.read("folder_id")
    @folder_id.setter
    def folder_id(self, value):
        self.write("folder_id", value)


    @property
    def folder_name(self):
        return self.read("folder_name")
    @folder_name.setter
    def folder_name(self, value):
        self.write("folder_name", value)


    @property
    def carte(self):
        return self.read("carte")
    @carte.setter
    def carte(self, value):
        self.write("carte", value)


    @property
    def cartes(self):
        return self.read("cartes")
    @cartes.setter
    def cartes(self, value):
        self.write("cartes", value)


    @property
    def jeu(self):
        return self.read("jeu")
    @jeu.setter
    def jeu(self, value):
        self.write("jeu", value)


    @property
    def url_view(self):
        return self.read("url_view")
    @url_view.setter
    def url_view(self, value):
        self.write("url_view", value)


    @property
    def url_actions(self):
        return self.read("url_actions")
    @url_actions.setter
    def url_actions(self, value):
        self.write("url_actions", value)


    @property
    def url_delete(self):
        return self.read("url_delete")
    @url_delete.setter
    def url_delete(self, value):
        self.write("url_delete", value)


    @property
    def url_return(self):
        return self.read("url_return")
    @url_return.setter
    def url_return(self, value):
        self.write("url_return", value)


    @property
    def url_back(self):
        return self.read("url_back")
    @url_back.setter
    def url_back(self, value):
        self.write("url_back", value)


    @property
    def url_join(self):
        return self.read("url_join")
    @url_join.setter
    def url_join(self, value):
        self.write("url_join", value)


    @property
    def url_folder(self):
        return self.read("url_folder")
    @url_folder.setter
    def url_folder(self, value):
        self.write("url_folder", value)


    @property
    def sort(self):
        return self.read("sort")
    @sort.setter
    def sort(self, value):
        self.write("sort", value)


    @property
    def url_jeu_pari(self):
        return self.read("url_jeu_pari")
    @url_jeu_pari.setter
    def url_jeu_pari(self, value):
        self.write("url_jeu_pari", value)


    @property
    def url_jeu_real(self):
        return self.read("url_jeu_real")
    @url_jeu_real.setter
    def url_jeu_real(self, value):
        self.write("url_jeu_real", value)


    @property
    def url_participant(self):
        return self.read("url_participant")
    @url_participant.setter
    def url_participant(self, value):
        self.write("url_participant", value)


    @property
    def url_participant_update(self):
        return self.read("url_participant_update")
    @url_participant_update.setter
    def url_participant_update(self, value):
        self.write("url_participant_update", value)


    @property
    def action_param(self):
        return self.read("action_param")
    @action_param.setter
    def action_param(self, value):
        self.write("action_param", value)


    @property
    def url_sort(self):
        return self.read("url_sort")
    @url_sort.setter
    def url_sort(self, value):
        self.write("url_sort", value)


    @property
    def jeu_current(self):
        return self.read("jeu_current")
    @jeu_current.setter
    def jeu_current(self, value):
        self.write("jeu_current", value)


    @property
    def qcols(self):
        return self.read("qcols")
    @qcols.setter
    def qcols(self, value):
        self.write("qcols", value)


    @property
    def is_form_autovalid(self):
        return self.read("form_autovalid")
    @is_form_autovalid.setter
    def is_form_autovalid(self, value):
        self.write("form_autovalid", value)


    @property
    def message(self):
        return self.read("message")
    @message.setter
    def message(self, value):
        self.write("message", value)


    @property
    def modified(self):
        return self.read("modified")
    @modified.setter
    def modified(self, value):
        self.write("modified", value)


    @property
    def version_python(self):
        return (sys.version)

    @property
    def layout(self):
        return self.read("layout")
    @layout.setter
    def layout(self, value):
        self.write("layout", value)


    @property
    def add_title(self):
        return self.read("add_title")
    @add_title.setter
    def add_title(self, value):
        self.write("add_title", value)


    @property
    def help_page(self):
        return self.read("help_page")
    @help_page.setter
    def help_page(self, value):
        self.write("help_page", value)


    @property
    def version(self):
        return CRUDY_VERSION


