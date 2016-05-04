Environnement de développement open source
##########################################

:date: 2016-04-19
:tags: arch,linux,i3,atom,vim,docker,tmux,zsh,git
:category: Linux
:slug: environnement-developpement
:authors: Morgan
:summary: Environnement de développement open source

| Envie de faire évoluer ton environnement de développement ?
| D'utiliser une solution simple, pratique et efficace ?
| Alors, tu es au bon endroit !
|

On va faire le tour des outils indispensables pour mettre ça en place.
Bien évidemment, mon avis est subjectif et ce n'est qu'une solution parmis tant
d'autres.

C'est parti !

1) La distro
------------

.. image:: ./images/arch.png
    :alt: arch linux
    :align: right

On commence par le choix de la distribution. Je te conseille vivement de partir
sur `arch linux <https://www.archlinux.org/>`_ pour les raisons suivantes:

* `rolling-release <https://fr.wikipedia.org/wiki/Rolling_release>`_:
  ton système est tout le temps à jour et tu bénéficies des dernières
  versions des logiciels.
* légèreté: l'installation de base est minimaliste, ce qui fait que tu n'installes
  que ce dont tu as besoin.
* la communauté: le `wiki <https://wiki.archlinux.org/>`_ et le
  `forum <https://bbs.archlinux.org/>`_ de la communauté sont vraiment très bien
  foutus. Il y a même une `communauté francophone <https://archlinux.fr/>`_.
* `AUR <https://aur.archlinux.org/>`_: c'est un dépôt communautaire où l'on trouve
  absolument tout.

Les principales critiques envers arch linux concernent en général la stabilité du système.
La stabilité, c'est bien pour un serveur. Mais ce n'est pas forcément le plus important
pour le poste de travail d'un dev. Avec arch, tu pourras tester les toutes
dernières versions des logiciels et utiliser les nouvelles librairies à la mode !

Pour l'installer, je t'invites à le faire à la main en suivant
la `doc officielle <https://wiki.archlinux.fr/Installation>`_, histoire d'entrer dans le bain.
Si tu as vraiment la flemme, tu peux passer par
`architect <https://sourceforge.net/projects/architect-linux/>`_ pour te faciliter la chose.

N'oublie pas d'installer `yaourt <https://wiki.archlinux.fr/Yaourt>`_ pour bénifier du dépôt AUR.

Tu auras remarqué que les tutos de ce blog sont en général à destination
des utilisateurs ubuntu/debian. Pas de panique, il te suffira grosso-modo de
remplacer les **apt-get install** par **pacman -S** pour installer les paquets.
Pour le reste, c'est généralement du pareil au même.

2) Le shell
-----------

.. image:: ./images/zsh.gif
    :alt: zsh
    :align: right

Maintenant, tu vas t'installer un shell très pratique appelé `zsh <https://wiki.archlinux.fr/Zsh>`_,
qui permet une complétion avancée et l'utilisation d'une syntaxe plus sympa que bash pour
les scripts.

Et en plus de zsh, tu vas également t'installer `tmux <https://tmux.github.io/>`_,
qui est un multiplexeur de terminaux.
Il permet de manipuler plusieurs terminaux au sein d'une même fenêtre et
de se rattacher à une session tmux distante. C'est très pratique pour le
travail collaboratif et pour lancer des commandes sur des serveurs.

.. code-block:: bash

    pacman -S zsh tmux
    exec zsh
    chsh -s /bin/zsh

Il ne te reste plus qu'à `customiser ton .zshrc <https://github.com/dotmobo/dotzsh>`_
comme bon de semble.


3) Le gestionnaire de fenêtre
-----------------------------

.. image:: ./images/i3.png
    :alt: i3
    :align: right

Oublie les kde, gnome et autres cinammon. Ces environnements sont très bien
pour un usage classique de linux ; mais pour du dev, il vaut mieux se tourner vers
un `tiling window manager <https://en.wikipedia.org/wiki/Tiling_window_manager>`_.

