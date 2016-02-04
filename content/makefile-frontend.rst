Se passer de Grunt/Gulp/Brunch/Broccoli/Mimosa/Jake grâce à Make
================================================================

:date: 2016-01-12
:tags: frontend,make,makefile,javascript,livescript,less,css,compile,node.js
:category: Frontend
:slug: makefile-frontend
:authors: Morgan
:summary: Se passer de Grunt/Gulp/Brunch/Broccoli/Mimosa/Jake grâce à Make

.. image:: ./images/gnu.png
    :alt: Gnu
    :align: right

La communauté `Node.js <https://nodejs.org>`_ a été plutôt productive ces deux
dernières années, notamment au niveau de la création de *tasks runners*.

Certains sont enthousiastes de cet essor et de cette profusion d'outils,
mais d'autres le sont beaucoup moins `et le font savoir <https://medium.com/@wob/the-sad-state-of-web-development-1603a861d29f#.nrikd9bai>`_.

Tu as forcément déjà lu un article ou vu un bout de code qui mentionnait au choix `grunt <http://gruntjs.com/>`_,
`gulp <http://gulpjs.com/>`_, `brunch <http://brunch.io/>`_, `broccoli <http://broccolijs.com/>`_,
`mimosa <http://mimosa.io/>`_, `jake <http://jakejs.com/>`_ ou que sais-je.

Mais lequel utiliser ? Pourquoi y en a-t-il autant ? Quel est le plus simple ? Le plus performant ? Le plus suivi ?
Quel tuto suivre ?

Franchement, devoir ré-apprendre un *tasks runners* tous les trois mois en fonction de la mode,
c'est plutôt lourd. Et ça rappelle fortement le choix cornélien du framework ou de la librairie javascript (
`angular <https://angularjs.org/>`_, `angular2 <https://angular.io/>`_, `react <https://facebook.github.io/react/>`_,
`polymer <https://www.polymer-project.org/1.0/>`_, `jquery <https://jquery.com/>`_, `vue.js <http://vuejs.org/>`_, etc...)

N'y a-t-il pas un outil robuste, simple et pérenne ? Et qui pourrait te servir pour autre chose que du
développement frontend tant qu'à faire ? Et ben si, ça existe depuis la création de `GNU <https://www.gnu.org>`_ en 1983 par Richard
Stallman, et ça s'appelle `Make <https://www.gnu.org/software/make/>`_.

*Make* est un outil qui permet d'automatiser la construction de fichiers et qui peut
jouer le rôle de *tasks runners*.

Concrètement, en développement web, de quoi est-ce qu'on a le plus besoin ?

* Compiler nos fichiers `LESS <http://lesscss.org/>`_ ou `Sass <http://sass-lang.com/>`_ en CSS.
* Minifier nos fichiers CSS.
* Compiler nos fichiers `LiveScript <http://livescript.net/>`_, `CoffeeScript <http://coffeescript.org/>`_ ou `TypeScript <http://www.typescriptlang.org/>`_ en JavaScript.
* Minifier nos fichiers JavaScript.
* Avoir un *watcher* qui lance automatiquement toutes ces tâches lorsqu'un fichier source est modifié.

On suppose que tu as :

* tes fichiers LESS dans **static/src/less**
* tes fichiers LiveScript dans **static/src/ls**

Et que tu veux tes fichiers compilés et minifiés dans **static/dist/css** et **static/dist/js**.

C'est parti, tu vas te créer un fichier **Makefile** qui fera tous ça !

.. code-block:: bash

    vim Makefile

Tu y déclares tes répertoires de travail :

.. code-block:: bash

    LESS_FOLDER := static/src/less
    LS_FOLDER := static/src/ls
    CSS_FOLDER := static/dist/css
    JS_FOLDER := static/dist/js

Ensuite, tu y listes les fichiers concernés :

.. code-block:: bash

    LESS_FILES := ${shell find ${LESS_FOLDER} -type f -name '*.less'}
    LS_FILES := ${shell find ${LS_FOLDER} -type f -name '*.ls'}
    CSS_FILE := ${CSS_FOLDER}/main.min.css
    JS_FILE := ${JS_FOLDER}/main.min.js

La commande **find** utilisée pour *LESS_FILES* et *LS_FILES* permet de récupérer le
chemin de tous les fichiers LESS et LiveScript présents.

Tu déclares une tâche *build* qui sera chargée de lancer la compilation des fichiers :

.. code-block:: bash

    build: build-css build-js

Puis, tu commences par créer la tâche qui va compiler les fichiers LESS :

