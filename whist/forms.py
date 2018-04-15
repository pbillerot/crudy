from django import forms
from .models import WhistPartie, WhistJoueur, WhistParticipant, WhistJeu
from crudy.crudy import Crudy
from crudy.forms import CrudyForm

class WhistPartieForm(CrudyForm):
    """ Création / mise à jour d'une partie """
    class Meta:
        model = WhistPartie
        fields = ['name', 'cartes']
        readonly_fields = ()
        widgets = {
            'name': forms.TextInput(attrs={
                'type': 'text',
                'maxlength': 15,
                "required": "required",
                "autofocus": "autofocus"
            }),
            'cartes': forms.TextInput(attrs={
                'type': 'text',
                'pattern': "[456789]",
            }),
        }
    # CTR
    def clean_cartes(self):
        cartes = self.cleaned_data['cartes']
        if cartes < 4:
            raise forms.ValidationError("Le nombre de carte doit être supérieur à 3")
        return cartes  # Ne pas oublier de renvoyer le contenu du champ traité

    def clean_name(self):
        field = self.cleaned_data['name']
        return field.upper()  # Ne pas oublier de renvoyer le contenu du champ traité

class WhistJoueurForm(CrudyForm):
    """ Création / mise à jour d'un joueur """
    class Meta:
        model = WhistJoueur
        fields = ['pseudo']
        widgets = {
            'pseudo': forms.TextInput(attrs={'type': 'text', 'maxlength': 15, "required": "required", "autofocus": "autofocus"}),
            # 'email': forms.TextInput(attrs={'type': 'email'}),
        }
        readonly_fields = ()

    def clean_pseudo(self):
        field = self.cleaned_data['pseudo']
        return field.upper()  # Ne pas oublier de renvoyer le contenu du champ traité

class WhistJeuPariForm(CrudyForm):
    """ Saisie du pari dun joueur """

    class Meta:
        model = WhistJeu
        fields = ['pari']
        widgets = {
            'pari': forms.RadioSelect(attrs={'type': 'radio',"autofocus": "autofocus"})
        }
        readonly_fields = ()

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

class WhistJeuRealForm(CrudyForm):
    """ Saisie du réalisé dun joueur """

    class Meta:
        model = WhistJeu
        fields = ['real']
        widgets = {
            'real': forms.RadioSelect(attrs={'type': 'radio'})
        }
        readonly_fields = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        crudy = Crudy(self.request, "whist")
        whistJeu = kwargs["instance"]
        choices = []
        for i in range(0, whistJeu.carte + 1):
            choices.append((i, "%s pli" % (i,)))
        self.fields['real'].choices = choices
        self.fields['real'].label = ""
