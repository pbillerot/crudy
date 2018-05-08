# coding: utf-8
from django.contrib import admin
from .models import WhistJoueur, WhistPartie, WhistParticipant, WhistJeu
from django.utils.safestring import mark_safe
from . import forms

class WhistJoueurAdmin(admin.ModelAdmin):
    list_display = ('owner','pseudo', 'email')
    list_filter = ('owner',)
    # search_fields = ('pseudo', 'email')
    pass

class WhistPartieAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'date', 'cartes', 'jeu', 'modified')
    list_filter = ('owner',)
    # fields = ('name', 'cartes')
    # search_fields = ('name',)
    # list_editable = ['jeu']
    pass

class WhistParticipantAdmin(admin.ModelAdmin):
    list_display = ('partie', 'joueur', 'score', 'order', 'donneur')
    # search_fields = ('partie', 'joueur')
    # ordering = ('partie', '-score')
    list_filter = ('partie',)
    # readonly_fields = ('score',)
    pass

admin.site.register(WhistJoueur, WhistJoueurAdmin)
admin.site.register(WhistPartie, WhistPartieAdmin)
# admin.site.register(WhistJeu, WhistJeuAdmin)
admin.site.register(WhistParticipant, WhistParticipantAdmin)
