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
        choices = [(".", "Je passe"),("PT", "Petite (10 points)"),("PC", "Pouce (20 points)")\
        ,("GA", "Garde (40 points)"),("GS", "Garde Sans (60 points)"),("GC", "Garde Contre (80 points)")]
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
        choices = [(-30,"chute de 30"),(-20,"chute de 20"),(-10,"chute de 10"),(-1,"chute de 0")\
        ,(+1,"fait de 0"),(+10,"fait de 10"),(+20,"fait de 20"),(+30,"fait de 30")\
        ,(+40,"fait de 40"),(+50,"fait de 50"),(+60,"fait de 60")]
        self.fields['real'].choices = choices
        self.fields['real'].label = ""

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
        fields = ['ptbout', 'misere1', 'misere2', 'poignee1', 'poignee2', 'poignee3', 'ptchelem', 'pchelem', 'ppchelem', 'grchelem', 'gchelem', 'gpchelem']
        widgets = {
            'ptbout': forms.CheckboxInput(attrs={'type': 'check'}),
            'misere1': forms.CheckboxInput(attrs={'type': 'check'}),
            'misere2': forms.CheckboxInput(attrs={'type': 'check'}),
            'poignee1': forms.CheckboxInput(attrs={'type': 'check'}),
            'poignee2': forms.CheckboxInput(attrs={'type': 'check'}),
            'poignee3': forms.CheckboxInput(attrs={'type': 'check'}),
            'ptchelem': forms.CheckboxInput(attrs={'type': 'check'}),
            'pchelem': forms.CheckboxInput(attrs={'type': 'check'}),
            'ppchelem': forms.CheckboxInput(attrs={'type': 'check'}),
            'grchelem': forms.CheckboxInput(attrs={'type': 'check'}),
            'gchelem': forms.CheckboxInput(attrs={'type': 'check'}),
            'gpchelem': forms.CheckboxInput(attrs={'type': 'check'}),
        }
        readonly_fields = ()

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for name, field in self.fields.items():
    #         field.required = False
