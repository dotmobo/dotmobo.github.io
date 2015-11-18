Introduction à Asyncio
######################

:date: 2015-11-15
:tags: python,asychrone,asyncio,aiohttp,requests,json,http,async,await,coroutine
:category: Python
:slug: introduction-asyncio
:authors: Morgan
:summary: Introduction à Asyncio

.. image:: ./images/python.png
    :alt: Django
    :align: right

La librairie `Asyncio <http://asyncio.org/>`_
a fait beaucoup parler d'elle dernièrement, au point d'être
intégrée dans la bibliothèque standard depuis la version 3.4 de Python.

C'est la réponse aux `goroutines <https://gobyexample.com/goroutines>`_
de `Go <https://golang.org/>`_, inscrivant ainsi Python dans la liste des
langages permettant la programmation asynchrone. Ce type de programmation permet
de ne pas bloquer son programme lors des opérations I/O qui peuvent durer un
certain temps et de réagir lors de la réception des informations au
lieu de les attendre. Ça permet ainsi d'optimiser et d'améliorer fortement les
performances de son code.

Je t'invite à te renseigner sur les différences entre programmation asynchrone,
parallèle et concurrente via `l'article de Sam&Max <http://sametmax.com/la-difference-entre-la-programmation-asynchrone-parallele-et-concurrente/>`_
et `la vidéo de Jonathan Worthington <https://www.youtube.com/watch?v=JpqnNCx7wVY>`_ du monde Perl.

Asyncio utilise une boucle d'événements qui va contenir l'ensemble de nos tâches
à exécuter. Ces tâches devront être sous la forme de `coroutines <http://sametmax.com/quest-ce-quune-coroutine-en-python-et-a-quoi-ca-sert/>`_,
qui sont des sortes de générateurs inversés, c'est-à-dire qu'on y envoie des données à la place
d'en reçevoir. C'est le côté *lazy* des coroutines qui permet à Asyncio de les
exécuter en asynchrone.

Trêve de blabla et passons à la pratique. Il y a déjà beaucoup d'articles sur le net
traitant du fonctionnement d'Asyncio et ce n'est pas forcément facile
de s'y retrouver. Tu vas donc voir ici un cas d'usage concret, qui est le développement
d'un aggrégateur de données *json* performant. Le tutorial sera en python 3.5,
ce qui te permettra d'utiliser les nouveaux mots clés **async** et **await**.

Tu utiliseras la boucle d'événements, les coroutines et les objets **Future**.
L'idée n'est pas de faire le code le plus simple et performant possible, mais plutôt de passer
en revue l'ensemble des concepts et mots-clés utiles.

Pour Asyncio, il n'y a rien à installer à part python 3.5. Par contre, il va te
falloir `aiohttp <https://github.com/KeepSafe/aiohttp>`_ pour faire les requêtes http:

.. code-block:: bash

    pip install aiohttp

Et c'est là où le bât blesse. Tu ne pourras pas utiliser `requests <http://docs.python-requests.org/en/latest/>`_ par exemple, car
il faut utiliser des outils compatibles avec Asyncio, c'est-à-dire écrits sous forme
de coroutines. Sinon, le programme bloquera la boucle d'événements et ça ne sera
pas asynchrone. Pareil pour les accès *BDD*, il faut utiliser `aiopg <https://github.com/aio-libs/aiopg>`_ pour postgresql par exemple.

Tu crées un fichier *asyncio35.py*, tu importes *aiohttp* et *asyncio* et tu déclares ta liste
d'urls:

.. code-block:: python

    import asyncio
    import aiohttp

    URLS = ['http://ip.jsontest.com/', 'http://headers.jsontest.com/',
            'http://date.jsontest.com/']

Tu vas alors créer ta coroutine qui va récupérer les données renvoyées par une
url et les insérer dans un objet **Future**:

.. code-block:: python

    async def call_url(client, url, future):
        """ Coroutine récupérant les données provenant d'une url """
        async with client.get(url) as response:
            result = await response.json()
            future.set_result(result)

Plusieurs explications sont nécessaires ici:

* **async**: Nouveau mot-clé introduit en python 3.5, à mettre avant le **def**, qui permet de spécifier que cette méthode est une coroutine asynchrone. Ça vient remplacer le **@asyncio.coroutine** de python 3.4.
* **async with**: Permet d'utiliser des *context managers* asynchrones.
* **await**: Bloque l'exécution de la coroutine jusqu'à la fin du traitement de l'instruction, ici **response.json()**. Ça vient remplacer le **yield from** de python 3.4.
* **future.set_result**: Définit la valeur de l'objet **Future**.

Ensuite, dans ton *main*, tu initalises ta boucle, ton client *aiohttp*, ta liste
de tâches et ta liste de résultats:

