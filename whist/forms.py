# coding: utf-8
from django import forms
from .models import WhistPartie, WhistJoueur, WhistParticipant, WhistJeu
from crudy.crudy import Crudy

class WhistForm(forms.ModelForm):

    class Meta:
        model = None
        fields = []
        readonly_fields = ()
        url_delete = ""
        is_form_autovalid = False

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(WhistForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in self.Meta.readonly_fields:
                field.widget.attrs['disabled'] = 'true'
                field.required = False
        crudy = Crudy(self.request, "whist")
        crudy.url_delete = self.Meta.url_delete
        crudy.is_form_autovalid = self.Meta.is_form_autovalid
        crudy.save()

    def clean(self):
        cleaned_data = super(WhistForm, self).clean()
        for field in self.Meta.readonly_fields:
            cleaned_data[field] = getattr(self.instance, field)
        return cleaned_data

class WhistPartieForm(WhistForm):
    """ Création / mise à jour d'une partie """
    class Meta:
        model = WhistPartie
        is_form_autovalid = False
        fields = ['name', 'cartes']
        readonly_fields = ()
        widgets = {
            'name': forms.TextInput(attrs={
                'type': 'text',
                'maxlength': 15,
                "required": "required"
            }),
            'carte': forms.TextInput(attrs={
                'type': 'number',
                'maxlength': 15,
            }),
        }
        url_delete = "f_partie_delete"
    # CTR
    # def clean_jeu(self):
    #     jeu = self.cleaned_data['cartes']
    #     if jeu < 3:
    #         raise forms.ValidationError("Le nombre de jeu de la partie doit être supérieur à 3")
    #     return jeu  # Ne pas oublier de renvoyer le contenu du champ traité

    # def clean_name(self):
    #     name = self.cleaned_data['name']
    #     if not name:
    #         raise forms.ValidationError("Le nom est obligatoire")
    #     return name  # Ne pas oublier de renvoyer le contenu du champ traité

    # def clean(self):
    #     cleaned_data = super(WhistPartieForm, self).clean()
    #     # if self.errors:
    #     #     raise forms.ValidationError("Corrigez les erreurs suivantes.")
    #     # name = cleaned_data.get('name')
    #     # err = self.errors
    #     return cleaned_data  # N'oublions pas de renvoyer les données si tout est OK

class WhistJoueurForm(WhistForm):
    """ Création / mise à jour d'un joueur """
    class Meta:
        model = WhistJoueur
        is_form_autovalid = False
        fields = ['pseudo', 'email']
        widgets = {
            'pseudo': forms.TextInput(attrs={'type': 'text', 'maxlength': 15, "required": "required"}),
            'email': forms.TextInput(attrs={'type': 'email'}),
        }
        readonly_fields = ()
        url_delete = "f_joueur_delete"

    # def clean_pseudo(self):
    #     pseudo = self.cleaned_data['pseudo']
    #     if not pseudo:
    #         raise forms.ValidationError("Le pseudo est obligatoire")
    #     return pseudo  # Ne pas oublier de renvoyer le contenu du champ traité

class WhistJeuPariForm(WhistForm):
    """ Saisie du pari dun joueur """

    class Meta:
        model = WhistJeu
        is_form_autovalid = True
        fields = ['pari']
        widgets = {
            'pari': forms.RadioSelect(attrs={'type': 'radio'})
        }
        readonly_fields = ()
        url_delete = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        crudy = Crudy(self.request, "whist")
        whistJeu = kwargs["instance"]
        # nre de plis demandés
        plis = 0
        for jeu in WhistJeu.objects.all().filter(participant__partie_id=crudy.folder_id, jeu=whistJeu.jeu):
            if jeu.donneur != 1:
                plis += jeu.pari
        choices = []
        for i in range(0, whistJeu.carte + 1):
            if whistJeu.carte - plis == i and whistJeu.donneur == 1:
                continue
            choices.append((i, "%s pli" % (i,)))
        self.fields['pari'].choices = choices
        self.fields['pari'].label = ""

class WhistJeuRealForm(WhistForm):
    """ Saisie du réalisé dun joueur """

    class Meta:
        model = WhistJeu
        is_form_autovalid = True
        fields = ['real']
        widgets = {
            'real': forms.RadioSelect(attrs={'type': 'radio'})
        }
        readonly_fields = ()
        url_delete = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        crudy = Crudy(self.request, "whist")
        whistJeu = kwargs["instance"]
        choices = []
        for i in range(0, whistJeu.carte + 1):
            choices.append((i, "%s pli" % (i,)))
        self.fields['real'].choices = choices
        self.fields['real'].label = ""
