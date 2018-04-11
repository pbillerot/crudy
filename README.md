## CRUDY

Framework de développement d'applications Web 
    particulièrement pour mobile - Django 2.x

Sources disponible sur [Github](https://github.com/pbillerot/crudy)

#### CSS
- CSS: <https://getmdl.io/index.html>
- ICON: <https://material.io/icons/>

#### DJANGO 
- Ref: <https://docs.djangoproject.com/fr/2.0/topics/>
- Fields: <https://docs.djangoproject.com/fr/2.0/ref/models/fields/>
- Templates : <https://docs.djangoproject.com/fr/2.0/ref/templates/builtins/>
- django-markup: <http://django-markup.readthedocs.io/en/latest/index.html> 

### Version 1.2 du 11 avril 2018
- L'application Whist intégrée dans le framework CRUDY
- Protection de toutes les URLs

### Version 1.13 du 5 avril 2018
> Avertissement: avec Apache2 limiter le nombre de process wsgi à 1 \
> sinon le contexte crudy ne peut pas être partagé entre chaque request
```
# Exemple de config de WSGI 
WSGIDaemonProcess crudy processes=1 threads=8 display-name=%{GROUP} python-home=***/crudy/venv python-path=:***/crudy
WSGIProcessGroup crudy
WSGIScriptAlias / ***/crudy/crudy/wsgi.py
<Directory "***/crudy/crudy">
  <Files "wsgi.py">
    Require all granted
  </Files>
</Directory>

Alias /static/ ***/crudy/static/
Alias /media/ ***/crudy/static/
<directory ***/crudy/static>
   Require all granted
</directory>
```

### Version 1.12 du 4 avril 2018
- Sécurisation des vues / folder

### Version 1.1 du 28 mars 2018
- Comptage des points du Tarot à 3, 4, 5, et 6 joueurs

### Version 1.0.1 du 19.3.28
- Seuls les utilisateurs connectés peuvent utiliser l'outil.

### Version 1.0 du 18.2.28
- Version opérationnelle sur Raspberry PI en HTTPS Apache2.4 Sqlite3 Django 2.0.2 Python 3.5

#### Version 18.2.28 alpha
- Material Design Lite
- Suppression des warnings
- Fichier local_settings.py pour gérer une config par site
- Gestion des logs de python

#### Version 18.2.13 beta
- Version opérationnelle sur Raspberry PI - Apache2 - Sqlite3

#### Version 18.2.8 beta
- Application WHIST opérationelle pour déploiement sur production