.. code-block:: bash

    build-css: ${CSS_FOLDER} ${CSS_FILE}

    ${CSS_FILE}: ${LESS_FILES}
    	cat $^ | lessc - | cleancss > $@

    ${CSS_FOLDER}:
    	mkdir -p $@

Ta tâche *build-css* va créer le répertoire **static/dist/css** via **mkdir**.
Et elle va compiler tous les fichiers LESS à l'aide de **lessc** et les minifier à
l'aide de **cleancss**.

Dans une **Makefile**, *$^* correspond à la liste des dépendances. Il s'agit ici
des fichiers contenus dans *LESS_FILES*. *$@* correspond au nom de la cible, à
savoir le fichier contenu dans *CSS_FILE*.

De la même manière, tu crées la tâche qui va compiler les fichiers LiveScript :

.. code-block:: bash

    build-js: ${JS_FOLDER} ${JS_FILE}

    ${JS_FILE}: ${LS_FILES}
    cat $^ | lsc -sc | uglifyjs - > $@

    ${JS_FOLDER}:
    mkdir -p $@

Les fichiers LiveScript sont compilés à l'aide de **lsc** et minifiés à l'aide
de **uglifyjs**.

Tu rajoutes une méthode pour nettoyer le répertoire *dist* :

.. code-block:: bash

    clean:
    	rm ${CSS_FILE} ${JS_FILE}

Et une méthode qui te permettra d'installer les librairies utilisées par ton **Makefile** via **npm** :

.. code-block:: bash

    install-dependencies:
    	sudo npm install -g less clean-css livescript uglifyjs onchange

Enfin, tu vas mettre en place ton *watcher* à l'aide de **onchange** :

.. code-block:: bash

    watch:
    	onchange "${LESS_FILES}" "${LS_FILES}" -- make build

La dernière instruction servira à dire à **make** que certaines tâches
ne sont pas directement liées à des noms de fichiers :

.. code-block:: bash

    .PHONY: build build-css build-js clean watch install-dependencies

Et c'est fini! Tu disposes désormais des commandes suivantes :

* **make install-dependencies** : pour installer les dépendances.
* **make** ou **make build** : pour compiler et minifier tous les fichiers.
* **make build-js** : pour compiler et minifier les fichiers LiveScript.
* **make build-css** : pour compiler et minifier les fichiers LESS.
* **make clean** : pour effacer les fichiers compilés et minifiés.
* **make watch** : pour relancer automatiquement la commande **make build** à chaque modifications de fichiers.

Le résultat final :

.. code-block:: bash

    #################################################
    # Compile and minify less and livescript files. #
    # Require node.js and npm                       #
    #################################################

    LESS_FOLDER := static/src/less
    LS_FOLDER := static/src/ls
    CSS_FOLDER := static/dist/css
    JS_FOLDER := static/dist/js

    LESS_FILES := ${shell find ${LESS_FOLDER} -type f -name '*.less'}
    LS_FILES := ${shell find ${LS_FOLDER} -type f -name '*.ls'}
    CSS_FILE := ${CSS_FOLDER}/main.min.css
    JS_FILE := ${JS_FOLDER}/main.min.js

    ###############
    # Build files #
    ###############

    build: build-css build-js

    ####################
    # Build css files #
    ####################

    build-css: ${CSS_FOLDER} ${CSS_FILE}

    ${CSS_FILE}: ${LESS_FILES}
    	cat $^ | lessc - | cleancss > $@

    ${CSS_FOLDER}:
    	mkdir -p $@

    ##################
    # Build js files #
    ##################

    build-js: ${JS_FOLDER} ${JS_FILE}

    ${JS_FILE}: ${LS_FILES}
    	cat $^ | lsc -sc | uglifyjs - > $@

    ${JS_FOLDER}:
    	mkdir -p $@

    ###############
    # Clean files #
    ###############

    clean:
    	rm ${CSS_FILE} ${JS_FILE}

    ########################
    # Install dépendencies #
    ########################

    install-dependencies:
    	sudo npm install -g less clean-css livescript uglifyjs onchange

    ###############
    # Watch files #
    ###############

    watch:
    	onchange "${LESS_FILES}" "${LS_FILES}" -- make build

    #########
    # Phony #
    #########

    .PHONY: build build-css build-js clean watch install-dependencies

Evidemment, ça reste un exemple très simple. Mais rien ne t'empêche de faire
évoluer ton **Makefile** selon tes besoins.

En plus, tu viens d'apprendre un outil qui te sera utile pour faire de l'administration système.

Bonne compilation !
