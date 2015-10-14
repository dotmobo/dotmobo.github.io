Passer de Sublime Text à Atom pour développer en Python
#######################################################

:date: 2015-10-18
:tags: sublime text,python,atom,éditeur,github,code
:category: Python
:slug: sublime-text-to-atom
:authors: Morgan
:summary: Passer de Sublime Text à Atom pour développer en Python

.. image:: https://avatars0.githubusercontent.com/u/1089146?v=3&s=200
    :alt: Pelican
    :align: right

| *"Sublime Text, c'est vraiment pas mal mais bon, c'est pas libre."*
| *"Eclipse, c'est vraiment trop lourd pour faire du Python."*
| *"Vim, ça va deux minutes, mais pour les très gros projets c'est contraignant."*
| *"Emacs j'y comprends rien."*
| *"Pycharm, ce n'est qu'à moitié libre."*
| *"Atom, y paraît que c'est buggé et lent."*
|

Bon, je vois que tu es un difficile concernant le choix de ton éditeur de code,
et tu as bien raison ! Je t'arrêtes tout de suite en ce qui concerne
`Atom <https://atom.io/>`_. Pour les autres, je ne vais pas rentrer dans le
troll!

*"C'était"* buggé et lent, mais ça ne l'est plus depuis la sortie de la version
stable 1.0 sortie cet été. La version actuelle (1.0.19) marche plutôt bien et
est enfin devenue une alternative viable à
`Sublime Text <http://www.sublimetext.com/>`_.

Comme ST, tu vas pouvoir bénificier:

* des curseurs multiples.
* de la palette de commandes via *ctrl+shift+p*.
* de la recherche de fichiers via *ctrl+p*.
* d'une intégration Git très poussée.
* d'une vue permettant de parcourir tes fichiers.
* d'onglets, de panels.
* de la coloration syntaxique, de la complétion.
* d'une tonnes de plugins.

Il n'y a évidemment pas encore autant de plugins que pour ST, mais ça
vient comme tu peux le voir `ici <https://atom.io/packages>`_.

Convaincu ? Prêt pour l'installation ? C'est parti.

Installe-le tout d'abord via les paquets proposés sur le
`site officiel <https://atom.io/>`_.

Avant de l'exécuter, on va installer une série de plugins qui va te permettre
de développer dans de bonnes conditions. Ces plugins vont être:

* `minimap <https://github.com/atom-minimap/minimap>`_, qui est un
  aperçu du code sous forme de minimap à la manière de ST.
* `autocomplete-paths <https://github.com/atom-community/autocomplete-paths>`_,
  qui permet d'activer la complétion des chemins des dossiers et fichiers de ton
  système.
* `autocomplete-python <https://github.com/sadovnychyi/autocomplete-python>`_,
  qui est le plugin le plus fiable pour la complétion Python, basé sur
  `jedi <http://jedi.jedidjah.ch/en/latest/>`_. Pour activer la complétion des
  librairies présentes dans ton virtualenv, il suffit de lancer atom depuis ton
  virtualenv.
* `linter <https://github.com/atom-community/linter>`_, qui permet de visualiser
  les erreurs de syntaxe `de nombreux langages <http://atomlinter.github.io/>`_.
* `linter-pep8 <https://github.com/AtomLinter/linter-pep8>`_ comme linter python.
  On aurait pu en utiliser un autre, comme
  `linter-pylint <https://github.com/AtomLinter/linter-pylint>`_, mais je
  le trouve trop verbeux.
* `emmet <https://github.com/emmetio/emmet-atom>`_ pour le développement HTML et
  CSS.
* `git-plus <https://github.com/akonwi/git-plus>`_, qui permet d'utiliser toutes
  les commandes git depuis Atom.
* `merge-conflicts <https://github.com/smashwilson/merge-conflicts>`_, qui est un
  bon helper lors des *git merge*.
* `travis-ci-status <https://github.com/tombell/travis-ci-status>`_, pour
  afficher le status de `travis <https://travis-ci.org/>`_ dans la barre de
  status d'Atom.
* `monokai <https://github.com/kevinsawicki/monokai>`_, pour obtenir un thème
  proche de ST.
* `pigments <https://github.com/abe33/atom-pigments>`_, pour afficher les
  couleurs dans les CSS, LESS et autres.
* `color-picker <https://github.com/thomaslindstrom/color-picker>`_, pour choisir
  une couleur HTML via *ctrl+shift+c*.
* `highlight-selected <https://github.com/richrace/highlight-selected>`_, qui,
  lors du double-clique sur un mot, met en surbrillance tous les mots
  correspondants, comme ST.
* `atom-beautify <https://github.com/Glavin001/atom-beautify>`_, permet
  d'indenter automatiquement le code de nombreux langages pour améliorer la
  lisibilité.
* `language-restructuredtext <https://github.com/Lukasa/language-restructuredtext>`_,
  qui active la coloration syntaxique des fichiers *.rst*.

Il en existe d'autres qui pourrait t'intéresser, comme
`vim-mode <https://github.com/atom/vim-mode>`_,
`terminal-plus <https://github.com/jeremyramin/terminal-plus>`_, ou encore
`project-manager <https://github.com/danielbrodin/atom-project-manager>`_, à toi
de faire ton marché!

Atom propose un outil en ligne de
commande, **apm**, qui permet d'installer des plugins sans passer par le menu
*Settings* d'Atom. On installe donc les plugins:

.. code-block:: bash

    apm install minimap
    apm install autocomplete-paths
    pip install jedi
    apm install autocomplete-python
    apm install linter
    pip install pep8
    apm install linter-pep8
    apm install emmet
    apm install git-plus
    apm install merge-conflicts
    apm install travis-ci-status
    apm install monokai
    apm install pigments
    apm install color-picker
    apm install highlight-selected
    apm install atom-beautify
    apm install language-restructuredtext


Tu peux maintenant lancer Atom via la commande:

.. code-block:: bash

    atom

On commence par définir la tabulation comme étant 4 espaces pour être compatible
`pep8 <https://www.python.org/dev/peps/pep-0008/>`_ dans
*Edit->Preferences->Settings*: ::

    Tab Length
    4

Puis on active le thème Monokai installé précédemment via
*Edit->Preferences->Theme*: ::

    Syntax Theme
    Monokai

Et c'est fini! Tout est prêt pour commencer le développement de tes applications
Python et Django.

Tu peux alors créer tes propres
`snippets <https://atom.io/docs/latest/using-atom-snippets>`_ en éditer le
fichier *snippets.cson* du répertoire *~/.atom* de cette manière par exemple:

.. code-block:: javascript

    '.source.js':
      'console.log':
        'prefix': 'log'
        'body': 'console.log(${1:"crash"});$2'

Utilise *alt+shift+s* pour rechercher tes snippets.

Enfin tu vas également pouvoir sauvegarder ta configuration sur Github de `cette
manière <https://github.com/dotmobo/dotatom>`_ par exemple.
