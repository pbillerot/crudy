# coding: utf-8
from django import forms
from .models import TarotPartie, TarotJoueur, TarotParticipant, TarotJeu
from crudy.crudy import Crudy

class TarotForm(forms.ModelForm):

    class Meta:
        model = None
        fields = []
        readonly_fields = ()

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(TarotForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in self.Meta.readonly_fields:
                field.widget.attrs['disabled'] = 'true'
                field.required = False

    def clean(self):
        cleaned_data = super(TarotForm, self).clean()
        for field in self.Meta.readonly_fields:
            cleaned_data[field] = getattr(self.instance, field)
        return cleaned_data

class TarotPartieForm(TarotForm):
    """ Création / mise à jour d'une partie """
    class Meta:
        model = TarotPartie
        fields = ['name']
        readonly_fields = ()
        widgets = {
            'name': forms.TextInput(attrs={
                'type': 'text',
                'maxlength': 15,
                "required": "required"
            }),
        }

class TarotJoueurForm(TarotForm):
    """ Création / mise à jour d'un joueur """
    class Meta:
        model = TarotJoueur
        fields = ['pseudo']
        widgets = {
            'pseudo': forms.TextInput(attrs={'type': 'text', 'maxlength': 15, "required": "required"}),
            # 'email': forms.TextInput(attrs={'type': 'email'}),
        }
        readonly_fields = ()

    # def clean_pseudo(self):
    #     pseudo = self.cleaned_data['pseudo']
    #     if not pseudo:
    #         raise forms.ValidationError("Le pseudo est obligatoire")
    #     return pseudo  # Ne pas oublier de renvoyer le contenu du champ traité

class TarotJeuPariForm(TarotForm):
    """ Saisie du pari dun joueur """

    class Meta:
        model = TarotJeu
        fields = ['pari']
        widgets = {
            'pari': forms.RadioSelect(attrs={'type': 'radio'})
        }
        readonly_fields = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        crudy = Crudy(self.request, "tarot")
        tarotJeu = kwargs["instance"]
        # nre de plis demandés
        plis = 0
        for jeu in TarotJeu.objects.all().filter(participant__partie_id=crudy.folder_id, jeu=tarotJeu.jeu):
            if jeu.donneur != 1:
                plis += jeu.pari
        choices = []
        for i in range(0, tarotJeu.carte + 1):
            if tarotJeu.carte - plis == i and tarotJeu.donneur == 1:
                continue
            choices.append((i, "%s pli" % (i,)))
        self.fields['pari'].choices = choices
        self.fields['pari'].label = ""

class TarotJeuRealForm(TarotForm):
    """ Saisie du réalisé dun joueur """

    class Meta:
        model = TarotJeu
        fields = ['real']
        widgets = {
            'real': forms.RadioSelect(attrs={'type': 'radio'})
        }
        readonly_fields = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        crudy = Crudy(self.request, "tarot")
        tarotJeu = kwargs["instance"]
        choices = [("PT", "Petite"),("PC", "Pouce"),("GA", "Garde"),("GS", "Garde Sans"),("GC", "Garde Contre")]
        for i in range(0, tarotJeu.carte + 1):
            choices.append((i, "%s pli" % (i,)))
        self.fields['real'].choices = choices
        self.fields['real'].label = ""

class TarotJeuBoutsForm(TarotForm):
    """ Saisie du nombre de bouts """

    class Meta:
        model = TarotJeu
        fields = ['bouts']
        widgets = {
            'bouts': forms.TextInput(attrs={'type': 'radio'}),
        }
        readonly_fields = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        crudy = Crudy(self.request, "tarot")
        choices = []
        for i in range(0, 3):
            choices.append((i, "%s bout" % (i,)))
        self.fields['bouts'].choices = choices
        self.fields['bouts'].label = ""

class TarotJeuPartenaireForm(TarotForm):
    """ Saisie du partenaire """

    class Meta:
        model = TarotJeu
        fields = ['partenaire']
        widgets = {
            'partenaire': forms.CheckboxInput(attrs={'type': 'check'}),
        }
        readonly_fields = ()

class TarotJeuPrimeForm(TarotForm):
    """ Saisie des primes """

    class Meta:
        model = TarotJeu
        fields = ['ptbout', 'misere1', 'misere2', 'poignee1', 'poignee2', 'poignee3', 'ptchelem', 'grchelem']
        widgets = {
            'ptbout': forms.CheckboxInput(attrs={'type': 'check'}),
            'misere1': forms.CheckboxInput(attrs={'type': 'check'}),
            'misere2': forms.CheckboxInput(attrs={'type': 'check'}),
            'poignee1': forms.CheckboxInput(attrs={'type': 'check'}),
            'poignee2': forms.CheckboxInput(attrs={'type': 'check'}),
            'poignee3': forms.CheckboxInput(attrs={'type': 'check'}),
            'ptchelem': forms.CheckboxInput(attrs={'type': 'check'}),
            'grchelem': forms.CheckboxInput(attrs={'type': 'check'}),
        }
        readonly_fields = ()

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for name, field in self.fields.items():
    #         field.required = False
