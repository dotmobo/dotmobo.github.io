Nix : Package manager et gestionnaire de configuration
######################################################

:date: 2024-10-12
:tags: nix, nixos, linux, distro, package, manager, devops, sysadmin
:category: Linux
:slug: nix
:authors: Morgan
:summary: Nix : Package manager et gestionnaire de configuration

.. image:: ./images/nix.png
    :alt: Nix
    :align: right



Bon, c'est parti pour un article pas du tout prévu, mais c'est tellement un banger que je me dois d'en parler.

Je viens de découvrir le package manager `Nix <https://nixos.org/>`_, et quelle claque !

À une époque, j'avais jeté un œil à `GNU Guix <https://guix.gnu.org>`_ et à son langage `Guile <https://gnu.org/software/guile/>`_, qui semblaient intéressants.
Mais j'ai laissé tomber car la doc était imbuvable et ça ne semblait pas encore au point.

Puis j'ai appris récemment que Guix venait en fait de Nix et que, pour le coup, Nix était à nouveau en vogue à cause de NixOS.
Un collègue m'a poussé à creuser et je n'ai pas été déçu.

Pour faire simple, Nix est un gestionnaire de paquets qui peut s'installer sur n'importe quelle distro et permet d'installer des paquets récents indépendamment de la distro.
Tu peux donc rester sur Debian stable et utiliser la dernière version de Neovim grâce à Nix, par exemple.

Tout est géré dans un répertoire indépendant, **/nix**, et son fonctionnement peut faire penser à Git dans le sens où tout est versionné.
Tu peux donc faire des rollbacks si l'installation d'un paquet s'est mal passée.

Nix
====

Pour commencer, tu peux installer Nix sur ta machine avec la commande suivante :

