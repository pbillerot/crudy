# coding: utf-8
import os
from django.shortcuts import render
from crudy.crudy import Crudy
"""
    Vues du portail
"""

# Create your views here.
def p_portail_home(request):
    """ Portail d'accueil de CRUDY """
    crudy = Crudy(request, "portail")
    return render(request, 'p_portail_home.html', locals())

def p_portail_help(request):
    """ Aide de CRUDY """
    crudy = Crudy(request, "portail")
    readme = ""
    with open(os.path.dirname(__file__) + "/../README.md", mode="r", encoding='utf-8') as fichier:
	    readme = fichier.read()
    return render(request, 'p_portail_help.html', locals())