Je te conseille de partir sur `i3 <https://i3wm.org/>`_, qui est facile d'accès,
customisable et efficace. Il te permettra d'utiliser l'ensemble de l'espace visible
disponible, de splitter tes fenêtres comme bon te semble et d'exécuter tes applications.
De plus, tu pourras manipuler tout ton bureau
`au clavier <http://i3wm.org/docs/userguide.html#_default_keybindings>`_,
ce qui fait un sacré gain de temps.

.. code-block:: bash

    pacman -S i3
    echo "exec i3" > ~/.xinitrc
    reboot

A côté d'i3, tu pourras installer entre autres:

* `i3-style <https://www.npmjs.com/package/i3-style>`_: pour styliser i3.
* `dmenu <https://wiki.archlinux.org/index.php/Dmenu>`_: pour avoir un lanceur d'applications.
* `i3bar et i3status <https://wiki.archlinux.org/index.php/i3#i3bar>`_:
  pour avoir une barre de status en bas de l'écran.
* `i3lock et xautolock <https://wiki.archlinux.org/index.php/i3#Screensaver_and_power_management>`_:
  pour verrouiller l'écran au bout de quelques minutes d'inactivité.
* `nitrogen <http://projects.l3ib.org/nitrogen/>`_: pour changer l'image de fond.
* pactl de `pulseaudio <https://wiki.archlinux.org/index.php/PulseAudio>`_:
  pour changer le volume au clavier.
* `dunst <http://knopwob.org/dunst/index.html>`_: pour les notifications.
* `redshift <http://jonls.dk/redshift/>`_: pour éviter de se fatiguer les yeux.
* `pcmanfm <http://wiki.lxde.org/en/PCManFM>`_: pour la gestion des fichiers.
* `firefox <https://www.mozilla.org/fr/firefox/>`_: pour la navigation web.

Jete un coup d'oeil à `ma customisation <https://github.com/dotmobo/doti3>`_
si ça t'intéresse.

Et si tu as besoin d'aide, la `communauté reddit <https://www.reddit.com/r/i3wm/>`_
est très active.

4) Je veux coder !
------------------

.. image:: ./images/vim.png
    :alt: vim
    :align: right

Pour coder, tu auras besoin d'un éditeur de texte.
Je te recommande fortement `atom <https://atom.io/>`_, que j'ai déjà présenté
`ici <http://dotmobo.github.io/sublime-text-to-atom.html>`_.

En plus d'atom, tu auras besoin d'un éditeur qui peut s'exécuter dans un terminal.
Pas besoin de chercher bien loin, le plus avancé est `vim <http://www.vim.org/>`_.
Mais tu peux également te tourner vers son successeur, `neovim <https://neovim.io/>`_.

Comme le reste des outils présentés sur cet article, il est aussi `très fortement
customisable <https://github.com/dotmobo/dotvim>`_.

En plus des éditeurs de texte, il te faudra un gestionnaire de version de code.
Sans surprise, je t'invite à installer `git <https://git-scm.com/>`_,
qui te permettra de partager ton code sous github et qui s'interface très bien
avec atom.

.. code-block:: bash

    pacman -S git vim
    yaourt -S atom

Enfin, à toi d'installer ce qui te manque:
python, node.js, postgresql, nginx, etc ...


5) Environnements isolés
------------------------

.. image:: ./images/docker.png
    :alt: docker
    :align: right

Dans le cas où tu aurais besoin de tester des applications sous d'autres
distributions, tu pourras utiliser `vagrant <https://www.vagrantup.com/>`_
pour installer des vms ou `docker <https://www.docker.com/>`_ pour utiliser des conteneurs.

.. code-block:: bash

    yaourt -S vagrant docker docker-compose

A l'aide de `docker-compose <https://docs.docker.com/compose/>`_,
tu pourras te créer un environnement spécifique par application en utilisant des conteneurs.
Par exemple, un pour elasticsearch, un autre pour mysql,
un troisième pour redis et un quatrième pour ton application django.

Tu bénificieras ainsi d'environnements complètement isolés, sans devoir installer des tonnes
d'applications directement sur ton système.

A toi de jouer maintenant, et n'hésite pas à donner tes propres astuces dans les commentaires !
