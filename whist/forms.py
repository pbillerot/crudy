from django import forms
from .models import WhistPartie, WhistJoueur, WhistParticipant, WhistJeu

# Personnalisation des champs
class MyForm(forms.Form):
  def as_foobar(self):
    return self._html_output(
      normal_row = u'%(label)s %(field)s%(help_text)s',
      error_row = u'%s',
      row_ender = '',
      help_text_html = u' %s',
      errors_on_separate_row = False)

class WhistForm(forms.ModelForm):

    class Meta:
        model = None
        fields = []
        readonly_fields = ()

    def __init__(self, *args, **kwargs):
        super(WhistForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in self.Meta.readonly_fields:
                field.widget.attrs['disabled'] = 'true'
                field.required = False

    def clean(self):
        cleaned_data = super(WhistForm, self).clean()
        for field in self.Meta.readonly_fields:
            cleaned_data[field] = getattr(self.instance, field)
        return cleaned_data

class WhistPartieFolderForm(WhistForm):
    """ Création / mise à jour d'une partie """
    class Meta:
        model = WhistPartie
        fields = ['name']
        readonly_fields = ()

class WhistPartieForm(WhistForm):
    """ Création / mise à jour d'une partie """
    class Meta:
        model = WhistPartie
        fields = ['name', 'cartes']
        readonly_fields = ()

    # CTR
    def clean_jeu(self):
        jeu = self.cleaned_data['jeu']
        if jeu < 3:
            raise forms.ValidationError("Le nombre de jeu de la partie doit être supérieur à 3")
        return jeu  # Ne pas oublier de renvoyer le contenu du champ traité

    def clean_name(self):
        name = self.cleaned_data['name']
        if not name:
            raise forms.ValidationError("Le nom est obligatoire")
        return name  # Ne pas oublier de renvoyer le contenu du champ traité

    def clean(self):
        cleaned_data = super(WhistPartieForm, self).clean()
        # if self.errors:
        #     raise forms.ValidationError("Corrigez les erreurs suivantes.")
        # name = cleaned_data.get('name')
        # err = self.errors
        return cleaned_data  # N'oublions pas de renvoyer les données si tout est OK

class WhistJoueurForm(WhistForm):
    """ Création / mise à jour d'un joueur """
    class Meta:
        model = WhistJoueur
        fields = ['pseudo', 'email']
        readonly_fields = ()

    def clean_pseudo(self):
        pseudo = self.cleaned_data['pseudo']
        if not pseudo:
            raise forms.ValidationError("Le pseudo est obligatoire")
        return pseudo  # Ne pas oublier de renvoyer le contenu du champ traité

class WhistParticipantForm(WhistForm):
    """ Création / mise à jour d'un participant d'une partie """
    class Meta:
        model = WhistParticipant
        fields = ['partie', 'joueur', 'score']
        readonly_fields = ('score',)

class WhistJeuForm(WhistForm):
    """ Création / mise à jour d'un jeu d'une partie """
    class Meta:
        model = WhistJeu
        # fields = ['partie', 'joueur', 'jeu', 'pari', 'real', 'score']
        fields = ['participant', 'jeu', 'pari', 'real', 'score']
        readonly_fields = ('score',)

    # CTRL pour les views et Admin
    def clean_pari(self):
        pari = self.cleaned_data['pari']
        if pari > self.cleaned_data['jeu']:
            raise forms.ValidationError("Le pari ne peut pas dépasser le nombre de carte du jeu")
        if pari < 0:
            raise forms.ValidationError("Le pari ne peut pas être négatif")

        return pari  # Ne pas oublier de renvoyer le contenu du champ traité

    def clean_real(self):
        real = self.cleaned_data['real']
        if real > self.cleaned_data['jeu']:
            raise forms.ValidationError("Le réalisé ne peut pas dépasser le nombre de carte du jeu")
        if real < 0:
            raise forms.ValidationError("Le réalisé ne peut pas être négatif")

        return real  # Ne pas oublier de renvoyer le contenu du champ traité

    # def clean(self):
    #     cleaned_data = super(WhistJeuForm, self).clean()
    #     pari = cleaned_data.get('pari')
    #     real = cleaned_data.get('real')
    #     if pari != real:
    #         cleaned_data.set_value('points', -10)
    #     else:
    #         cleaned_data.set_value('points', 10 + pari * 2)

    #     return cleaned_data  # N'oublions pas de renvoyer les données si tout est OK
