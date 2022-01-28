Mon environnement python en 2022
################################

:date: 2022-01-28
:tags: python,librairies,poetry,black,isort,pyenv,mypy
:category: Python
:slug: environnement-python-2022
:authors: Morgan
:summary: Mon environnement python en 2022

.. image:: ./images/python.png
    :alt: Python
    :align: right

Pour cette nouvelle année 2022, on va voir ensemble les quelques librairies plutôt cools pour
se faire un environnement de dev sympa et efficace en python ! On teste avec **python 3.9** car il y a encore des soucis de compatibilité
pour certaines librairies avec python 3.10.

Versions de python
==================

Pour gérer les différentes versions de python sur ta machine, il est plutôt pratique d'utiliser `pyenv <https://github.com/pyenv/pyenv>`_.
Pour les devs JS, c'est un équivalent à `nvm <https://github.com/nvm-sh/nvm>`_ et à `n <https://github.com/tj/n>`_ mais pour python.

Pour l'installer et l'utiliser rien de plus simple :

.. code-block:: bash

    sudo apt-get install aria2 build-essential curl git libbz2-dev libffi-dev liblzma-dev \
    libncurses5-dev libncursesw5-dev libreadline-dev libsqlite3-dev libssl-dev llvm make tk-dev wget xz-utils zlib1g-dev
    curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"

    pyenv install 3.9.10

Après, si tu n'as pas besoin de gérer plein de versions différentes régulièrement, tu peux te cantonner à utiliser les packages de ta distro.


Environnement virtuel et packaging
==================================

Pour ma part, fini les `virtualenv <https://github.com/pypa/virtualenv>`_, `virtualenvwrapper <https://virtualenvwrapper.readthedocs.io/en/latest/>`_
et `setup.py <https://docs.python.org/fr/3/distutils/setupscript.html>`_, et place
à `poetry <https://python-poetry.org/>`_ et au fichier `pyproject.toml <https://python-poetry.org/docs/pyproject/>`_ !

La communauté python peine depuis un moment à avoir de bons outils pour gérer le packaging des applications et **poetry** vient apporter une solution à
tout ça. Certains diront que sa non-compatibilité avec les fichiers **setup.py** est le mal absolu car non-standard, ce qui n'est pas complètement faux ...
Mais cet outil est tellement pratique que j'en ai fait fi.

On l'installe et on initie un nouveau projet avec un **venv** encapsulé automatiquement :

.. code-block:: bash

    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

    poetry new --src myapp
    cd myapp
    poetry add black isort
    echo 'print("Hello World!")' > src/main.py
    poetry run python src/main.py
    poetry build
    poetry publish

Ici on a ajouté les librairies black et isort dans les dépendances du projet et on a exécuté notre script python "Hello World!".
Ensuite, on a buildé un **sdist** et un **wheel** qu'on a déployé sur PyPI.

Et voici aperçu du fameux fichier **pyproject.toml** généré :

.. code-block:: bash

    [tool.poetry]
    name = "myapp"
    version = "0.1.0"
    description = ""
    authors = ["mobo"]

    [tool.poetry.dependencies]
    python = "^3.9"
    black = "^21.12b0"
    isort = "^5.10.1"

    [tool.poetry.dev-dependencies]
    pytest = "^5.2"

    [build-system]
    requires = ["poetry-core>=1.0.0"]
    build-backend = "poetry.core.masonry.api"

Quel gain de temps énorme !

Formattage du code
==================

`Black <https://github.com/psf/black>`_ domine désormais de très loin tous les linters et autres formatteurs de code python. Plus besoin de
cumuler et de configurer une tonne d'outils comme pep8, flake8, pylint, pyflakes, pychecker.
On dégage tout ça et on utilise que **black**. Il va se charger de formatter correctement ton code, point barre. C'est l'équivalent du gofmt de golang.

Est-ce que le rendu est parfait ? Non. Est-ce qu'il est suffisamment bon pour qu'on arrête de se poser la question de comment formater notre code ?
Oui, mille fois oui.

On l'installe et on l'exécute sur notre projet et c'est tout. Pour automatiser tout ça, tu peux même le mettre sur un git hook, au commit par exemple.

.. code-block:: bash

    poetry add black
    poetry run black src/

Si tu es quelqu'un de tatillon qui aime avoir ses importations bien ordonnées, tu peux utiliser `isort <https://github.com/PyCQA/isort>`_.
Comme pour black, tu l'installes et tu le lances sur ton projet et c'est réglé :

.. code-block:: bash

    poetry add isort
    poetry run isort src/

Typage statique
================

Suite au succès de `typescript <https://www.typescriptlang.org/>`_ pour le typage statique de javascript, une sorte d'équivalent a vu le
jour pour python sous la forme d'une librairie optionnelle appelée `mypy <https://github.com/python/mypy>`_.
Cette librarie permet d'annoter notre code pour expliciter les types de nos arguments, fonctions, classes, etc ...

Tu peux écrire ce script par exemple :

.. code-block:: python

    def hello(name: str, age: int) -> str:
            return f"Hello {name}, you are {age} years old."

    print(hello("Jean", 18))


Et tu verifies le typage à l'aide de la commande suivante :

.. code-block:: bash

    poetry add mypy
    poetry run mypy src/

Tests unitaires
===============

Rien de neuf sous le soleil, on utilise toujours `pytest <https://docs.pytest.org/en/6.2.x/>`_ qui est installé par defaut avec poetry :

.. code-block:: bash

    poetry run pytest

Il est même possible d'utiliser `tox avec poetry <https://python-poetry.org/docs/faq/#is-tox-supported>`_ pour exécuter les tests sous
plusieurs environnements avec un **tox.ini** ressemblant à ça :

.. code-block:: bash

    [tox]
    isolated_build = true
    envlist = py27, py36

    [testenv]
    whitelist_externals = poetry
    commands =
        poetry install -v
        poetry run pytest tests/

Développement web
=================

Rien de révolutionnaire ici non plus. Dans 80% des cas, pour les applications moyennes et complexes, `django-rest-framework <https://www.django-rest-framework.org/>`_
couplé au framework front-end de ton choix fera le café.

Pour les 20% de cas d'applications très simples, je reste sur le framework `bottle <https://bottlepy.org/>`_ et l'orm `peewee <https://github.com/coleifer/peewee>`_,
qui ne m'ont jamais fait défaut.

Je trouve que le combo `flask <https://flask.palletsprojects.com/>`_ + `sqlalchemy <https://www.sqlalchemy.org/>`_ est une espèce
d'entre-deux qui ne correspond à aucun de mes cas d'usage.

Bon dev à tous !