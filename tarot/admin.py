# coding: utf-8
from django.contrib import admin
from .models import TarotJoueur, TarotPartie, TarotParticipant, TarotJeu
from django.utils.safestring import mark_safe
from . import forms

class TarotJoueurAdmin(admin.ModelAdmin):
    list_display = ('owner', 'pseudo', 'email')
    list_filter = ('owner',)
    # search_fields = ('pseudo', 'email')
    pass

class TarotPartieAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'jeu', 'modified')
    list_filter = ('owner',)
    # fields = ('name',)
    # search_fields = ('name',)
    # list_editable = ['jeu']
    pass

class TarotParticipantAdmin(admin.ModelAdmin):
    list_display = ('partie', 'joueur', 'score', 'order', 'donneur')
    # search_fields = ('partie', 'joueur')
    # ordering = ('partie', '-score')
    list_filter = ('partie',)
    # readonly_fields = ('score',)
    pass

admin.site.register(TarotJoueur, TarotJoueurAdmin)
admin.site.register(TarotPartie, TarotPartieAdmin)
# admin.site.register(TarotJeu, TarotJeuAdmin)
admin.site.register(TarotParticipant, TarotParticipantAdmin)
