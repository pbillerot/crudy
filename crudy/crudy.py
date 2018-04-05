# coding: utf-8
""" Gestion du contexte de CRUDY """
import sys

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
    ses = {
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
        "version": "1.12 du 4 avril 2018",
        "add_title": "Ajouter",
        "help_page": None
    }
    request = None
    request_context = None

    def __init__(self, request, app_id="portail"):
        """ Récupération du contexte de la session """
        self.request = request
        self.application = app_id

        # Contexte de la request
        # self.request_context = RequestContext(request)
        # if self.request_context.get("crudy_ctx", None):
        #     self.ses = self.request_context.get("crudy_ctx")
        # else:
        #     self.request_context["crudy_ctx"] = self.ses
        # contexte de la session
        if self.request.session.get("crudy_ses", None):
            self.ses = self.request.session.get("crudy_ses")
        else:
            self.request.session["crudy_ses"] = self.ses
        print("*** ses: ", self.ses)


    def save(self):
        """ Enregistrement du contexte dans la session """
        self.request.session["crudy_ses"] = self.ses

    @property
    def applications(self):
        """ Retourne la liste des applications """
        application_list = []
        for key in self.apps:
            application_list.append((key, self.apps[key]))
        return application_list

    @property
    def application(self):
        return self.apps.get(self.ses.get("app_id"))
    @application.setter
    def application(self, app_id):
        self.ses["app_id"] = app_id
        self.save()
    @property
    def application_help(self):
        return "i_%s_help.md" % self.ses.get("app_id")
    @property
    def application_menu(self):
        return "i_%s_menu.html" % self.ses.get("app_id")

    @property
    def selected(self):
        return self.ses["selected"]
    @selected.setter
    def selected(self, value):
        self.ses["selected"] = value
        self.save()

    @property
    def joined(self):
        return self.ses["joined"]
    @joined.setter
    def joined(self, value):
        self.ses["joined"] = value
        self.save()

    @property
    def folder_id(self):
        return self.ses["folder_id"]
    @folder_id.setter
    def folder_id(self, value):
        print("set folder", value)
        self.ses["folder_id"] = value
        self.save()

    @property
    def folder_name(self):
        return self.ses["folder_name"]
    @folder_name.setter
    def folder_name(self, value):
        self.ses["folder_name"] = value
        self.save()

    @property
    def carte(self):
        return self.ses["carte"]
    @carte.setter
    def carte(self, value):
        self.ses["carte"] = value
        self.save()

    @property
    def cartes(self):
        return self.ses["cartes"]
    @cartes.setter
    def cartes(self, value):
        self.ses["cartes"] = value
        self.save()

    @property
    def jeu(self):
        return self.ses["jeu"]
    @jeu.setter
    def jeu(self, value):
        self.ses["jeu"] = value
        self.save()

    @property
    def url_view(self):
        return self.ses["url_view"]
    @url_view.setter
    def url_view(self, value):
        self.ses["url_view"] = value
        self.save()

    @property
    def url_actions(self):
        return self.ses["url_actions"]
    @url_actions.setter
    def url_actions(self, value):
        self.ses["url_actions"] = value
        self.save()

    @property
    def url_delete(self):
        return self.ses["url_delete"]
    @url_delete.setter
    def url_delete(self, value):
        self.ses["url_delete"] = value
        self.save()

    @property
    def url_return(self):
        return self.ses["url_return"]
    @url_return.setter
    def url_return(self, value):
        self.ses["url_return"] = value
        self.save()

    @property
    def url_back(self):
        return self.ses["url_back"]
    @url_back.setter
    def url_back(self, value):
        self.ses["url_back"] = value
        self.save()

    @property
    def url_join(self):
        return self.ses["url_join"]
    @url_join.setter
    def url_join(self, value):
        self.ses["url_join"] = value
        self.save()

    @property
    def url_folder(self):
        return self.ses["url_folder"]
    @url_folder.setter
    def url_folder(self, value):
        self.ses["url_folder"] = value
        self.save()

    @property
    def sort(self):
        return self.ses["sort"]
    @sort.setter
    def sort(self, value):
        self.ses["sort"] = value
        self.save()

    @property
    def url_jeu_pari(self):
        return self.ses["url_jeu_pari"]
    @url_jeu_pari.setter
    def url_jeu_pari(self, value):
        self.ses["url_jeu_pari"] = value
        self.save()

    @property
    def url_jeu_real(self):
        return self.ses["url_jeu_real"]
    @url_jeu_real.setter
    def url_jeu_real(self, value):
        self.ses["url_jeu_real"] = value
        self.save()

    @property
    def url_participant(self):
        return self.ses["url_participant"]
    @url_participant.setter
    def url_participant(self, value):
        self.ses["url_participant"] = value
        self.save()

    @property
    def url_participant_update(self):
        return self.ses["url_participant_update"]
    @url_participant_update.setter
    def url_participant_update(self, value):
        self.ses["url_participant_update"] = value
        self.save()

    @property
    def action_param(self):
        return self.ses["action_param"]
    @action_param.setter
    def action_param(self, value):
        self.ses["action_param"] = value
        self.save()

    @property
    def url_sort(self):
        return self.ses["url_sort"]
    @url_sort.setter
    def url_sort(self, value):
        self.ses["url_sort"] = value
        self.save()

    @property
    def jeu_current(self):
        return self.ses["jeu_current"]
    @jeu_current.setter
    def jeu_current(self, value):
        self.ses["jeu_current"] = value
        self.save()

    @property
    def qcols(self):
        return self.ses["qcols"]
    @qcols.setter
    def qcols(self, value):
        self.ses["qcols"] = value
        self.save()

    @property
    def is_form_autovalid(self):
        return self.ses["form_autovalid"]
    @is_form_autovalid.setter
    def is_form_autovalid(self, value):
        self.ses["form_autovalid"] = value
        self.save()

    @property
    def message(self):
        return self.ses["message"]
    @message.setter
    def message(self, value):
        self.ses["message"] = value
        self.save()

    @property
    def modified(self):
        return self.ses["modified"]
    @modified.setter
    def modified(self, value):
        self.ses["modified"] = value
        self.save()

    @property
    def version_python(self):
        return (sys.version)

    @property
    def layout(self):
        return self.ses["layout"]
    @layout.setter
    def layout(self, value):
        self.ses["layout"] = value
        self.save()

    @property
    def add_title(self):
        return self.ses["add_title"]
    @add_title.setter
    def add_title(self, value):
        self.ses["add_title"] = value
        self.save()

    @property
    def help_page(self):
        return self.ses["help_page"]
    @help_page.setter
    def help_page(self, value):
        self.ses["help_page"] = value
        self.save()

    @property
    def version(self):
        return self.ses["version"]


