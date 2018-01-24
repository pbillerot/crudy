from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import WhistJoueur, WhistPartie, WhistParticipant, WhistJeu
from django.utils.safestring import mark_safe
from . import forms

class WhistJoueurAdmin(admin.ModelAdmin):
    list_display = ('pseudo', 'email')
    search_fields = ('pseudo', 'email')

class WhistPartieAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'jeu')
    search_fields = ('name',)
    list_editable = ['jeu']

class WhistJeuAdmin(admin.ModelAdmin):
    # liste
    list_display = ('partie', 'joueur', 'jeu', 'pari', 'real', 'Points', 'score')
    search_fields = ['partie__name', 'joueur__pseudo',]
    ordering = ('partie', 'jeu', '-score', 'joueur')
    list_filter = ('partie', 'jeu')
    list_editable = ['pari', 'real']
    # formulaire
    fields = ['partie', 'joueur', 'jeu', 'pari', 'real', 'score']
    readonly_fields = ('score',)
    form = forms.WhistJeuForm

    def Points(self, obj):
        color = 'black'
        if obj.points > 10:
            color = 'green'
        if obj.points < 0:
            color = 'red'
        return mark_safe('<b style="text-align: right; color:{};">{}</b>'.format(color, obj.points))
        # return u'<b style="background:{};">{}</b>'.format(color, obj.points)

class WhistParticipantAdmin(admin.ModelAdmin):
    list_display = ('partie', 'joueur', 'score')
    search_fields = ('partie', 'joueur')
    ordering = ('partie', '-score')
    list_filter = ('partie',)

admin.site.register(WhistJoueur, WhistJoueurAdmin)
admin.site.register(WhistPartie, WhistPartieAdmin)
admin.site.register(WhistJeu, WhistJeuAdmin)
admin.site.register(WhistParticipant, WhistParticipantAdmin)
