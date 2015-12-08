Httpie, le client http intuitif
###############################

:date: 2015-12-08
:tags: httpie,http,python,curl,json
:category: Python
:slug: httpie
:authors: Morgan
:summary: Httpie, le client http intuitif

.. image:: ./images/http.png
    :alt: Httpie
    :align: right


`Httpie <http://httpie.org>`_ est un client http en ligne de commande plutôt 
bien foutu. C'est une alternative viable à `curl <http://curl.haxx.se/>`_ qui
a été développée en python.

Intuitif, simple, et prenant en charge la coloration syntaxique, c'est l'outil
idéal pour requêter des APIs JSON par exemple.

Tu l'installes avec pip :

.. code-block:: bash

    pip install httpie

Tu disposes maintenant de la commande **http** dans ton terminal qui te
permettra d'effectuer des requêtes très simplement de cette manière:

.. code-block:: bash

    http [flags] [METHOD] URL [ITEM [ITEM]]


Tu peux évidemment faire du GET:

.. code-block:: bash

    http httpie.org
    http GET httpie.org

Du DELETE:

.. code-block:: bash

    http DELETE example.org/todos/7

Ou mettre à jour les données d'une API via PUT:

.. code-block:: bash

    http PUT example.org X-API-Token:123 name=John

Tu remarques ici qu'on a d'abord passé la méthode PUT, puis l'url, puis le token
d'authentification dans l'entête de la requête, et enfin les données.

Pas besoin d'utiliser des options pour spécifier chaque élément, tout se fait intuitivement !
Les éléments de l'entête de la requête sont séparés par **:**, les données par
**=**.

Tu peux aussi utiliser l'option **-a** pour l'authentification type
username/password.

Par exemple, pour poster un commentaire sur un problème via l'api github:

.. code-block:: bash

    http -a USERNAME POST https://api.github.com/repos/jkbrzt/httpie/issues/83/comments body='HTTPie is awesome!'

Tu peux utiliser les symboles de redirection pour uploader
ou downloader des fichiers :

.. code-block:: bash

    http example.org < file.json
    http example.org > file.json

L'outil est très complet (gestion des sessions, des certificats SSL) mais je 
l'apprécie surtout pour son côté simple et facile d'accès.

Tu vas pouvoir manipuler et tester tes APIs très rapidement, sans te prendre la
tête avec une documentation imbuvable!


