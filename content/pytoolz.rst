Programmation fonctionnelle avec PyToolz
########################################

:date: 2016-03-03
:tags: python,pytoolz,programmation fonctionnelle,fonctions,mochi,pipe,curry
:category: Python
:slug: pytoolz
:authors: Morgan
:summary: Programmation fonctionnelle avec PyToolz

.. image:: ./images/python.png
    :alt: Python
    :align: right

`PyToolz <http://toolz.readthedocs.org/en/latest/index.html>`_ est un ensemble
de fonctions qui étendent *itertools* et *functools* de la librairie
standard. Ainsi, il va te permettre d'utiliser les
paradigmes de la programmation fonctionnelle en python.

Ce qui est sympa avec *PyToolz*, c'est qu'il est écrit en pur python et ne
dépend donc d'aucune librairie externe. De plus, il est compatible python 3.

Comme le veut la programmation fonctionnelle, les fonctions proposées sont
*composable*, *pure* et *lazy*. Si tout ça ne te parle pas, je t'invite à lire
le livre "`Apprendre Haskell vous fera le plus grand bien ! <http://lyah.haskell.fr/>`_"
pour te plonger dans l'univers de la programmation fonctionnelle.
Même si tu ne comptes pas développer en `Haskell <https://www.haskell.org/>`_,
il est intéressant d'en comprendre les concepts.

Mais retournons à *PyToolz*. Comme d'hab, tu l'installes avec pip:

.. code-block:: bash

    pip install toolz

Et tu peux maintenant utiliser toutes les méthodes de
`Itertoolz <http://toolz.readthedocs.org/en/latest/api.html#itertoolz>`_,
`Functoolz <http://toolz.readthedocs.org/en/latest/api.html#functoolz>`_ et
`Dictoolz <http://toolz.readthedocs.org/en/latest/api.html#dicttoolz>`_.

*Itertoolz* te permettra, par exemple, de retirer les éléments pairs d'une liste:

.. code-block:: python

    >>> from toolz.itertoolz import remove
    >>> list(remove(lambda x: x % 2 == 0, [1, 2, 3, 4, 5]))
    [1, 3, 5]

De récupérer les deux premiers éléments d'une liste:

.. code-block:: python

    >>> from toolz.itertoolz import take
    >>> list(take(2, [1, 2, 3, 4, 5]))
    [1, 2]

De partitionner une liste d'éléments en liste de tuples de deux éléments:

.. code-block:: python

    >>> from toolz.itertoolz import partition
    >>> list(partition(2, [1, 2, 3, 4, 5]))
    [(1, 2), (3, 4)]

Ou encore de retourner les différences entre deux listes:

.. code-block:: python

    >>> from toolz.itertoolz import diff
    >>> list(diff(["pommes", "poires", "bananes"], ["pommes", "poires", "oranges"]))
    [('bananes', 'oranges')]

*PyToolz* propose également la version *curryfiée* des différentes
fonctions pour en effectuer des applications partielles. Ici, on crée les
fonctions **remove_even** et **take_two**:

.. code-block:: python

    >>> from toolz.curried import remove, take
    >>> remove_even = remove(lambda x: x % 2 == 0)
    >>> list(remove_even([1, 2, 3, 4, 5]))
    [1, 3, 5]
    >>> take_two = take(2)
    >>> list(take_two([1, 2, 3, 4, 5]))
    [1, 2]

Et maintenant, place au fun avec **functoolz** ! Comme en *shell*, tu vas
pouvoir **piper** tes fonctions. Disons que tu veuilles les deux premiers
éléments non paires d'une liste:

.. code-block:: python

    >>> from toolz.curried import remove, take
    >>> from toolz.functoolz import pipe
    >>> remove_even = remove(lambda x: x % 2 == 0)
    >>> take_two = take(2)
    >>> list(pipe([1,2,3,4,5], remove_even, take_two))
    [1, 3]

Plutôt cool non ?

**Dictoolz**, quand à lui, permet entre autres de fusionner des dictionnaires:

.. code-block:: python

    >>> from toolz.dicttoolz import merge
    >>> merge({1: 'one'}, {2: 'two'})
    {1: 'one', 2: 'two'}

Ou d'appliquer une fonction aux valeurs d'un dictionnaire:

.. code-block:: python

    >>> from toolz.dicttoolz import valmap
    >>> bills = {"Alice": [20, 15, 30], "Bob": [10, 35]}
    >>> valmap(sum, bills)
    {'Alice': 65, 'Bob': 45}

Il y a évidemment tout un tas d'autres fonctions disponibles que je t'invite à découvrir !

Sinon, si tu veux pousser une peu plus loin la programmation fonctionnelle avec
python, il existe un langage intéressant appelé `Mochi <https://github.com/i2y/mochi>`_, dont l'interpréteur
convertit le code Mochi en bytecode Python 3.

Il permet d'écrire notamment ce genre de chose:

.. code-block:: python

    def fizzbuzz(n):
        match [n % 3, n % 5]:
            [0, 0]: "fizzbuzz"
            [0, _]: "fizz"
            [_, 0]: "buzz"
            _: n

    range(1, 31)
    |> map(fizzbuzz)
    |> pvector()
    |> print()

À découvrir !
