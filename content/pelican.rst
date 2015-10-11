Générer son site statique grâce à Pelican
#########################################

:date: 2015-10-11
:tags: pelican,python,jekyll,blog,github
:category: Python
:slug: pelican
:authors: Morgan
:summary: Générer son site statique grâce à Pelican

`Pelican <http://blog.getpelican.com/>`_ est un outil vraiment chouette pour
générer rapidement un site statique comme un blog, afin de le publier via
`Github Pages <https://pages.github.com>`_ par exemple.

C'est une alternative Python à `Jekyll <https://jekyllrb.com/>`_ (qui lui est
écrit en Ruby), permettant de rédiger ses articles en Markdown. La
principale force de Pelican, c'est de proposer également le `reStructuredText
<http://sphinx-doc.org/rest.html>`_ comme format d'écriture, ce qui rendra
heureux tous les amoureux de Sphinx.

Pour l'installer, rien de plus simple, l'outil est dispo sur `Pypi
<https://pypi.python.org/pypi>`_:

.. code-block:: bash

    pip install pelican

Il propose une commande de génération automatique de projet :

.. code-block:: bash

    mkdir ~/dev/myblog && cd ~/dev/myblog && pelican-quickstart

N'oublie pas de dire oui aux deux questions concernant Github Pages,
et ... c'est tout! Pour proposer des articles, il te suffit de les créer en .rst
dans le dossier *content*:

.. code-block:: bash

    vi ~/dev/myblog/content/mon-article.rst

Ils devront ressembler à ça:

.. code-block:: rst

    Mon article
    ###########

    :date: 2015-10-11 10:20
    :modified: 2015-11-04 18:40
    :tags: python,django
    :category: Développement
    :slug: mon-article
    :authors: Toi
    :summary: Mon article concerne blablabla

    blablabla ...

Jetons maintenant un coup d'oeil aux deux fichiers de configuration.

Le premier, *pelicanconf.py* , est utilisé pour la configuration générale du site:

.. code-block:: python

    #!/usr/bin/env python
    # -*- coding: utf-8 -*- #
    from __future__ import unicode_literals

    AUTHOR = 'myusername'
    SITENAME = "myblog"
    SITEURL = ''

    PATH = 'content'

    TIMEZONE = 'Europe/Paris'

    DEFAULT_LANG = 'fr'

    # Feed generation is usually not desired when developing
    FEED_ALL_ATOM = None
    CATEGORY_FEED_ATOM = None
    TRANSLATION_FEED_ATOM = None
    AUTHOR_FEED_ATOM = None
    AUTHOR_FEED_RSS = None

    # Blogroll
    LINKS = None

    # Social widget
    SOCIAL = None

    DEFAULT_PAGINATION = 10

    # Uncomment following line if you want document-relative URLs when developing
    RELATIVE_URLS = True

    # Theme
    # THEME = "simple"

Tu remarqueras une partie *Theme*, on y reviendra plus tard.
Le reste est relativement compréhensible pour se passer d'explication.

Le second, *publishconf.py* , rajoute les spécificités pour la production:

.. code-block:: python

    #!/usr/bin/env python
    # -*- coding: utf-8 -*- #
    from __future__ import unicode_literals

    # This file is only used if you use `make publish` or
    # explicitly specify it as your config file.

    import os
    import sys
    sys.path.append(os.curdir)
    from pelicanconf import *

    SITEURL = 'http://myusername.github.io'
    RELATIVE_URLS = False

    FEED_ATOM = 'feeds/all.atom.xml'

    DELETE_OUTPUT_DIRECTORY = True

    # Following items are often useful when publishing

    #DISQUS_SITENAME = ""
    #GOOGLE_ANALYTICS = ""

Il est important ici de définir **SITEURL** et **FEED_ATOM**.
En effet, en mode dev, on n'a pas besoin de générer les flux atom et on utilise
des urls relatives.

Si besoin, tu noteras une compatibilité avec Google Analytics.
Et concernant Disqus, on y reviendra également plus tard.

Pelican propose alors tout un tas de commandes pour générer et déployer ton site.
Au choix, on va pouvoir utiliser `Fabric <http://www.fabfile.org>`_
(malheureusement non disponible en Python 3) ou **make**.

Pour générer ton site en mode dev (utilise *pelicanconf.py*):

.. code-block:: bash

    make html

Tu peux aussi utiliser un watcher pour automatiser la génération de ton site à chaque modification:

.. code-block:: bash

    make regenerate

Pour servir ton site en mode dev sur `http://localhost:8000/ <http://localhost:8000/>`_:

.. code-block:: bash

    make serve

Pour générer ton site pour la production (utilise *publishconf.py*):

.. code-block:: bash

    make publish

Enfin, pour le diffuser sur le master de ton dépôt Github Pages:

.. code-block:: bash

   make github

Concernant le dépôt Github, je te recommande de commiter le code Pelican sur une
branche à part, et de garder la branche *master* pour la diffusion du site.
Ton dépôt devra s'appeler *<username>.github.io* pour être compatbile avec
Github Pages.

Par défaut, le design peut sembler austère.

C'est pourquoi on va installer un `thème <http://pelicanthemes.com/>`_ un peu
plus moderne utilisant `Bootstrap <http://getbootstrap.com/>`_, comme
`alchemy <https://github.com/nairobilug/pelican-alchemy>`_ par exemple.

La plupart des thèmes disponibles sont sous licence MIT, donc n'hésite pas à les
forker pour y apporter tes customisations.

Pour les habitués de `django <https://www.djangoproject.com/>`_ et
`flask <http://flask.pocoo.org/>`_, Pelican utilise `jinja2 <http://jinja.pocoo.org/>`_
comme moteur de template. Et ça c'est carrément cool.

On installe donc alchemy:

.. code-block:: bash

    git clone git@github.com:nairobilug/pelican-alchemy.git ~/dev/pelican-alchemy
    pelican-themes -i ~/dev/pelican-alchemy/alchemy

Et on définit la variable **THEME** de notre fichier de conf *pelicanconf.py*:

.. code-block:: python

    THEME = "alchemy"
    SITE_SUBTEXT = "Blabla"
    PROFILE_IMAGE = "profil.jpeg"
    GITHUB_ADDRESS = "https://github.com/myusername"
    TWITTER_ADDRESS = "https://twitter.com/myusername"
    EXTRA_FAVICON = False
    LICENSE_NAME = "MIT"
    LICENSE_URL = "https://opensource.org/licenses/MIT"
    MENU_ITEMS = {}
    META_DESCRIPTION = "Blabla
    PAGES_ON_MENU = True
    CATEGORIES_ON_MENU = True
    TAGS_ON_MENU = True
    ARCHIVES_ON_MENU = True
    SHOW_ARTICLE_AUTHOR = False

Concernant les paramètres optionnels, je t'invite à regarder la doc d'alchemy.

"Ok, avoir un blog statique, c'est bien sympa, mais comment je fais pour avoir
des commentaires? Il me faut bien une partie dynamique non ?". Pas de panique,
`Disqus <https://disqus.com>`_ est là pour ça.

Il te suffit de te créer un compte sur Disqus et d'y enregistrer ton site en
utilisant le paramétrage **universal-embed-code**. À partir de la, tu vas pouvoir
le configurer via *http://<username>.disqus.com/admin/settings*.

Enfin, tu l'actives via ton fichier de conf de prod *publishconf.py*:

.. code-block:: python

    DISQUS_SITENAME = "myusername"

Tu commites tout ça, tu publies et hop! Ton blog est complètement prêt!
