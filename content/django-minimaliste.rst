Créer une application django minimaliste
########################################

:date: 2016-04-04
:tags: python,django,mini
:category: Django
:slug: django-minimaliste
:authors: Morgan
:summary: Créer une application django minimaliste

.. image:: ./images/djangopony.png
    :alt: Django
    :align: right

`Django <https://www.djangoproject.com/>`_ est un framework très complet,
qui nécessite un certain investissement pour entrer dans le bain.

Il est donc le plus souvent utilisé pour créer des applications conséquentes,
ce qui amène les développeurs à préférer des frameworks légers comme
`Bottle <http://bottlepy.org/>`_ ou `Flask <http://flask.pocoo.org/>`_ pour le
développement de petites applications.

Pourtant, il est possible d'utiliser Django de manière minimaliste, afin
d'obtenir un résultat proche des frameworks légers.

L'astuce décrite ci-dessous est à garder quelque part dans un coin de ta tête,
car ça pourra sûrement t'être utile un jour.

Après avoir installé django (1.9.5 à l'heure où j'écris ces lignes):

.. code-block:: bash

    pip install django

Tu crées le fichier **myserver.py** suivant dans le répertoire de ton pojet:

.. code-block:: python

    # -*- coding: utf-8 -*-

    """
        Django minimaliste
    """

    from django.conf import settings
    from django.conf.urls import url
    from django.shortcuts import render
    import sys

    # On définit les settings obligatoires et utiles
    settings.configure(
        DEBUG=True,
        SECRET_KEY='S3CR3T',
        ROOT_URLCONF=__name__,
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': ['./templates/'],
        }],
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ),
    )

    # On crée nos vues
    def index(request, someone="World"):
        return render(request, 'index.html', {"someone": someone})

    # On délare nos urls
    urlpatterns = (
        url(r'^$', index),
        url(r'^(?P<someone>\w+)/$', index),
    )

    # On exécute le serveur comme s'il s'agissait d'un fichier manage.py
    # via python myserver.py runserver
    if __name__ == "__main__":
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)

Tu as donc écrit:

* Les paramètres de configuration de base, incluant le nom du répertoire qui
  contiendra les templates.
* Une vue **index** qui appelle le template **index.html**.
* Les patterns de tes urls.
* Le **main** qui va te permettre d'exécuter l'ensemble des commandes django.

Evidemment, tu peux faire évoluer ce fichier selon tes besoins, comme pour
rajouter une base de données par exemple.

Maintenant, tu vas créer le template **index.html** suivant dans un sous-répertoire
appelé **templates**:

.. code-block:: html

    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8">
            <title>Hello World!</title>
        </head>
        <body>
            <p>Hello {{ someone }} !</p>
        </body>
    </html>

Il ne te reste plus qu'à lancer le serveur via la commande:

.. code-block:: bash

    python myserver.py runserver

Enfin, rends-toi sur http://127.0.0.1:8000/ et http://127.0.0.1:8000/arthur/
pour voir le résultat !
