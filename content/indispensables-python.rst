Mes librairies python indispensables
####################################

:date: 2016-07-09
:tags: python,django,librairies
:category: Python
:slug: indispensables-python
:authors: Morgan
:summary: Mes librairies python indispensables

.. image:: ./images/python.png
    :alt: Python
    :align: right

C'est pas forcément évident de trouver le temps de faire un tuto intéressant
et complet pour chaque outil rencontré dans sa vie de dev.

Du coup, j'en profite pour te un faire un petit listing de mes librairies
indispensables en python. On ne sait jamais, peut-être que tu y découvriras
quelque-chose d'utile !

Framework web
=============

* django_: framework le plus réputé, qui a l'avantage d'avoir une tonne de
  support et de documentation. Indispensable pour créer des applications web complexes.
* bottle_: framework ultra minimaliste, idéal pour les applications web de petites et de
  moyennes tailles.
* pelican_: générateur de site statique utilisé par ce blog ! Tuto dispo `ici <http://dotmobo.github.io/pelican.html>`__.

Base de données
===============

* sqlalchemy_: orm python le plus avancé, tout simplement.
* peewee_: orm léger et simple, parfait pour des besoins pas trop complexes.
* psycopg2_: driver postgresql
* cx-oracle_: driver oracle
* tinydb_: base de données ultra minimaliste. Tuto dispo `ici <http://dotmobo.github.io/tinydb.html>`__.

Http
====

* httpie_: client http en ligne de commande. Tuto dispo `ici <http://dotmobo.github.io/httpie.html>`__.
* requests_: librairie http la plus simple et le plus efficace.
* britney_ et britney-utils_: client SPORE_, qui est une spécification de description
  d'APIs REST.
* suds-jurko_: client SOAP léger et simple d'usage.

Templating
==========

* jinja2_: moteur de template le plus réputé, utilisé par django.
* mako_: moteur de template ultra performant. Tuto dispo `ici <http://dotmobo.github.io/mako.html>`__.
* cookiecutter_: moteur de template de projet utilisant jinja2. Vous pouvez jeter un oeil à `l'article
  de Sam <http://sametmax.com/templates-de-projet-avec-cookiecutter/>`_ sur le sujet.
  Exemples d'utilisation: simple-python-drybones_ et bottle-drybones_.

Machine learning
================

* scikit-learn_: projet de machine learning qui provient du Google Summer Of Code 2007.
  Google est en train d'en faire `une série du tutos sur youtube <https://www.youtube.com/watch?v=cKxRvEZd3Mw&list=PLOU2XLYxmsIIuiBfYad6rFYQU_jL2ryal&index=6>`_
  vraiment intéressante.

Déploiement
===========

* fabric_: outil qui permet déployer des applications via ssh.
* fabtools_: ensemble de fonctionnalités pour fabric.
* pydiploy_: projet qui utilise fabric et fabtools pour automatiser le déploiement
  d'applications. Pour les applications django par exemple, il permet de déployer et de configurer
  toute la stack python/virtualenv/circus/chaussette/nginx.

Django
======

* django-extensions_: extension des commandes de django.
* django-static-precompiler_: librairie qui permet d'automatiser la précompilation des fichiers
  CoffeeScript, Livescript, Sass, Less et autres.
* django-crispy_: outil formidable pour créer des formulaires compatibles bootstrap. Tuto dispo `ici <http://dotmobo.github.io/django-crispy-forms.html>`__.
* django-workflows_ et django-workflow-activity_: outils pour créer des worflows états/transitions.
* django-drybones_: template de projet django.
* django-autocomplete-light_: module d'autocomplétion pour les champs des formulaires.
* django-countries_: gestion des pays dans django. Tuto dispo `ici <http://dotmobo.github.io/django-countries.html>`__.
* django-simple-captcha_: utilisation de captchas. Tuto dispo `ici <http://dotmobo.github.io/django-simple-captcha.html>`__.
* django-rest-framework_ (drf): excellente librairie pour créer des APIs REST.
* django-fine-permissions_: gestion des permissions fines, par champs et par utilisateur,
  pour drf.
* django-filter_: gestion des filtres des querysets qui fonctionne très bien avec drf.
* django-hypnos_: outil qui permet de générer automatiquement une api rest avec drf,
  à partir d'une base de données sqlite/postgresql/mysql/oracle existante.
* django-cas-sso_: client pour l'authentification CAS, qui supporte le Single-Sign-Out.
* django-ldapdb_: backend pour manipuler les entrées des annuaires LDAP.
* django-oauth-toolkit_: ensemble d'outils pour oauth2.

