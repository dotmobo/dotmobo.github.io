Intégration continue sous Github avec Tox et Travis
###################################################

:date: 2015-10-25
:tags: python,github,travis,tox,intégration continue,coveralls,tests unitaires,landscape,coverage
:category: Python
:slug: integration-continue
:authors: Morgan
:summary: Intégration continue sous Github avec Tox et Travis

.. image:: https://travis-ci.com/img/travis-mascot-200px.png
    :alt: Travis
    :align: right

L'`intégration continue <https://fr.wikipedia.org/wiki/Int%C3%A9gration_continue>`_
est une part très importante d'un projet, à ne surtout pas négliger.
Elle permet de vérifier constamment son code via des tests unitaires,
généralement à chaque *commit*. Ceci permet de tester la qualité et la robustesse
du code et d'éviter toutes régressions.

Dans cet article, tu verras comment mettre en place l'intégration continue d'une application
`python <https://www.python.org/>`_ sous `Github <https://github.com/>`_. À la fin de cette lecture, tu seras capable:

* d'écrire un test unitaire simple.
* de vérifier la couverture de ton code.
* d'exécuter tes tests sous plusieurs versions de python.
* d'automatiser l’exécution des tests à chaque *commit*.
* d'automatiser la vérification de la couverture du code.
* d'automatiser l'analyse de la qualité de ton code.
* d'utiliser les badges github pour l'affichage des rapports.

L'application de démo de ce tuto est dispo `ici <https://github.com/dotmobo/demo-integration-continue>`_.


1) Créer une application
------------------------

Dans le répertoire de ton projet *myproject*, tu vas créer un package *myapp* contenant le
classique *__init__.py*, ainsi qu'un fichier *maths.py*.
Celui-ci contiendra une méthode d'addition et de soustraction:

.. code-block:: python

    # -*- coding: utf-8 -*-

    """
    Provides an addition function and a subtraction function
    """


    def addition(a, b):
        """ Méthode d'addition """
        return a + b


    def subtraction(a, b):
        """ Méthode de soustraction """
        return a - b


Tu vas donc mettre en place l'intégration continue sur ce petit bout de code.

Tu ajoutes également dans le répertoire du projet le fichier *setup.py* suivant:

.. code-block:: python

    #!/usr/bin/env python

    from setuptools import setup

    setup(name='myproject',
      version='1.0',
      description='My project',
      author='Me',
      author_email='me@noreply.com',
      url='http://myproject',
      packages=[],
      )

Puis, tu exécutes la commande suivante afin d'ajouter ton application dans le *path*
python:

.. code-block:: python

    python setup.py develop


2) Ajouter des tests unitaires
--------------------------------

Tu vas maintenant créer des tests unitaires à l'aide de
`unittest <https://docs.python.org/3/library/unittest.html>`_.

Au même niveau que ton package *myapp*, tu vas créer un package *tests* qui sera
dédié aux tests unitaires. Celui-ci doit contenir le fichier *__init__.py* et le
fichier *test_maths.py* suivant:

.. code-block:: python


    # -*- coding: utf-8 -*-
    """
    Tests unitaires
    """
    from unittest import TestCase, main
    from myapp.maths import addition, subtraction


    class MathsTest(TestCase):
        """
        Classe qui va contenir nos test unitaires
        """
        def setUp(self):
            """ Méthode qui permet d'initialiser des variables pour nos tests """
            self.a = 25
            self.b = 12

        def test_addition(self):
            """ Test de l'addition """
            self.assertEqual(addition(self.a, self.b), 37)

        def test_subtraction(self):
            """ Test de la soustraction """
            self.assertEqual(subtraction(self.a, self.b), 13)

        def tearDown(self):
            """ Méthode appelée à la fin des tests """
            self.a = None
            self.b = None

    if __name__ == '__main__':
        main()

Et pour vérifier le bon fonctionnement de tes tests, tu peux les exécuter via:

.. code-block:: bash

    python tests/test_maths.py

Pour plus d'informations concernant les tests unitaires, je t'invite à te pencher
sur le dossier de Sam&Max :

* http://sametmax.com/un-gros-guide-bien-gras-sur-les-tests-unitaires-en-python-partie-1/
* http://sametmax.com/un-gros-guide-bien-gras-sur-les-tests-unitaires-en-python-partie-2/
* http://sametmax.com/un-gros-guide-bien-gras-sur-les-tests-unitaires-en-python-partie-3/
* http://sametmax.com/un-gros-guide-bien-gras-sur-les-tests-unitaires-en-python-partie-4/


3) Couvrir son code avec Coverage
---------------------------------

Tu vas maintenant ajouter les utilitaires permettant la couverture de ton code.

Premièrement, tu installes `coverage <https://bitbucket.org/ned/coveragepy>`_:

.. code-block:: bash

    pip install coverage

Puis, tu crées le fichier de configuration de coverage appelé *.coveragerc*
dans ton répertoire *myproject*:

