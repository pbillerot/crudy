# coding: utf-8
""" Gestion du contexte de CRUDY """

class Crudy():
    ## Dictionnaire des applications
    apps = {
        "portail": {
            "title": "Crudy",
            "logo": "filter_none",
            "menu_title": "Choix des applications",
            "url_name": "p_portail_home",
        },
        "whist": {
            "title": "Whist - Compter les points",
            "logo": "filter_1",
            "menu_title": "Whist",
            "url_name": "p_whist_home",
        },
    }

    # Application en cours
    app = None # alimentée par le constructeur

    # Contexte de la session
    ctx = {
        "selected": [],
        "joined": [],
        "folder_id": None,
        "folder_name": None,
        "carte": [],
        "jeu": None,
        "sort": None,
        "action_param": None,
        "jeu_current": None,
        "url_view": None,
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
    }
    request = None

    def __init__(self, request, app_id="portail"):
        """ Récupération du contexte de la session """
        self.request = request
        if request.session.get("ctx", None):
            self.ctx = request.session["ctx"]
        else:
            request.session["ctx"] = self.ctx
        self.app = self.apps.get(app_id)

    def update_session(self):
        """ Enregistrement du contexte dans la session """
        self.request.session["ctx"] = self.ctx

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

    @property
    def selected(self):
        return self.ctx["selected"]
    @selected.setter
    def selected(self, value):
        self.ctx["selected"] = value

    @property
    def joined(self):
        return self.ctx["joined"]
    @joined.setter
    def joined(self, value):
        self.ctx["joined"] = value

    @property
    def folder_id(self):
        return self.ctx["folder_id"]
    @folder_id.setter
    def folder_id(self, value):
        self.ctx["folder_id"] = value

    @property
    def folder_name(self):
        return self.ctx["folder_name"]
    @folder_name.setter
    def folder_name(self, value):
        self.ctx["folder_name"] = value

    @property
    def carte(self):
        return self.ctx["carte"]
    @carte.setter
    def carte(self, value):
        self.ctx["carte"] = value

    @property
    def cartes(self):
        return self.ctx["cartes"]
    @cartes.setter
    def cartes(self, value):
        self.ctx["cartes"] = value

    @property
    def jeu(self):
        return self.ctx["jeu"]
    @jeu.setter
    def jeu(self, value):
        self.ctx["jeu"] = value

    @property
    def url_view(self):
        return self.ctx["url_view"]
    @url_view.setter
    def url_view(self, value):
        self.ctx["url_view"] = value

    @property
    def url_actions(self):
        return self.ctx["url_actions"]
    @url_actions.setter
    def url_actions(self, value):
        self.ctx["url_actions"] = value

    @property
    def url_delete(self):
        return self.ctx["url_delete"]
    @url_delete.setter
    def url_delete(self, value):
        self.ctx["url_delete"] = value

    @property
    def url_return(self):
        return self.ctx["url_return"]
    @url_return.setter
    def url_return(self, value):
        self.ctx["url_return"] = value

    @property
    def url_join(self):
        return self.ctx["url_join"]
    @url_join.setter
    def url_join(self, value):
        self.ctx["url_join"] = value

    @property
    def url_folder(self):
        return self.ctx["url_folder"]
    @url_folder.setter
    def url_folder(self, value):
        self.ctx["url_folder"] = value

    @property
    def sort(self):
        return self.ctx["sort"]
    @sort.setter
    def sort(self, value):
        self.ctx["sort"] = value

    @property
    def url_jeu_pari(self):
        return self.ctx["url_jeu_pari"]
    @url_jeu_pari.setter
    def url_jeu_pari(self, value):
        self.ctx["url_jeu_pari"] = value

    @property
    def url_jeu_real(self):
        return self.ctx["url_jeu_real"]
    @url_jeu_real.setter
    def url_jeu_real(self, value):
        self.ctx["url_jeu_real"] = value

    @property
    def url_participant(self):
        return self.ctx["url_participant"]
    @url_participant.setter
    def url_participant(self, value):
        self.ctx["url_participant"] = value

    @property
    def url_participant_update(self):
        return self.ctx["url_participant_update"]
    @url_participant_update.setter
    def url_participant_update(self, value):
        self.ctx["url_participant_update"] = value

    @property
    def action_param(self):
        return self.ctx["action_param"]
    @action_param.setter
    def action_param(self, value):
        self.ctx["action_param"] = value

    @property
    def url_sort(self):
        return self.ctx["url_sort"]
    @url_sort.setter
    def url_sort(self, value):
        self.ctx["url_sort"] = value

    @property
    def jeu_current(self):
        return self.ctx["jeu_current"]
    @jeu_current.setter
    def jeu_current(self, value):
        self.ctx["jeu_current"] = value

    @property
    def qcols(self):
        return self.ctx["qcols"]
    @qcols.setter
    def qcols(self, value):
        self.ctx["qcols"] = value
