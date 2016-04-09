Servir son application web python avec Chaussette, Circus et Nginx
##################################################################

:date: 2016-04-08
:tags: python,circus,chaussette,nginx,django,bottle,flask,mozilla
:category: Python
:slug: chaussette-circus
:authors: Morgan
:summary: Servir son application web python avec Chaussette, Circus et Nginx

.. image:: ./images/chaussette.png
    :alt: Chaussette
    :align: right

Voilà, tu as enfin développé ton application django/bottle/flask (rayes les
mentions inutiles) et tu es fin prêt à la rendre disponible au monde entier.

*Mais comment faire ? Quel serveur wsgi utiliser ? A l'aide !*

Il existe différentes alternatives mais je vais te proposer celle que j'affectionne
tout particulièrement, à savoir utiliser le trio chaussette/circus/nginx.

Tu vas commencer par créer une application bottle de base (pour changer de django
tiens!)

Tu crées et actives un environnement virtuel à l'aide de *virtualenvwrapper* en
python 3.5 que tu appelles **myapp**:

.. code-block:: python

    mkvirtualenv -p /usr/bin/python3.5 myapp

Dans le répertoire de ton projet, tu crées un module python **myapp** qui contient
un fichier vide **__init__.py** et le fichier **wsgi.py** suivant:

.. code-block:: python

    from bottle import route, template, default_app

    @route('/hello/<name>')
    def index(name):
        return template('<b>Hello {{name}}</b>!', name=name)

    application = default_app()

Pour information, sous django, le fichier à utiliser s'appelle aussi **wsgi.py**.

Et tu vas utiliser chaussette pour lancer ton application web.

Chaussette est un serveur wsgi qui permet le dialogue entre les requêtes http
et ton application python. Il permet d'utiliser différents backends wsgi, comme
waitress par exemple et a également la particularité de pouvoir servir ton
application sur un socket déjà ouvert. Dis comme ça, ça n'a l'air de rien, mais
ça permet du coup d'utiliser un manager de socket comme circus ou supervisor.

Tu installes bottle, chaussette et waitress en étant **dans** le virtualenv:

.. code-block:: bash

    pip install bottle chaussette waitress

Et tu lances ton serveur wsgi depuis le répertoire de ton projet:

.. code-block:: bash

    chaussette --backend waitress myapp.wsgi.application

Va sur **http://127.0.0.1:8080/hello/you**, tu devrais voir ta page apparaître.

Place au spectacle!

Circus est un grosso-modo un manager de processus et de socket. C'est lui qui va
se charger de monitorer eet de redémarrer tes applications. Il est compatible
python 2 et python 3, il permet d'utiliser les virtualenvs et se marie très bien
avec chaussette. Ce projet nous vient à l'origine de la fondation mozilla.

Tu l'installes via pip **en dehors** du virtualenv (donc en global sur ton système):

.. code-block:: bash

    apt-get install libzmq-dev libevent-dev python-dev python-virtualenv
    sudo pip install circus circus-web

Et tu créees le fichier de configuration de circus qui va te permettre de lancer
ton serveur chaussette:

Dans un fichier **circus.ini** dans ton *home*,  tu mets:

.. code-block:: bash

    [circus]
    statsd = 1
    httpd = 1

    [watcher:myapp]
    cmd = /home/TONUSER/.virtualenvs/myapp/bin/chaussette --fd $(circus.sockets.web) --backend waitress myapp.wsgi.application
    working_dir = /home/TONUSER/LECHEMINVERSTONPROJET
    numprocesses = 3
    copy_env = 1
    use_sockets = 1
    virtualenv = /home/TONUSER/.virtualenvs/myapp
    virtualenv_py_ver = 3.5

    [socket:web]
    host = 127.0.0.1
    port = 8001

N'oublies pas de modifier les différents pour que ça correspondent à ta machine.

Et lances le *daemon* de circus:

.. code-block:: bash

    circusd --daemon ~/circus.ini

Si tout s'est bien passé, tu devrais pouvoir utiliser les commandes de **circusctl**
pour voir le status des applications, les redémarrer, etc ... :

.. code-block:: bash

    # exemple de commandes
    circusctl status
    circusctl listsockets
    circusctl restart myapp

Si tu te rends sur **http://127.0.0.1:8001/hello/you**, tu devrais voir ton application!
Et en allant sur **http://127.0.0.1:8080/**, tu te connectes au tableau de bord de circus.

Avec circus, tu peux ainsi manager plusieurs applications différentes, qui tournent sous
des environnements virtuels différents.

Bon, il ne te reste plus qu'à mettre en place nginx. C'est un
serveur http libre et performant qui est une très bonne alternative à apache.
Il va nous permettre de rediriger les requêtes http à circus/chaussette.

Tu l'installes via **apt** par exemple:

    .. code-block:: bash

        apt-get install nginx

Et tu vas créer la configuration suivante dans **/etc/nginx/sites-available/myapp.conf**:

    .. code-block:: bash

    upstream myapp  {
        server localhost:8001;
    }
    server {
        listen 80;
        server_name localhost myapp;

        location / {
            proxy_pass      http://myapp$request_uri;
            proxy_redirect  off;
            proxy_set_header   Host             $host;
            proxy_set_header   X-Real-IP        $remote_addr;
    }

Tu actives ta conf et tu redémarre nginx:

    .. code-block:: bash

        ln -S /etc/nginx/sites-available/myapp.conf /etc/nginx/sites-enabled/myapp.conf
        service nginx restart #ou via systemd selon ta distro

Il ne te reste plus qu'à te rendre sur http://localhost/hello/you pour observer le résultat !
