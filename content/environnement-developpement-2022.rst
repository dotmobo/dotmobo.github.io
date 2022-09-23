Environnement de développement en 2022
######################################

:date: 2022-09-19
:tags: debian,environnement,developpement,gnome,flatpak,fish,copilot,neovim
:category: Linux
:slug: environnement-developpement-2022
:authors: Morgan
:summary: Environnement de développement 2022

Mon dernier article concernant mon environnement de développement datant de 2016, il était temps de faire une petite
mise à jour de ce qui a changé depuis.

.. image:: ./images/debian.png
    :alt: Debian
    :align: right

Distribution
============

Au revoir Arch Linux, et bonjour `Debian Sid <https://www.debian.org/>`_. J'adore toujours Arch Linux mais je n'ai plus autant de temps qu'avant pour
bidouiller et customiser mon système. Il me faut un système stable et robuste, sans surprise, mais qui soit relativement
à jour par rapport aux derniers paquets disponibles. Et clé en main.

Ça va faire 3 ans que je suis sur Debian Sid et je n'ai jamais eu de problème. C'est un bon compromis entre stabilité et
fraicheur. Debian est devenu suffisamment user-friendly pour rendre obsolète toutes les distros basées sur elle comme Ubuntu
ou Mint.

Tout ce qui me dérange un peu, c'est la migration vers Systemd, car je ne suis personnellement pas fan du principe.
Je préfère les outils qui suivent plus la philosophie Unix, c'est-à-dire qui font une seule chose et le font bien.
Mais bon, toutes les grosses distros ont désormais migré dessus, et à l'avenir il faudra peut-être plutôt regarder du
côté de BSD pour avoir des outils plus simples.

Bureau
======

`Gnome <https://www.gnome.org/>`_. Principalement parce que je suis passé d'un PC fixe à un portable avec un dock. Ce qui fait que j'ai beaucoup
de périphériques à gérer et que je me connecte/déconnecte régulièrement à différents docks et écrans. Et Gnome gère
automatiquement tout ça pour moi. Ok, y a plein de daemons qui tournent mais bon... C'est clairement du confort.

Je regarde toujours les tiling window managers de temps en temps comme i3, et j'ai donc testé Pop Shell qui permet du tiling avec Gnome.
C'est pas trop mal mais finalement, sur un portable, je préfére utiliser Gnome avec le terminal top-down `Guake <http://guake-project.org/>`_.


Shell
=====

J'ai migré de zsh à `fish <https://fishshell.com/>`_ après m'être rendu compte que ma configuration customisée de zsh correspondait exactement
au réglage par défaut de fish. Donc fish vanilla couplé à `tmux <https://github.com/tmux/tmux>`_ pour la gestion des onglets et des sessions.
Rien à configurer, juste ça marche par défaut. Magique.


Theme
=====

Concernant les thèmes, je suis passé sur `Dracula <https://draculatheme.com/>`_ pour absolument tout. C'est un thème sombre parfait qui est disponible
pour gnome, fish, vim, tmux, vs code, etc. L'ensemble de mon environnement est donc cohérent et j'aime beaucoup le résultat.

Police
======

J'utile désormais la police `Fira Code <https://github.com/tonsky/FiraCode>`_ depuis que je l'ai découverte. C'est une police monospace avec des ligatures,
parfaite pour le développement.

Editeur de code
===============

`Visual Code Studio <https://code.visualstudio.com/>`_ et `Neovim <https://neovim.io/>`_.

VS Code a clairement remporté la bataille des éditeurs de texte face à Atom et Sublime Text.
C'est un éditeur de code moderne, performant, avec un grand nombre de plugins. Et il est open source.
Rien à redire de ce côté là, bravo Microsoft pour une fois.

Neovim prend bien la relève de Vim et c'est plutôt agréable de pouvoir utiliser Lua pour gérer les plugins.

Completion
==========

J'ai participé à la beta de `Github Copilot <https://github.com/features/copilot>`_ et j'y suis resté depuis. Un outil vraiment bluffant, et qui continue de me
bluffer tous les jours. Je vois beaucoup de réticents mais vraiment... essayez-le, au moins pour votre culture.
Pour des développements type Java avec une tonne de boilerplate à écrire, c'est juste génial.


Gestion des applications
========================

Récemment j'ai découvert `Flatpak <https://flatpak.org/>`_ et je suis plutôt fan du principe. J'avais testé Snap de Ubuntu à l'époque mais ça ne m'avait pas
convaincu. Flatpak est plutôt rapide et simple à utiliser. C'est un peu plus sécurisé et ça permet de gérer les dépendances de manière plus propre.
Le principe d'isolation me fait un peu penser aux installations des applications sur Android.

Du coup, désormais, dès que je dois installer une application externe propriétaire commme Spotify, Discord, Telegram ou Google Chrome,
je passe par Flatpak.

En vrai, je me dis que Flatpak me permettrait même de rester sur Debian Stable plutôt que Sid et d'avoir des outils à jour grâce
à lui. Mais bon, il y a encore quelques soucis de compatibilité avec certaines applications comme VS Code ou Steam par exemple.

Bonne découverte !


