Introduction à Asyncio
######################

:date: 2015-11-15
:tags: python,asychrone,asyncio
:category: Python
:slug: introduction-asyncio
:authors: Morgan
:summary: Introduction à Asyncio

.. image:: ./images/python.png
    :alt: Django
    :align: right

La libraire Asyncio a fait beaucoup parler d'elle dernièrement, au point d'être
intégrer dans la bibliothèque standard depuis la version 3.4 de python.

C'est la réponse aux goroutines de go, inscrivant ainsi python dans la liste des
langages permettant la programmation asynchrone. Ce type de programmation permet
de ne pas bloquer son programme lors des opérations I/O qui peuvent durer un
certain temps et donc de réagir en fonction de la réception des informations au
lieu de les attendre. Ça permet ainsi d'optimiser et d'améliorer fortement les
performances de son code.

Je t'invite à te renseigner sur les différences entre programmation asynchrone,
parallèle et concurrente via l'article de Sam&Max et la vidéo de Jonathan
Worthington du monde Perl.

Asyncio utilise une boucle d'évenements qui va contenir l'ensemble de nos tâches
à exécuter. Ces tâches devront être sous la forme de `coroutines <http://sametmax.com/quest-ce-quune-coroutine-en-python-et-a-quoi-ca-sert/>`_,
qui sont des sortes de générateurs inversés, c-à-d qu'on y envoie des données à la place
d'en reçevoir. C'est le côté lazy des coroutines qui permet à asyncio de les
exécuter en asynchrone.

Trêve de blabla et passons à la pratique. Il y a déjà beaucoup d'article sur le net
traitant de tous le fonctionnement d'Asyncio et çe n'est pas forcément facile
de s'y retrouver. Tu vas donc voir ici un cas d'usage, c-à-d comment développer
un aggrégateur de données html performant. Le tutorial sera en python 3.5,
ce qui te permettra d'utiliser les nouveaux mots clés **async** et **await**.

Tu utiliseras la boucle d'évenement, les coroutines et les objets **Future**.
L'idée, c'est surtout de passer en revue l'ensemble des concepts et mots clés utiles.

Pour Asyncio, rien besoin d'installer à part python 3.5. Par contre, il va te
falloir aiohttp pour faire les requêtes html:

.. code-block:: bash

    pip install aiohttp

Et c'est là où le bât blesse. Tu ne pourra pas utiliser requests par exemple, car
il faut utiliser des outils compatible avec asyncio, c'est à dire écrit sous forme
de coroutines. Sinon, le programme bloquera la boucle d'évenement et ça ne sera
pas asynchrone. Pareil pour les accès bdd, il faut utiliser aiopg pour postgresql.

Tu créer un fichier *.py*, tu importes aiohttp et asyncio et tu déclares ta liste
d'urls:

.. code-block:: python

    import asyncio
    import aiohttp

    URLS = ['http://ip.jsontest.com/', 'http://headers.jsontest.com/',
            'http://date.jsontest.com/']

Tu va alors créer ta coroutines qui va récupérer les données renvoyées par une
url et les insérer dans un objet **Future**:

.. code-block:: python

    async def call_url(client, url, future):
        """ Coroutine récupérant les données provenant d'une url """
        async with client.get(url) as response:
            result = await response.json()
            future.set_result(result)

Plusieurs explications sont nécessaires ici:
 * **async**: Nouveau mot-clé introduit en python 3.5, à mettre avant le **def**,
   qui permet de spécifier que cette méthode est une coroutine asynchrone.
   Ça vient remplacer le **@asyncio.coroutine** de python 3.4.
 * **async with**: Permet d'utiliser des *context managers* asynchrones.
 * **await**: Bloque l'exécution de la coroutine jusqu'à la fin du traitement
   de l'instruction, ici **response.json()*. Ça vient remplacer le **yield from**
   de python 3.4.
 * **future.set_result**: Définit la valeur de l'objet **Future**.

 Ensuite, dans ton *main*, tu initalise ta boucle, ton client aiohttp, ta liste
 de tâches et ta liste de résultats

.. code-block:: python

    if __name__ == "__main__":
        # On initialise les variables
        list_results, list_tasks = [], []
        loop = asyncio.get_event_loop()
        client = aiohttp.ClientSession(loop=loop)

Tu ajoute ta méthode de callback pour les objets **Future**:

.. code-block:: python

    def fill_results_list(future):
        """ Callback de l'objet future qui ajoute sa valeur dans une liste """
        list_results.append(future.result())

Pour chaque url, tu va créer un objet **Future**, ajouter la méthode **call_url**
à la liste de tâches à accomplir via la méthode **ensure_future** et ajouter
la méthode de callback **fill_results_list** à ton objet **Future** via la méthode
**add_done_callback**:

.. code-block:: python

    # On créé les objets Future et la liste des tâches
    for url in URLS:
        future = asyncio.Future()
        list_tasks.append(asyncio.ensure_future(call_url(client, url, future)))
        future.add_done_callback(fill_results_list)

Puis, il suffit de lancer l'exécution des tâches de manières asynchrone via
la boucle d'évenement et la méthode **loop.run_until_complete**. Ton programme
sera bloqué ici jusqu'à la fin du traitement de toute les tâches et donc de la
réception des **Future** via **asyncio.wait**. A la fin, il affiche la liste
des résultats sur la sortie standard:

.. code-block:: python

    # Exécution des tâches
    loop.run_until_complete(asyncio.wait(list_tasks))
    print(list_results)

Enfin, tu peux fermer le client aiohttp et la boucle d'évenement.

.. code-block:: python

    # Ferme le client et la boucle
    client.close()
    loop.close()

Encore une chose concernant la boucle. Celle-ci est unique pour tous le programme.
Donc il faut faire attention quand tu la manipule à plusieurs endroits du code,
et quand tu la ferme.

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


Et hop, tu exécute tout ça:

.. code-block:: bash

    $ time python asyncio35.py
    [b'{\n   "Host": "headers.jsontest.com",\n   "Content-Length": "0",\n   "User-Agent": "Python/3.5 aiohttp/0.18.4",\n   "Accept": "*/*"\n}\n', b'{"ip": "109.221.53.120"}\n', b'{\n   "time": "11:52:32 AM",\n   "milliseconds_since_epoch": 1447501952998,\n   "date": "11-14-2015"\n}\n']

    real	0m0.511s
    user	0m0.263s
    sys	0m0.033s

"Ok c'est sympa mais est-ce que c'est vraiment plus rapide en asynchrone ?"

Tu veux une preuve ? En voici une; le même programme sans asyncio:

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
    [{'ip': '109.221.53.120'}, {'Host': 'headers.jsontest.com', 'User-Agent': 'python-requests/2.8.1', 'Accept': '*/*'}, {'date': '11-14-2015', 'time': '11:57:03 AM', 'milliseconds_since_epoch': 1447502223337}]

    real	0m1.188s
    user	0m0.247s
    sys	0m0.017s

Le double de temps ! Convaincu ?

Alors évidemment, ce n'est qu'un simple cas d'usage. Il y a beaucoup plus à voir
dans la doc officielle.
