Mon environnement python en 2025
################################

:date: 2025-08-25
:tags: python,librairies,uv,ty,pytest,ruff,fastapi
:category: Python
:slug: environnement-python-2025
:authors: Morgan
:summary: Mon environnement python en 2025

.. image:: ./images/python.png
    :alt: Python
    :align: right


Après trois ans sans toucher à Python, il est temps de faire une mise à jour sur les outils pratiques pour un environnement de développement.
Pas mal de choses ont changé depuis `l'article de 2022 <https://dotmobo.xyz/environnement-developpement-2022.html#environnement-developpement-2022>`_, et un
nouveau venu, `Astral <https://astral.sh/>`_ a tout chamboulé en proposant des outils ultra-performants écrits en **Rust**.


Versions de python, environnement virtuel et packaging
======================================================

`uv <https://github.com/astral-sh/uv>`_ est un formidable outil tout-en-un qui remplace **pyenv** et **poetry**.

Tu l'installes via :

.. code-block:: bash

    curl -LsSf https://astral.sh/uv/install.sh | sh

Pour installer une version de python, rien de plus simple avec la commande suivante :

.. code-block:: bash

    uv python install 3.13

Et pour ensuite créer un projet avec un environnement virtuel spécifique avec :

.. code-block:: bash

    uv init myapp -p 3.13
    cd myapp
    uv venv -p 3.13
    source .venv/bin/activate

Tu peux alors ajouter des librairies, exécuter des scripts, builder et publier ton projet sur PyPI avec :

.. code-block:: bash

    uv add requests
    echo 'print("Hello World!")' > main.py
    uv run python main.py
    uv build
    uv publish

L'outil utilise par défaut `pyproject.toml` pour les dépendances, s'inscrivant dans la lignée de **poetry** qui a popularisé ce format.

L'outil permet également d'installer les dépendances à la main avec un bon vieux **requirements.txt** via la commande :

.. code-block:: bash

    uv pip install -r requirements.txt

Il permet de gérer un lockfile comme pour npm, de gérer du cache et d'autres petites choses plutôt cool.
En plus niveau performance c'est vraiment très rapide.


Formatage du code
=================

On utilisait **black** et **isort**, mais `ruff <https://github.com/astral-sh/ruff>`_ fusionne maintenant le meilleur des deux mondes pour devenir le couteau suisse du linting et du formatage.

Tu l'ajoutes en dépendances dans ton projet avec uv :

.. code-block:: bash

    uv add ruff --dev

Pour faire du linting, c'est :

.. code-block:: bash

    uv run ruff check

Et pour formatter, c'est :

.. code-block:: bash

    uv run ruff format

On garde la configuration par défaut qui est très bien, pas besoin de se prendre la tête.

Typage statique
===============

Pour le typage, j'utilisais **mypy**, que j'ai ensuite délaissé pour **pyright**, mieux intégré aux éditeurs comme VS Code.

Mais Astral planche actuellement sur un concurrent appelé `ty <https://github.com/astral-sh/ty>`_ qui est encore en version
beta mais qui est très prometteur. J'ai déjà sauté le pas : mon usage du typage est assez simple et, pour l'instant, l'outil fait parfaitement l'affaire.
En tout cas niveau performance, par rapport aux deux autres, il n'y a pas photo.

Comme pour ruff, tu l'ajoutes à ton projet avec uv :

.. code-block:: bash

    uv add ty --dev

Et tu lances la vérification du typage avec :

.. code-block:: bash

    uv run ty check


Les trois outils **ruff**, **ty** et **uv** sont très bien intégrés dans **vscode** via les extensions officielles.

Franchement, merci Astral ! J'ai hâte de voir vos prochaines sorties.

Tests unitaires
===============

Encore rien de neuf sous le soleil, on utilise toujours `pytest <https://docs.pytest.org>`_ :

.. code-block:: bash

    uv add pytest --dev
    uv run pytest

Développement web
=================

Ces dernières années, un poids lourd a fait son apparition : `fastapi <https://fastapi.tiangolo.com/>`_. Il a détrôné **django**, **flask** et **bottle** en termes d'usage et de performance.

C'est devenu également mon choix par défaut. Il est simple et efficace comme on veut, permet de faire du sync et de l'async,
et surtout génère automatiquement la documentation openapi ! Il se base sur `pydantic <https://docs.pydantic.dev/latest/>`_
pour la validation des données, qui est aussi une petite librairie intéressante à connaitre.

Au niveau du code ça ressemble à ça, ultra clean :

.. code-block:: python

    from typing import Union

    from fastapi import FastAPI
    from pydantic import BaseModel

    app = FastAPI()


    class Item(BaseModel):
        name: str
        price: float
        is_offer: Union[bool, None] = None


    @app.get("/")
    def read_root():
        return {"Hello": "World"}


    @app.get("/items/{item_id}")
    def read_item(item_id: int, q: Union[str, None] = None):
        return {"item_id": item_id, "q": q}


    @app.put("/items/{item_id}")
    def update_item(item_id: int, item: Item):
        return {"item_name": item.name, "item_id": item_id}


JIT
===

Python 3.13 introduit un compilateur JIT pour pallier l'un de ses gros points faibles : les performances. Pour le moment, ce n'est pas encore complètement au point, mais il faut
savoir que `numba <https://numba.pydata.org/numba-doc/dev/user/jit.html>`_ propose déjà un compilateur JIT plutôt
efficace pour améliorer les performances de certaines fonctions.

Ça s'utilise de cette façon :

.. code-block:: python

    from numba import jit

    @jit
    def somme(n):
        total = 0
        for i in range(n):
            total += i
        return total

    print(somme(10000000))

Ça permet d'améliorer les performances de certaines fonctions de manière significative, sans pour autant devoir réécrire
tout le code en C ou Rust.

Au final, les outils convergent et l'écosystème Python se simplifie autour d'un consensus. C'est une excellente nouvelle.
