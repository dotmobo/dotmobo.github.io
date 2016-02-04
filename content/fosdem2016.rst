Retour du FOSDEM 2016
#####################

:date: 2016-02-04
:tags: fosdem,2016,python,docker,containers,pulp,guix,tox,systemd
:category: Événements
:slug: fosdem2016
:authors: Morgan
:summary: Retour du FOSDEM 2016

.. image:: ./images/fosdem.png
    :alt: FOSDEM
    :align: right

Le `FOSDEM <https://fosdem.org/>`_ est un événement qui a lieu chaque année à
`l'Université Libre de Bruxelles <http://www.ulb.ac.be/>`_.
Il permet de rencontrer d'autres développeurs, d'animer et
d'assister à des conférences, de partager des idées et des bières, et de
découvrir les nouvelles technos sympas du moment.

Cette année, c'était noir de monde ! Plus de 7900 développeurs et sysadmins étaient
présents !

Je vais te faire un bref petit retour des confs qui m'ont marqué et des technos
à suivre.


Systemd
=======
*par Lennart Poettering*

Ça y est, *systemd* est officiellement installé par défaut dans toutes les plus
grosses distros linux (sauf Gentoo).

Si tu es sous linux, tu vas obligatoirement devoir te pencher dessus.
C'est grosso-modo un *daemon* qui va te permettre de gérer tes services
(apache, postgres et autres) via la commande **systemctl**.

Je ne vais pas m'éterniser dessus, car il y a déjà pas mal d'articles sur le sujet,
comme `celui-ci <http://linuxfr.org/news/systemd-l-init-martyrise-l-init-bafoue-mais-l-init-libere>`_.


Docker for developers
=====================
*par Michael Hrivnak*

Bon, n'y allons pas par quatres chemins, `Docker <https://www.docker.com/>`_ est
clairement **LA** techno en vogue du moment. La salle était pleine à craquer, et
il y avait facilement autant de gens à l'intérieur qu'à l'extérieur. J'avais
l'impression que les organisateurs ne s'attendaient pas à ça !

C'est un outil écrit en Go et développé par Solomon Kykes, qui permet de gérer
des conteneurs LXC et d'y déployer des applications.

On a pu voir ici l'utilisation quotidienne de Docker pour un développeur, sans
évoquer les questions de déploiement.

Pour les tests unitaires
-------------------------

L'idée, c'est d'utiliser une image Docker pour chaque combinaison
d'environnement. En python, on a déjà les *virtualenvs* qui nous
permettent de tester diverses combinaisons d'interpréteurs et de librairies
python via *tox*.

Grâce à Docker, on va en plus pouvoir tester nos applications dans différents
environnements linux (debian, gentoo, etc...)

Il suffit de créer un *Dockerfile* qui va :

* utiliser la bonne distro.
* installer les paquets systèmes et les paquets python nécessaires.
* monter notre code dans */code* par exemple.
* exécuter les tests unitaires depuis le conteneur.

Pour la base de données de dev
------------------------------

En utilisant des conteneurs pour tes bases de données, tu peux facilement
tester une migration de postgres 9.4 en 9.5 par exemple, sans pourrir ton système.
Tu démarres un nouveau conteneur, tu te branches dessus et puis voilà !

Tes tests unitaires pourront également utiliser une base de données dans un
conteneur, ce qui te permettra d'éviter de manipuler du *sqlite* ou une base en
mémoire.

Pour diffuser une application de démo
-------------------------------------

Ce n'est pas forcément évident de *containeriser* une application de prod.
Il faut notamment penser à la gestion des mots de passe et des certificats.

Mais pour diffuser une application de démo, tu peux passer outre ces questions !
Tu vas ainsi éviter à tes utilisateurs d'installer toute une application sur leur
système, en leur proposant juste de démarrer un conteneur.

Pour les serveurs http
----------------------

L'idée est la même que pour les bases de données. Tu peux installer et tester
*nginx*, *apache* et *lighttpd* dans des conteneurs.

Pour faker des API
-------------------

À la place de *mocker* les réponses de tes API dans tes tests unitaires, tu
peux déployer tes API de test dans un conteneur et les utiliser directement dans
tes tests unitaires.

Guix-tox
========
*par Cyril Roelandt*

`Guix <https://www.gnu.org/software/guix/>`_ est un gestionnaire fonctionnel de
paquets pour le système GNU. On pourrait le considérer comme une alternative
à Docker pour déployer des applications.

Il fonctionne pour tous les langages. Ainsi, il permettrait d'éviter d'utiliser
des gestionnaires de paquets spécifiques aux langages, comme pip, npm, cpan.

Il utilise le langage `Guile <http://www.gnu.org/software/guile/>`_, qui est
une implémentation de `Scheme <http://schemers.org/>`_.

Dans guix, on a entre autres la possibilité d'utiliser des conteneurs, de gérer
des profils, de revenir en arrière.

Je t'invite à lire `l'article de Matutine <http://matutine.cmoi.cc/2015/11/14/installer-guix-le-gestionnaire-de-paquets-distro-venv-universel-et-container.html>`_
qui explique bien l'idée générale.

Et du coup, `guix-tox <https://git.framasoft.org/Steap/guix-tox>`_ est tout
simplement un fork de tox qui remplace les *virtualenvs* python par guix.

Tu vas ainsi pouvoir tester ton application dans un environnement système
complet, ce qui rejoint l'idée précédemment évoquée avec Docker.

Pulp
====
*par Michael Hrivnak*

`Pulp <http://www.pulpproject.org/>`_ est un projet qui permet de gérer ses propres
dépôts. On va ainsi pouvoir héberger son propre Pypi, synchroniser les dépôts
entre eux et y uploader nos paquets.

C'est compatible avec les paquets Debian, RPM, python, Docker et autres.
Franchement, ça semble plutôt bien foutu et pratique!

Pour finir, merci à toute l'équipe du FOSDEM et à l'année prochaine !
