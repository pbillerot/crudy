# coding: utf-8
import os
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from crudy.crudy import Crudy
"""
    Vues du portail
"""

# Create your views here.
def p_portail_home(request):
    """ Portail d'accueil de CRUDY """
    crudy = Crudy(request, "portail")
    title = crudy.application["title"]
    return render(request, 'p_portail_home.html', locals())

def p_portail_help(request):
    """ Aide de CRUDY """
    crudy = Crudy(request, "portail")
    readme = ""
    with open(os.path.dirname(__file__) + "/../README.md", mode="r", encoding='utf-8') as fichier:
	    readme = fichier.read()
    return render(request, 'p_portail_help.html', locals())

def f_portail_login(request):
    """ Login """
    crudy = Crudy(request, "portail")
    title = ""

    if request.user.is_authenticated:
        print(request.user.email, 'is connected')
    else:
        print('not connected')

    form = AuthenticationForm(data=request.POST)
    if request.POST and form.is_valid():
        login(request, form.get_user())
        if request.user.is_authenticated:
            print(request.user.email, 'connected')
            return redirect('p_portail_home')

    return render(request, 'f_portail_login.html', locals())

def f_portail_logout(request):
    """ Logout """
    if request.user.is_authenticated:
        print(request.user.email, 'disconnecting')
    logout(request)
    return render(request, 'p_portail_home.html', locals())
