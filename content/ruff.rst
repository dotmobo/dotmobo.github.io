Ruff : le linter tout-en-un
###########################

:date: 2024-08-05
:tags: ruff, python, linter, format, black, isort, flake8, pep8, rust, pylint
:category: Python
:slug: ruff
:authors: Morgan
:summary: Ruff : le linter tout-en-un

.. image:: ./images/python.png
    :alt: Python
    :align: right

La guerre a fait rage pendant de nombreuses années concernant les **linters** et **formatters** Python.

On a d'abord eu **autopep8** qui faisait le taf mais qui était plutôt limité. Puis sont arrivés en vrac **Flake8**, **Pyflakes** ou encore **Pylint**
qui se sont battus pour devenir le meilleur linter de l'écosystème, mais en vain.

C'est alors qu'est venu `Go <https://go.dev/>`_ avec son excellent linter intégré **gofmt** qui faisait magnifiquement le travail.
Pas de configuration compliquée ici, juste une commande à taper et tout le monde obtient le même formatage. Il n'a pas fallu longtemps à la 
communauté Python pour copier l'idée (à raison) et sortir un équivalent, nommé `Black <https://github.com/psf/black>`_. 

Ouf, la guerre des linters est enfin finie et tout le monde a adopté **black**, on peut donc passer à autre chose non ?

*Eh bien non !*

Un petit dernier est arrivé et enfonce le clou en faisant tout comme **black**, mais en mieux.

Il s'appelle `Ruff <https://astral.sh/ruff>`_ et se veut ultra rapide et performant car il est écrit en Rust.

L'idée ici est vraiment d'avoir l'unique outil final tout-en-un. C'est une sorte de fusion de **black** et de **isort**.

Tu peux l'installer directement en stand-alone via la commande suivante :

.. code-block:: bash

    curl -LsSf https://astral.sh/ruff/install.sh | sh

Tu as alors à ta disposition deux commandes que tu peux exécuter.

La première va vérifier ton code et t'afficher les erreurs :

.. code-block:: bash

    ruff check

La seconde va automatiquement formater ton code : 

.. code-block:: bash

    ruff format

Et voilà, c'est tout ! Tu peux t'arrêter ici et utiliser l'outil de base de cette manière sans te prendre la tête avec une configuration ou autres.

Tu as même une `extension pour VS Code officielle <https://github.com/astral-sh/ruff-vscode>`_ si tu veux l'intégrer directement à ton éditeur.

Et si vraiment tu veux aller plus loin, tu peux configurer un `hook de pre-commit <https://github.com/astral-sh/ruff-pre-commit>`_ ou encore une
`GitHub action <https://github.com/chartboost/ruff-action>`_.

Enfin, pour overrider la `configuration <https://docs.astral.sh/ruff/configuration/>`_ par défaut, tu peux créer un fichier **ruff.toml** et l'éditer :

.. code-block:: toml

    # Exclude a variety of commonly ignored directories.
    exclude = [
        ".bzr",
        ".direnv",
        ".eggs",
        ".git",
        ".git-rewrite",
        ".hg",
        ".ipynb_checkpoints",
        ".mypy_cache",
        ".nox",
        ".pants.d",
        ".pyenv",
        ".pytest_cache",
        ".pytype",
        ".ruff_cache",
        ".svn",
        ".tox",
        ".venv",
        ".vscode",
        "__pypackages__",
        "_build",
        "buck-out",
        "build",
        "dist",
        "node_modules",
        "site-packages",
        "venv",
    ]

    # Same as Black.
    line-length = 88
    indent-width = 4

    # Assume Python 3.8
    target-version = "py38"

    [lint]
    # Enable Pyflakes (`F`) and a subset of the pycodestyle (`E`) codes by default.
    select = ["E4", "E7", "E9", "F"]
    ignore = []

    # Allow fix for all enabled rules (when `--fix`) is provided.
    fixable = ["ALL"]
    unfixable = []

    # Allow unused variables when underscore-prefixed.
    dummy-variable-rgx = "^(_+|(_+[a-zA-Z0-9_]*[a-zA-Z0-9]+?))$"

    [format]
    # Like Black, use double quotes for strings.
    quote-style = "double"

    # Like Black, indent with spaces, rather than tabs.
    indent-style = "space"

    # Like Black, respect magic trailing commas.
    skip-magic-trailing-comma = false

    # Like Black, automatically detect the appropriate line ending.
    line-ending = "auto"

Mais franchement je ne le conseillerais pas, sauf raison vraiment majeure et indispensable.
Autant garder la configuration par défaut pour rester dans l'idée d'origine de la simplicité de **gofmt**.

Happy coding !