.. code-block:: bash

    sh <(curl -L https://nixos.org/nix/install) --daemon
    nix --version
    

On va y aller étape par étape en prenant des cas d'usage intéressants en allant du plus simple au plus compliqué.

Pour tester que tout marche bien, on va commencer par utiliser un environnement shell de nix pour installer
et utiliser des paquets.

.. code-block:: bash

    nix-shell -p cowsay lolcat

Après avoir exécuter cette commande, tu te retrouves dans un shell avec cowsay et lolcat d'installés.
Tu peux les tester via :

.. code-block:: bash

    [nix-shell:~]$ cowsay Hello, Nix! | lolcat

Tu devrais voir un joli *Hello, Nix!* en couleur. Une fois que tu quittes le shell, les paquets sont désinstallés.
On est ici dans un cas d'environnement shell temporaire.

Il y a énormément de paquets disponibles, tu peux les chercher via le lien `https://search.nixos.org/ <https://search.nixos.org/>`_.

Script
======

Place aux cas d'usage.

Premier cas : tu veux balancer un script en prod, mais tu n'as pas les droits d'installer des paquets car tu n'es pas root.
Ce genre de cas arrive très souvent en entreprise, surtout lorsque l'on est dev et pas admin sys ou devops.

Avec Nix, il y a moyen d'installer temporairement des paquets juste le temps d'exécution du script, de cette manière, dans un fichier type **monscript.sh** :

.. code-block:: bash

    #!/usr/bin/env nix-shell
    #! nix-shell -i bash --pure
    #! nix-shell -p bash cacert curl jq python3Packages.xmljson
    #! nix-shell -I nixpkgs=https://github.com/NixOS/nixpkgs/archive/2a601aafdc5605a5133a2ca506a34a3a73377247.tar.gz

    curl https://github.com/NixOS/nixpkgs/releases.atom | xml2json | jq .

Tu vas utiliser ici les shebangs pour préciser les paquets nécessaires à l'exécution du script et tu
pointes vers une version précise de Nix pour être sûr de pouvoir reproduire le script à l'identique, peut
importe la machine sur laquelle tu l'installes.

Et voilà, la magie va opérer. Tu vas pouvoir bénéficier de **curl**, **xml2json** et **jq**.

Une fois le script exécuté, les paquets installés et nix seront supprimés.

C'est beaucoup plus simple que de gérer des Dockerfile !

Devenv
======

En parlant de Docker, tu peux utiliser la librairie `Devenv <https://devenv.sh/>`_ pour gérer des environnements de dev avec Nix directement, en te passant de Docker Compose !

Pour l'installer, rien de plus simple.

.. code-block:: bash

    nix-env -iA devenv -f https://github.com/NixOS/nixpkgs/tarball/nixpkgs-unstable

Voici un cas simple pour un environnement Angular dans un fichier **devenv.nix** :

.. code-block:: nix

    { pkgs, lib, config, inputs, ... }:

    {
    # https://devenv.sh/basics/
    env.GREET = "devenv";

    # https://devenv.sh/packages/
    packages = [
        pkgs.git
        pkgs.nodejs_20
    ];

    # https://devenv.sh/languages/
    # languages.rust.enable = true;

    # https://devenv.sh/processes/
    processes.angular.exec = "npm run start";

    # https://devenv.sh/services/
    # services.postgres.enable = true;

    # https://devenv.sh/scripts/
    scripts.install-angular-cli.exec = ''
        mkdir -p ~/.npm-global
        npm config set prefix '~/.npm-global'
        export PATH=~/.npm-global/bin:$PATH
        if ! npm list -g @angular/cli | grep @angular/cli@17; then
        npm install -g @angular/cli@17
        fi
    '';
    scripts.build-api.exec = ''
        ./gradlew assemble
    '';
    scripts.install-app.exec = ''
        npm install
    '';

    enterShell = ''
        install-angular-cli
        build-api
        install-app
    '';

    # https://devenv.sh/tests/
    enterTest = ''
        echo "Running tests"
        git --version | grep --color=auto "${pkgs.git.version}"
        node --version | grep --color=auto "${pkgs.nodejs_20.version}"
        ng version | grep "17"
        ./gradlew --version | grep "Gradle 7.4.2"
    '';

    # https://devenv.sh/pre-commit-hooks/
    # pre-commit.hooks.shellcheck.enable = true;

    # See full reference at https://devenv.sh/reference/options/
    }

Tu peux ici gérer ta version de node, de npm et de angular et lancer des commandes d'installation et de build
à l'entrée dans le shell, comme des **npm install** ou des **./gradlew assemble**.

Il y a même une petite partie permettant de faire des tests pour être sûr que tout est bien configuré.

Tu peux ensuite lancer ton environnement avec la commande :

.. code-block:: bash

    devenv up

Il va alors tout installer, tout builder et lancer automatiquement la commande **npm run start**.

Tu peux aussi faire un **devenv shell** pour entrer directement dans l'environnement shell.

Mais il est également possible de gérer tes services de base de données et autres, comme pour Docker Compose !
Sauf que tu n'es pas dans un container, mais dans un sous-shell directement.
Tu peux voir la partie **services** qui est commenté dans mon fichier.

Attention, ça signifie que ce sont donc bien les fichiers de ton système que tu manipules lorsque tu lances des commandes.

Home Manager
============

Alors là, c'est mon préféré, la cerise sur le gâteau.

Tu vas pouvoir gérer tout ton home et en faire une description précise dans un fichier Nix pour le rendre reproductible.

Tu peux installer des paquets et gérer tes dotfiles au même endroit !

Je m'en sers `ici <https://github.com/dotmobo/home-manager>`_ pour installer mon terminal, VS Code, Neovim et toute la configuration qui va avec.

Commence par installer home-manager :

.. code-block:: bash

    nix-channel --add https://github.com/nix-community/home-manager/archive/master.tar.gz home-manager
    nix-channel --update
    nix-shell '<home-manager>' -A install
    . "$HOME/.nix-profile/etc/profile.d/hm-session-vars.sh"

Puis tu créés un fichier **~/.config/home-manager/home.nix** pour y décrire toute ta configuration :

.. code-block:: nix

    { config, pkgs, ... }:

    let
      secrets =
        if builtins.pathExists "/home/morgan/.config/home-manager/secrets.nix"
        then import /home/morgan/.config/home-manager/secrets.nix
        else { };  
    in
    {
      nixpkgs = {
        config = {  
          allowUnfree = true;
          allowUnfreePredicate = (_: true);
        };
      };

      programs.home-manager.enable = true;

      home.username = "morgan";
      home.homeDirectory = "/home/morgan";

      home.stateVersion = "24.05";

      home.packages = with pkgs; [
        devenv
        # Fonts
        fira-code
        fira-code-symbols
        (nerdfonts.override { fonts = [ "FiraCode" ]; })
        # Terminal
        guake
        tdrop
        wmctrl
        st
        atuin
        starship
        # Programming languages
        nodejs_20
        go
        python312
        pipx
        poetry
        ruff
        black
        pyright
        rustc
        rustfmt
        cargo
        rust-analyzer
        clippy
        zig
        lua
        # Tools
        httpie
        wget
        jq
        curl
        ffmpeg
        htop
        xclip
        bats
        ripgrep
        tmux
        eza
        bat
        fd
        tree
        peek
        rsync
        gh
        zip
        unzip
        unrar
        transmission
        # Network
        traceroute
        tcpdump
      ];

      home.file = { };

      home.sessionVariables = {
        # User configuration
        EDITOR = "nvim";
        LANG = "fr_FR.UTF-8";
        # Chrome
        CHROME_BIN = "/usr/bin/chromium";
        CHROME_EXECUTABLE = "/usr/bin/chromium";
        # Node.js
        NODE_OPTIONS = "--max-old-space-size=4096";
        # Rust
        RUST_SRC_PATH = "${pkgs.rust.packages.stable.rustPlatform.rustLibSrc}";
        # Jenkins
        JENKINS_URL = "${secrets.JENKINS_URL}";
        JENKINS_USER_ID = "${secrets.JENKINS_USER_ID}";
        JENKINS_API_TOKEN = "${secrets.JENKINS_API_TOKEN}";
      };

      home.sessionPath = [ 
        "$HOME/.local/bin" 
      ];

      programs = {
        git = (import ./git.nix { inherit pkgs; });
        neovim = (import ./neovim.nix { inherit pkgs; });
        fish = (import ./fish.nix { inherit pkgs; });
        vscode = (import ./vscode.nix { inherit pkgs; });
        zoxide = {
          enable = true;
          enableFishIntegration= true;
          options = [
            "--cmd cd"
          ];
        };
        zellij = {
          enable = true;
          settings = {
            copy_command = "xclip -selection clipboard";
              paste_command = "xclip -selection clipboard -o";
            };
          };
      };

      fonts.fontconfig.enable = true;

    }

Ici j'utilise nix pour installer mes paquets via **home.packages**, gérer mes variables d'environnement via **home.sessionVariables** et mes dotfiles via **programs**.
Tu peux noter que j'utiliser une fichier **/home/morgan/.config/home-manager/secrets.nix** pour y mettre mes mots de passe et autres secrets.

Pour les programmes qui nécessitent une configuration spécifique, j'utilise des fichiers **.nix** que j'importe dans mon fichier principal :

- `git.nix <https://github.com/dotmobo/home-manager/blob/master/git.nix>`_ pour gérer ton username, ton mail ou tes alias.
- `neovim.nix <https://github.com/dotmobo/home-manager/blob/master/neovim.nix>`_ pour gérer tes plugins et ta configuration.
- `fish.nix <https://github.com/dotmobo/home-manager/blob/master/fish.nix>`_ qui est mon shell par défaut.
- `vscode.nix <https://github.com/dotmobo/home-manager/blob/master/vscode.nix>`_ pour gérer tes extensions et ta configuration.

Tu peux ensuite appliquer ta configuration avec la commande :

.. code-block:: bash

    home-manager switch

Et voilà, tu as tout ton home configuré à ta sauce, et tu peux le reproduire à l'identique sur n'importe quelle machine.

Note qu'il y a pas mal de nouveaux outils écrit en Rust que j'utilise. Ça pourra faire de futurs petits articles dessus si ça t'intéresse !

NixGL
=====

On utilise principalement le home-manager pour gérer son terminal. Mais il est également possible de l'utiliser pour des applications qui
utilise openGL. Par défaut, sans utiliser NixOS mais Debian par exemple, les applications openGL ne fonctionnent pas directement avec Nix.

Il existe alors un petit wrapper openGL appelé `NixGL <https://github.com/nix-community/nixGL>`_ qui permet de faire fonctionner les applications
comme **alacritty** par exemple.

Tu l'installes via :

.. code-block:: bash

    nix-channel --add https://github.com/nix-community/nixGL/archive/main.tar.gz nixgl && nix-channel --update
    nix-env -iA nixgl.auto.nixGLDefault

Tu utilises alors ce wrapper pour exécuter alacritty si tu l'as installé via home-manager :

.. code-block:: bash

    nixGL alacritty

C'est un petit point gênant qui me donne envie de réellement migrer sur NixOS.

NixOS
=====

Pour finir, la dernière étape serait de virer ma Debian et de migrer intégralement sur NixOS, la distro intégralement gérée par Nix.
Pour le moment, j'ai encore certains besoins de Debian à cause de mon taf, mais dès que possible, je migrerai sûrement dessus.

Jette un œil sur la partie **NixOS : the Linux distribution** du `site officiel <https://nixos.org/download/>`_.

Tu peux alors avoir l'intégralité de ton système géré par un fichier de configuration Nix, que ça soit pour les paquets, les services,
la configuration réseau ou les utilisateurs.

Voilà, j'espère t'avoir donné envie de découvrir Nix ! Il y a beaucoup de choses, et le piège est de ne pas savoir par quel bout commencer ! 
Je te conseille vraiment de faire comme moi, étape par étape, petit à petit.

Un fois pris au jeu, tu verras, tu ne pourras plus t'en passer !

