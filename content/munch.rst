Munch, un dictionnaire qui supporte les accesseurs
##################################################

:date: 2017-11-09
:tags: python,bunch,munch,object,dict
:category: Python
:slug: munch
:authors: Morgan
:summary: Munch, un dictionnaire qui supporte les accesseurs

.. image:: ./images/python.png
    :alt: Python
    :align: right

`Munch <https://github.com/Infinidat/munch>`_ est une petite librairie bien pratique et bien pensé.

En gros, elle permet d'utiliser les accesseurs pour accéder aux éléments de tes dictionnaires, à la manière d'un objet python.

Ça peut être utile notamment dans les tests unitaires, si tu as besoin de mocker rapidement un objet par exemple.

Tu écris un dictionnaire qui correspond à ton objet, tu le *munchify* et hop !

Si dans une fonction que tu veux tester, tu as utilisé des accesseurs sur un objet, ton *munch* sera considéré comme l'objet en question.

C'est à priori un fork de `Bunch <https://github.com/dsc/bunch>`_, mais maintenu et qui fonctionne en python 3.

Tu l'installes avec **pip** :

.. code-block:: bash

    pip install munch

Tu importes **munchify** et tu convertis ton dictionnaire en **munch** :

.. code-block:: python

    >>> from munch import munchify

    >>> data = {
            "last_name": "Dupont",
            "first_name": "Jean",
            "age": 30,
            "activities": ["football", "ping-pong"],
            "job": {
                "name": "Developer",
                "enterprise": "Mozilla"
            }
        }

    >>> mymunch = munchify(data)

    >>> mymunch.last_name
    'Dupont'
    >>> mymunch.first_name = "Pierre"
    >>> mymunch.first_name
    'Pierre'
    >>> mymunch.activities[0]
    'football'
    >>> mymunch.job.enterprise
    'Mozilla'

Voilà c'est tout ! 

Tu as accès aux différentes méthodes des dictionnaires, comme *keys()* et *update()*, ainsi qu'à l'itération et à l'opérateur *splat*.
Ça supporte également la sérialization en JSON et en YAML.
    