.. code-block:: python

    if __name__ == "__main__":
        # On initialise les variables
        list_results, list_tasks = [], []
        loop = asyncio.get_event_loop()
        client = aiohttp.ClientSession(loop=loop)

Tu ajoutes ton *callback* pour les objets **Future**:

.. code-block:: python

    def fill_results_list(future):
        """ Callback de l'objet future qui ajoute sa valeur dans une liste """
        list_results.append(future.result())

Pour chaque url, tu vas:

* créer un objet **Future**.
* ajouter la méthode **call_url** à la liste des tâches à accomplir via la méthode **ensure_future**.
* ajouter ton *callback* **fill_results_list** à ton objet **Future** via la méthode **add_done_callback**.

.. code-block:: python

    # On créé les objets Future et la liste des tâches
    for url in URLS:
        future = asyncio.Future()
        list_tasks.append(asyncio.ensure_future(call_url(client, url, future)))
        future.add_done_callback(fill_results_list)

Puis, il suffit de lancer l'exécution des tâches de manière asynchrone via
la boucle d'événements et sa méthode **run_until_complete**. Ton programme
sera bloqué ici jusqu'à la fin du traitement de toutes les tâches et donc de la
réception des objets **Future** via **asyncio.wait**. À la fin, il affiche la liste
des résultats sur la sortie standard:

.. code-block:: python

    # Exécution des tâches
    loop.run_until_complete(asyncio.wait(list_tasks))
    print(list_results)

Enfin, tu peux fermer le client *aiohttp* et la boucle d'événements:

.. code-block:: python

    # Ferme le client et la boucle
    client.close()
    loop.close()

Encore une chose concernant la boucle. Celle-ci est unique pour tout le programme.
Donc il faut faire attention quand tu la manipules à plusieurs endroits du code,
et quand tu la fermes.

Voici le résultat final :

.. code-block:: python

    import asyncio
    import aiohttp

    """
    Aggrégation de données provenant d'urls
    """

    URLS = ['http://ip.jsontest.com/', 'http://headers.jsontest.com/',
            'http://date.jsontest.com/']

    async def call_url(client, url, future):
        """ Coroutine récupérant les données provenant d'une url """
        async with client.get(url) as response:
            result = await response.json()
            future.set_result(result)

    if __name__ == "__main__":
        # On initialise les variables
        list_results, list_tasks = [], []
        loop = asyncio.get_event_loop()
        client = aiohttp.ClientSession(loop=loop)

        def fill_results_list(future):
            """ Callback de l'objet future qui ajoute sa valeur dans une liste """
            list_results.append(future.result())

        # On créé les objets Future et la liste des tâches
        for url in URLS:
            future = asyncio.Future()
            list_tasks.append(asyncio.ensure_future(call_url(client, url, future)))
            future.add_done_callback(fill_results_list)

        # Exécution des tâches
        loop.run_until_complete(asyncio.wait(list_tasks))
        print(list_results)

        # Ferme le client et la boucle
        client.close()
        loop.close()


Et hop, tu exécutes tout ça:

.. code-block:: bash

    $ time python asyncio35.py
    [{'ip': '109.221.53.120'},
    {'Host': 'headers.jsontest.com', 'User-Agent': 'Python/3.5 aiohttp/0.18.4', 'Accept': '*/*', 'Content-Length': '0'},
    {'date': '11-14-2015', 'time': '03:16:45 PM', 'milliseconds_since_epoch': 1447514205836}]

    real	0m0.511s
    user	0m0.263s
    sys	0m0.033s

*"Ok c'est sympa mais est-ce que c'est vraiment plus rapide en asynchrone ?"*

Tu veux une preuve ? En voici une; le même programme sans Asyncio:

.. code-block:: python

    import requests

    """
    Aggrégation de données provenant d'urls
    """

    URLS = ['http://ip.jsontest.com/', 'http://headers.jsontest.com/',
            'http://date.jsontest.com/']

    if __name__ == "__main__":
        list_results = []
        for url in URLS:
            result = requests.get(url)
            list_results.append(result.json())

        print(list_results)


Tu l'exécutes:

.. code-block:: bash

    $ time python noasyncio35.py
    [{'ip': '109.221.53.120'},
    {'Host': 'headers.jsontest.com', 'User-Agent': 'python-requests/2.8.1', 'Accept': '*/*'},
    {'date': '11-14-2015', 'time': '11:57:03 AM', 'milliseconds_since_epoch': 1447502223337}]

    real	0m1.188s
    user	0m0.247s
    sys	0m0.017s

Le double de temps ! Convaincu ?

Alors évidemment, ce n'est qu'un simple cas d'usage. Il y a beaucoup, mais
vraiment beaucoup plus à voir dans `la doc officielle <https://docs.python.org/3/library/asyncio.html>`_.