.. code-block:: bash

    [run]
    source =
        myapp

    [report]
    omit = */tests/*

Tu y indiques d'exéctuer les tests de ton application *myapp*, tout en
ignorant d'analyser la couverture des fichiers de tests.
Sinon, il faudrait faire des tests unitaires pour tester les tests unitaires !

Tu lances les tests unitaires avec coverage:

.. code-block:: bash

    coverage run -m unittest discover tests/

Tu peux désormais afficher un rapport simple via:

.. code-block:: bash

    coverage report

Ou un rapport html via:

.. code-block:: bash

    coverage html

Celui-ci s'est créé dans le répertoire *htmlcov*. A l'aide de ce rapport, tu
vas pouvoir visualiser le pourcentage de code couvert ainsi que les zones de code
couvertes et non couvertes, fichier par fichier. Plutôt pratique non ?

4) Utiliser Tox pour l'exécution des tests
------------------------------------------

`Tox <https://testrun.org/tox/latest/>`_ vise à standardiser l'exécution des tests
unitaires en python. Il permet, à l'aide d'environnements virtuels, de tester ton
code sous plusieurs interpréteurs python et sous plusieurs versions de librairies.

Il est très simple d'utilisation et s’interface parfaitement avec Travis.

Tu peux l'installer via pip:

.. code-block:: bash

    pip install tox

Ensuite, il te faut créer le fichier *tox.ini* dans le répertoire *myproject*:

.. code-block:: python

    [tox]
    envlist=py27,py34

    [testenv]
    deps=coverage
    commands=coverage run -m unittest discover tests/

Explication:

* *envlist* permet de lister les interpréteurs python que l'on veut tester. Ici,
  tu vas tester ton application sous python 2.7 et python 3.4. Il faut évidemment
  les installer sur ton système si ce n'est pas déjà fait.
* *deps* liste les dépendances à installer dans le virtualenv qui sera créé.
* *commands* indique la commande à exécuter pour lancer les tests unitaires.
* il y a plein d'autres paramètres utilisables, va voir dans la
  `doc officielle <https://testrun.org/tox/latest/example/basic.html>`_.

Enfin, pour exécuter tes tests sous les différents environnements, lance la
commande:

.. code-block:: bash

    tox

Plutôt simple non ?

Crée-toi un dépôt sur Github et *commit* tout ça.

5) Activer l'intégration continue de notre projet sous Travis et Coveralls
--------------------------------------------------------------------------

`Travis <https://travis-ci.org/>`_ est un outil d'intégration continue, à la
manière de `Jenkins <https://jenkins-ci.org/>`_. C'est lui qui va exécuter tes
tests unitaires à chaque *commit*, et qui va t'envoyer un mail si un problème a
été rencontré.

Tu peux t'y connecter via ton compte Github et y ajouter ton dépôt git via le bouton *+*.

Au préalable, il faut créer un fichier *.travis.yml* dans ton répertoire *myproject*:

.. code-block:: yaml

    language: python
    python: "2.7"
    env:
    - TOX_ENV=py27
    - TOX_ENV=py34
    install:
    - pip install tox
    script: tox -e $TOX_ENV
    after_success:
    - pip install coveralls
    - coveralls

On y indique les environnements de tox à tester et le script tox à exécuter.

Tu peux maintenant *commiter* tout ça sur ton dépôt Github, et te rendre sur le site
de travis pour visualiser les rapports d'exécution de tes tests!

*"Attends un peu, c'est quoi la partie qui est dans le after_success, coveralls?"*

Bien vu! `Coveralls <https://coveralls.io/>`_ est un outil qui permet de tester
la couverture de code à chaque *commit*.

Connecte-toi sur leur plate-forme via ton compte Github et active ton dépôt git via le bouton
*add repos*.

Tu vas ainsi pouvoir voir l'évolution de la couverture de code et analyser les rapports proposés.


6) Inspecter la qualité du code avec Landscape.io
-------------------------------------------------

Landscape.io est une plate-forme qui va inspecter la qualité de ton code à chaque *commit*.
Celle-ci est gratuite pour les projets open-source disponibles sur Github.

Elle se base sur `flake8 <https://flake8.readthedocs.org/en/2.4.1/>`_ comme outil
d'inspection de code.

Connecte-toi sur la plate-forme avec ton compte Github et ajoutes-y ton dépôt git
via *Add repository*.

Tu devras peut-être refaire un *commit* pour activer le bazar.


7) Ajouter des badges sur github
--------------------------------

Tu va pouvoir te créer un fichier *README.rst* et y ajouter les badges *travis*,
*coveralls* et *landscape*. Tu peux trouver ces badges sous différents formats, notamment en
`restructuredText <http://sphinx-doc.org/rest.html>`_, dans la configuration de
ton projet sur ces trois plate-formes.

Exemple:

.. code-block:: yaml

    demo-integration-continue
    -------------------------

    Application de démo d'intégration continue sous github

    .. image:: https://travis-ci.org/dotmobo/demo-integration-continue.svg
        :target: https://travis-ci.org/dotmobo/demo-integration-continue

    .. image:: https://coveralls.io/repos/dotmobo/demo-integration-continue/badge.svg?branch=master&service=github
        :target: https://coveralls.io/github/dotmobo/demo-integration-continue?branch=master

    .. image:: https://landscape.io/github/dotmobo/demo-integration-continue/master/landscape.svg?style=flat
        :target: https://landscape.io/github/dotmobo/demo-integration-continue/master
        :alt: Code Health

*Commit* et rends-toi sur ton dépôt github pour voir
`le résultat <https://github.com/dotmobo/demo-integration-continue>`_!
