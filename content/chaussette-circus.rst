Diffuser une application web python avec chaussette, circus et nginx
####################################################################

:date: 2016-04-08
:tags: python,circus,chaussette,nginx,django,bottle,flask,mozilla,waitress
:category: Python
:slug: chaussette-circus
:authors: Morgan
:summary: Diffuser une application web python avec chaussette, circus et nginx

.. image:: ./images/chaussette.png
    :alt: Chaussette
    :align: right

Voilà, tu as enfin développé ton application django/bottle/flask (raye les
mentions inutiles) et tu es fin prêt à la rendre disponible au monde entier.

*Mais comment faire ? Quel serveur wsgi utiliser ? A l'aide !*

Il existe différentes alternatives, mais je vais te proposer celle que j'affectionne
tout particulièrement, à savoir le trio chaussette/circus/nginx.

1) Créer une application web
----------------------------

Tu vas commencer par créer une application `bottle <http://bottlepy.org/>`_
de base, pour changer de django tiens!

Tu crées et actives un environnement virtuel **myapp** en python 3.5 à l'aide de
*virtualenvwrapper* :

.. code-block:: python

    mkdir myproject && cd myproject
    mkvirtualenv -p /usr/bin/python3.5 myapp

Tu installes bottle dans ton virtualenv:

.. code-block:: bash

    pip install bottle

Dans le répertoire de ton projet, tu crées un module python **myapp** qui contient
un fichier vide **__init__.py** et un fichier **wsgi.py**:

.. code-block:: python

    mkdir myapp && touch myapp/__init__.py myapp/wsgi.py

Ton fichier **wsgi.py** doit ressembler à ça:

.. code-block:: python

    from bottle import route, template, default_app

    @route('/hello/<name>')
    def index(name):
        return template('<b>Hello {{name}}</b>!', name=name)

    application = default_app()

Pour information, sous django, le fichier à utiliser s'appelle aussi **wsgi.py**.

2) Installer chaussette et waitress
-----------------------------------

Maintenant, tu vas utiliser `chaussette <https://chaussette.readthedocs.org>`_
pour lancer ton application web.

Chaussette est `un serveur wsgi <http://sametmax.com/quest-ce-que-wsgi-et-a-quoi-ca-sert/>`_
qui permet le dialogue entre les requêtes http et ton application python.
Il autorise l'utilisation de différents backends wsgi, comme
`waitress <http://waitress.readthedocs.org/>`_ par exemple,
et a également la particularité de pouvoir servir ton application sur un socket déjà
ouvert. Dis comme ça, ça n'a l'air de rien, mais ça permet du coup d'utiliser un
manager de sockets comme circus ou supervisor.

Tu installes chaussette et waitress en étant **dans** le virtualenv **myapp**:

.. code-block:: bash

    pip install chaussette waitress

Et tu lances ton serveur wsgi depuis le répertoire de ton projet **myproject**:

.. code-block:: bash

    chaussette --backend waitress myapp.wsgi.application

Rends-toi sur `http://127.0.0.1:8080/hello/you <http://127.0.0.1:8080/hello/you>`_,
tu devrais voir ta page apparaître. Si tout est ok, tu peux couper chaussette et
passer à la suite.

3) Configurer circus
--------------------

Place au spectacle !

`Circus <http://circus.readthedocs.org/>`_ est, grosso-modo, un manager de processus
et de sockets compatible python 2 et python 3. C'est lui qui va se charger de
monitorer et de redémarrer tes applications.
Il permet d'utiliser les virtualenvs et se marie très bien
avec chaussette. Ce projet nous vient à l'origine de la
`fondation mozilla <https://www.mozilla.org/en-US/foundation/>`_.

Tu l'installes via pip **en dehors** du virtualenv **myapp** (donc en global sur ton système):

.. code-block:: bash

    deactivate
    apt-get install libzmq-dev libevent-dev
    sudo pip install circus

Et tu crées le fichier de configuration de circus **circus.ini** dans ton *home*
par exemple. C'est là que tu vas pouvoir configurer tes *watchers*, qui vont
lancer tes processus chaussette.

Dans le fichier **~/circus.ini**, tu mets:

.. code-block:: bash

    [circus]
    statsd = 1
    httpd = 0

    [watcher:myapp]
    cmd = /home/TONUSER/.virtualenvs/myapp/bin/chaussette --fd $(circus.sockets.web) --backend waitress myapp.wsgi.application
    working_dir = /home/TONUSER/LECHEMINVERSTONPROJET/myproject
    numprocesses = 3
    copy_env = 1
    use_sockets = 1
    virtualenv = /home/TONUSER/.virtualenvs/myapp
    virtualenv_py_ver = 3.5

    [socket:web]
    host = 127.0.0.1
    port = 8001

N'oublie pas de modifier les différents chemins de **working_dir**, **cmd** et
**virtualenv** pour que ça correspondent à ta propre machine. Tu peux également
configurer plusieurs *watchers** si tu souhaites monitorer plusieurs applications
web.

Enfin, tu lances le *daemon* de circus:

.. code-block:: bash

    circusd --daemon ~/circus.ini

Si tout s'est bien passé, tu devrais pouvoir utiliser la commande **circusctl**
pour voir le status de tes applications, les redémarrer et autres.
Sinon, tu peux exécuter **circusd** sans l'option **--daemon** pour debugger.

Tu peux voir ci-dessous quelques exemples d'utilisation de **circusctl**:

.. code-block:: bash

    circusctl --help # voir l'ensemble des commandes disponibles
    circusctl status # voir le status des applications
    circusctl listsockets # lister les sockets utilisés par les applications
    circusctl restart myapp # redémarrer myapp
    circusctl reload myapp # recharcher la configuration du watcher myapp

Rends-toi sur `http://127.0.0.1:8001/hello/you <http://127.0.0.1:8001/hello/you>`_
pour vérifier que tout fonctionne.

Grâce à circus, tu peux désormais manager plusieurs applications différentes,
qui tournent sous des environnements virtuels différents.

Pour information, il existe une interfaçe web pour monitorer circus appelé
**circus-web**, mais qui n'est pas encore compatible python 3.

3) Paramétrer nginx
-------------------

Bon, il ne te reste plus qu'à mettre en place nginx. C'est un
serveur http libre et performant qui est une très bonne alternative à apache.
Il va nous permettre de transmettre les requêtes http à circus/chaussette via les
sockets.

Tu l'installes via **apt** par exemple:

.. code-block:: bash

    apt-get install nginx

Et tu vas créer la configuration suivante dans **/etc/nginx/sites-available/myapp.conf**:

.. code-block:: bash

    upstream myapp  {
        server 127.0.0.1:8001;
    }
    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass      http://myapp$request_uri;
            proxy_redirect  off;
            proxy_set_header   Host             $host;
            proxy_set_header   X-Real-IP        $remote_addr;
        }
    }

Tu actives ta conf, tu supprimes le site par défaut et tu redémarres nginx:

.. code-block:: bash

    ln -s /etc/nginx/sites-available/myapp.conf /etc/nginx/sites-enabled/myapp
    rm /etc/nginx/sites-enabled/default
    service nginx restart #ou via systemd selon ta distro

Il ne te reste plus qu'à te rendre sur http://localhost/hello/you pour observer le résultat !
