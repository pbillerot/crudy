# coding: utf-8
""" Gestion du contexte de CRUDY """

class Crudy():
    ## Dictionnaire des applications
    apps = {
        "portail": {
            "title": "Crudy",
            "resume": """Le framework tant attendu""",
            "logo": "filter_none",
            "menu_title": "Choix des applications",
            "url_name": "p_portail_home",
            "image": "images/portail/carte.png",
        },
        "whist": {
            "title": "Whist",
            "resume": """Compter les points du Whist""",
            "logo": "filter_1",
            "menu_title": "Whist",
            "url_name": "p_whist_home",
            "image": "images/whist/Brewtnall_The-Whist-Party.jpg",
        },
        "tarot": {
            "title": "Tarot",
            "resume": """Compter les points du jeu de Tarot""",
            "logo": "filter_3",
            "menu_title": "Tarot",
            "url_name": "p_tarot_home",
            "image": "images/tarot/tarot2.jpg",
        },
    }

    # Application en cours
    app = None # alimentée par le constructeur

    # Contexte de la session
    ses = {
        "folder_id": None,
        "folder_name": None,
        "jeu": 0,
        "jeu_current": 0,
        "url_view": None,
        "sort": None,
    }
    # Contexte de la request
    ctx = {
        "selected": [],
        "joined": [],
        "carte": [],
        "action_param": None,
        "url_return": None,
        "url_actions": None,
        "url_delete": None,
        "url_jeu_pari": None,
        "url_jeu_real": None,
        "url_participant": None,
        "url_participant_update": None,
        "url_sort": None,
        "url_join": None,
        "url_folder": None,
        "qcols": None,
        "form_autovalid": False,
        "message": None
    }
    request = None
    request_context = None

    def __init__(self, request, app_id="portail"):
        """ Récupération du contexte de la session """
        self.request = request
        self.app = self.apps.get(app_id)

        # Contexte de la request
        # self.request_context = RequestContext(request)
        # if self.request_context.get("crudy_ctx", None):
        #     self.ctx = self.request_context.get("crudy_ctx")
        # else:
        #     self.request_context["crudy_ctx"] = self.ctx
        if self.request.session.get("crudy_ctx", None):
            self.ses = self.request.session.get("crudy_ctx")
        else:
            self.request.session["crudy_ctx"] = self.ctx
        # contexte de la session
        if self.request.session.get("crudy_ses", None):
            self.ses = self.request.session.get("crudy_ses")
        else:
            self.request.session["crudy_ses"] = self.ses

    def save(self):
        """ Enregistrement du contexte dans la session """
        self.request.session["crudy_ses"] = self.ses
        self.request.session["crudy_ctx"] = self.ctx
        # self.request_context["crudy_ctx"] = self.ctx

    @property
    def applications(self):
        """ Retourne la liste des applications """
        application_list = []
        for key in self.apps:
            application_list.append((key, self.apps[key]))
        return application_list

    @property
    def application(self):
        return self.app
    @application.setter
    def application(self, app_id):
        self.app = self.apps.get(app_id)
        self.save()

    @property
    def selected(self):
        return self.ctx["selected"]
    @selected.setter
    def selected(self, value):
        self.ctx["selected"] = value
        self.save()

    @property
    def joined(self):
        return self.ctx["joined"]
    @joined.setter
    def joined(self, value):
        self.ctx["joined"] = value
        self.save()

    @property
    def folder_id(self):
        return self.ses["folder_id"]
    @folder_id.setter
    def folder_id(self, value):
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
        return self.ctx["carte"]
    @carte.setter
    def carte(self, value):
        self.ctx["carte"] = value
        self.save()

    @property
    def cartes(self):
        return self.ctx["cartes"]
    @cartes.setter
    def cartes(self, value):
        self.ctx["cartes"] = value
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
        return self.ctx["url_actions"]
    @url_actions.setter
    def url_actions(self, value):
        self.ctx["url_actions"] = value
        self.save()

    @property
    def url_delete(self):
        return self.ctx["url_delete"]
    @url_delete.setter
    def url_delete(self, value):
        self.ctx["url_delete"] = value
        self.save()

    @property
    def url_return(self):
        return self.ctx["url_return"]
    @url_return.setter
    def url_return(self, value):
        self.ctx["url_return"] = value
        self.save()

    @property
    def url_join(self):
        return self.ctx["url_join"]
    @url_join.setter
    def url_join(self, value):
        self.ctx["url_join"] = value
        self.save()

    @property
    def url_folder(self):
        return self.ctx["url_folder"]
    @url_folder.setter
    def url_folder(self, value):
        self.ctx["url_folder"] = value
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
        return self.ctx["url_jeu_pari"]
    @url_jeu_pari.setter
    def url_jeu_pari(self, value):
        self.ctx["url_jeu_pari"] = value
        self.save()

    @property
    def url_jeu_real(self):
        return self.ctx["url_jeu_real"]
    @url_jeu_real.setter
    def url_jeu_real(self, value):
        self.ctx["url_jeu_real"] = value
        self.save()

    @property
    def url_participant(self):
        return self.ctx["url_participant"]
    @url_participant.setter
    def url_participant(self, value):
        self.ctx["url_participant"] = value
        self.save()

    @property
    def url_participant_update(self):
        return self.ctx["url_participant_update"]
    @url_participant_update.setter
    def url_participant_update(self, value):
        self.ctx["url_participant_update"] = value
        self.save()

    @property
    def action_param(self):
        return self.ctx["action_param"]
    @action_param.setter
    def action_param(self, value):
        self.ctx["action_param"] = value
        self.save()

    @property
    def url_sort(self):
        return self.ctx["url_sort"]
    @url_sort.setter
    def url_sort(self, value):
        self.ctx["url_sort"] = value
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
        return self.ctx["qcols"]
    @qcols.setter
    def qcols(self, value):
        self.ctx["qcols"] = value
        self.save()

    @property
    def is_form_autovalid(self):
        return self.ctx["form_autovalid"]
    @is_form_autovalid.setter
    def is_form_autovalid(self, value):
        self.ctx["form_autovalid"] = value
        self.save()

    @property
    def message(self):
        return self.ctx["message"]
    @message.setter
    def message(self, value):
        self.ctx["message"] = value
        self.save()