Test
====

* tox_: outil qui permet d'exécuter les tests unitaires sous plusieurs virtualenvs
  avec des configurations différentes. Tuto dispo `ici <http://dotmobo.github.io/integration-continue.html>`_.
* coverage_: outil d'analyse de la couverture du code.
* prospector_: outil utilisé par `landsacape.io <https://landscape.io/>`_
  qui utilise les meilleurs linters python pour vérifier la qualité du code.

Doc
===

* sphinx_: outil de génération de documentation à partir de fichiers reStructuredText.

Wamp
====

* crossbar: router wamp le plus avancée pour python. Il y a de nombreux articles chez Sam;
* autobahn: implémentation du protocle wamp qui fonctionne très bien avec crossbar

Wsgi
====

* circus + chaussette + waitress: stack wsgi dont je parle ici

Date
====

* python-dateutil: extension au module datetime de python
* pytz: gestion des timezones

Script
======

* docopt: parser les arguments de script de manière élégante
* ipython: shell python le plus avancé
* apscheduler: planifier des tâches à la manière des crons

Crypto
======

* pycrypto: pratique pour générer des hashs en sha2546 par ex

Parsing
=======

* lxml: lire/écrire du xml
* jsonschema: c'est comme les schémas xml, mais pour json
* pyyaml: libraire pour lire/écrire du yaml
* reportlab: outil de production de pdf

En vrac
=======

* six: pour la compatibilité python 2/3
* pytoolz: extension d'itertools et functools, j'en parle ici
* unidecode: permet de remplacer des caractères unicode en ascii

Bonne découverte !

.. _django: https://www.djangoproject.com/
.. _bottle: http://bottlepy.org/docs/dev/index.html
.. _pelican: http://blog.getpelican.com/
.. _sqlalchemy: http://www.sqlalchemy.org/
.. _peewee: http://docs.peewee-orm.com/
.. _psycopg2: http://initd.org/psycopg/
.. _cx-oracle: http://cx-oracle.sourceforge.net/
.. _tinydb: https://pypi.python.org/pypi/tinydb
.. _httpie: http://httpie.org
.. _requests: http://docs.python-requests.org/en/master/
.. _britney: https://github.com/agrausem/britney
.. _britney-utils: https://github.com/unistra/britney-utils
.. _SPORE: http://spore.github.io/
.. _suds-jurko: https://bitbucket.org/jurko/suds
.. _jinja2: http://jinja.pocoo.org/
.. _mako: http://www.makotemplates.org/
.. _cookiecutter: https://github.com/audreyr/cookiecutter
.. _simple-python-drybones: https://github.com/unistra/simple-python-drybones
.. _bottle-drybones: https://github.com/unistra/bottle-drybones
.. _scikit-learn: http://scikit-learn.org/
.. _fabric: http://www.fabfile.org/
.. _fabtools: https://github.com/ronnix/fabtools
.. _pydiploy: https://github.com/unistra/pydiploy
.. _django-extensions: https://github.com/django-extensions/django-extensions
.. _django-static-precompiler: https://github.com/andreyfedoseev/django-static-precompiler
.. _django-crispy: http://django-crispy-forms.readthedocs.io/
.. _django-workflows: https://github.com/diefenbach/django-workflows
.. _django-workflow-activity: https://github.com/unistra/django-workflow-activity
.. _django-drybones: https://github.com/unistra/django-drybones
.. _django-autocomplete-light: https://github.com/yourlabs/django-autocomplete-light
.. _django-countries: https://github.com/SmileyChris/django-countries
.. _django-simple-captcha: https://github.com/mbi/django-simple-captcha
.. _django-rest-framework: http://www.django-rest-framework.org/
.. _django-fine-permissions: https://github.com/unistra/django-rest-framework-fine-permissions
.. _django-filter: https://github.com/carltongibson/django-filter
.. _django-hypnos: https://github.com/unistra/django-hypnos
.. _django-cas-sso: https://pypi.python.org/pypi/django-cas-sso/
.. _django-ldapdb: https://github.com/unistra/django-ldapdb
.. _django-oauth-toolkit: https://github.com/evonove/django-oauth-toolkit
.. _tox: http://tox.readthedocs.io/
.. _coverage: https://coverage.readthedocs.io
.. _prospector: http://prospector.landscape.io/en/master/
.. _sphinx: http://www.sphinx-doc.org/
