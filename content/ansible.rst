Thématique DevOps avec Ansible
##############################

:date: 2017-09-29
:tags: python,ansible,fabric,devops,linux,déploiement,vagrant,virtualbox,ubuntu
:category: Linux
:slug: ansible
:authors: Morgan
:summary: Thématique DevOps avec Ansible

.. image:: ./images/ansible.png
    :alt: Ansible
    :align: right


`Ansible <https://www.ansible.com/>`_ est un *configuration management tool*, c'est-à-dire que c'est un outil qui va te permettre
d'administrer tes serveurs et d'y déployer automatiquement tes applications. 

**Et franchement, ça bute !** 

C'est très puissant tout en étant relativement simple à prendre en main, à l'inverse d'outils plus compliqués comme *Chef* ou *Puppet* par exemple.

En gros, ça va remplacer tes bons vieux scripts shell ou `fabfile <http://www.fabfile.org/>`_.


Installation
============

Vagrant
-------

Pour tester Ansible, tu vas utiliser `Virtualbox <https://www.virtualbox.org/>`_ avec `Vagrant <https://www.vagrantup.com/downloads.html>`_
pour te monter deux petites VMs Ubuntu Xenial.

Sous Ubuntu, tu peux installer tout ça via la commande suivante et redémarrer ta machine si besoin:

.. code-block:: bash

    sudo apt-get install virtualbox virtualbox-dkms vagrant

Dans l'idéal, essaye d'avoir une version assez récente de Vagrant. Les fichiers de conf peuvent changer selon les versions.

Ensuite, tu te crées le fichier *Vagrantfile* suivant dans *~/tuto_ansible/vagrant/Vagrantfile* par exemple:

.. code-block:: ruby

    # -*- mode: ruby -*-
    # vi: set ft=ruby :

    Vagrant.configure(2) do |config|

        config.vm.define "vm1" do | vm1 |
            vm1.vm.box = "ubuntu/xenial64"
            config.vm.network :forwarded_port, guest: 22, host: 2200, id: "ssh"
            config.vm.network :forwarded_port, guest: 80, host: 8010, id: "http"
        end
        
        config.vm.define "vm2" do | vm2 |
            vm2.vm.box = "ubuntu/xenial64"
            config.vm.network :forwarded_port, guest: 22, host: 2201, id: "ssh"
            config.vm.network :forwarded_port, guest: 80, host: 8011, id: "http"
        end

    end

Et tu démarres tes deux VMs via:

.. code-block:: bash

    cd ~/tuto_ansible/vagrant/
    vagrant up

Ansible
-------

Tu installes Ansible sous Ubuntu via :

.. code-block:: bash

    sudo apt-get install software-properties-common
    sudo apt-add-repository ppa:ansible/ansible
    sudo apt-get update
    sudo apt-get install ansible

Puis tu crées un fichier *hosts* à la racine du projet, dans *~/tuto_ansible/hosts*:

.. code-block:: bash

    [ubuntu]
    vm1 ansible_host=127.0.0.1 ansible_port=2200 ansible_user=ubuntu ansible_become=yes env=test
    vm2 ansible_host=127.0.0.1 ansible_port=2201 ansible_user=ubuntu ansible_become=yes env=prod

Et tu édites un fichier *ansible.cfg* qui va contenir ta configuration Ansible, dans *~/tuto_ansible/ansible.cfg*:

.. code-block:: bash

    [defaults]
    inventory      = hosts

Tu as désormais indiqué à Ansible d'utiliser tes deux Vms précédemment créées.

Tout est prêt !

La commande ansible
===================

Déjà, tu te places dans le répertoire *~/tuto_ansible* pour pouvoir lancer les commandes:

.. code-block:: bash

    cd ~/tuto_ansible


Ansible a besoin de python sur les machines clientes, donc si c'est pas installé par défaut: 

.. code-block:: bash

    ansible all -m raw -a "apt install -y python" --ask-sudo-pass

L'astuce ici c'est que l'option **-m raw** permet d'exécuter directement une commande ssh sans Ansible.

Et tu essayes maintenant de contacter tes deux VMs via:

.. code-block:: bash
    
    ansible all -m ping 

Si tout est ok à ce niveau-là, tu peux passer à la suite. Sinon c'est qu'il y a un souci quelque-part.

Tu vas maintenant pouvoir utiliser la commande **ansible** pour faire des trucs sur les serveurs comme:

* Exécuter une commande pour afficher la liste des utilisateurs de la première machine:

.. code-block:: bash

    ansible vm1 -m shell -a "cat /etc/passwd"

* S’assurer que *openssl* et *bash* sont à jour sur tous les serveurs ubuntu.

.. code-block:: bash

    ansible ubuntu -m apt -a "name=openssl,bash state=latest"

* Créer un utilisateur *ansible* avec un shell */bin/bash*.

.. code-block:: bash

    ansible ubuntu -m user -a "name=ansible shell=/bin/bash"

* Installer la clef publique SSH de notre utilisateur sur l’utilisateur *ansible*.

.. code-block:: bash

    ansible ubuntu -m authorized_key -a "user=ansible state=present key={{ lookup('file', '~/.ssh/id_rsa.pub') }}"

* S’assurer des bons droits sur */etc/passwd (0644)* et */etc/shadow (0400)*.

.. code-block:: bash

    ansible ubuntu -m file -a "path=/etc/passwd mode=0664"
    ansible ubuntu -m file -a "path=/etc/shadow mode=0400"

Playbooks
=========

La commande **ansible** c'est bien mais ça va un moment. Ce que tu veux, c'est avoir une recette à exécuter qui s'occupe de mettre
à jour ou non ce dont tu as besoin sur les machines distantes. Cette recette, ça s'appelle un **playbook**.

Tu vas donc écrire un **playbook** permettant de :

* installer le paquet sudo.
* créer un utilisateur ansible.
* importer une clé SSH publique pour cet utilisateur.
* configurer sudo pour cet utilisateur (sans mot de passe).
* installer Apache avec le support de PHP activé pour les distributions Ubuntu.

Tu crées le fichier *~/tuto_ansible/myplaybook1.yml* :


.. code-block:: yaml

    ---
    
    - hosts: ubuntu
      become: yes
      tasks:
      - name: "Installation de sudo sur {{ ansible_distribution }}"
        apt:
          name: sudo
          state: latest
        when: ansible_distribution == 'Ubuntu'
      - name: Ajout d'un user
        user:
          name: ansible
          shell: /bin/bash
      - name: Clé ssh
        authorized_key:
          user: ansible
          state: present
          key: "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"
      - name: Ajout du user dans les sudoers
        lineinfile:
          dest: /etc/sudoers
          state: present
          line: 'ansible ALL=(ALL) NOPASSWD: ALL'      
          validate: 'visudo -cf %s'
      - name: "Installation de apache sur {{ ansible_distribution }}"
        apt:
          name: 
            - apache2
            - php
            - libapache2-mod-php
          state: latest
        when: ansible_distribution == 'Ubuntu'
        tags:
          - install_apache
      - name: Apache php
        apache2_module:
          name: php7.0
          state: present
        notify: Restart Apache
      handlers:
      - name: Restart Apache
        service:
          name: apache2
          state: restarted

Regarde bien en détail le playbook: 

* *hosts* précise sur quelles machines exécuter les tâches.
* *become* indique qu'il faut être *sudoer*.
* *tasks* contient les différentes tâches à lancer.
* *apt*, *user*, *authorized_key*, *lineinfile*, *apache2_module* et *service* sont `des modules <http://docs.ansible.com/ansible/latest/list_of_all_modules.html>`_.
* *when* permet d'utiliser de la conditionnalité pour l'exécution des tâches.
* *name*, *state*, *key*, *shell*, *dest*, *line* et autres sont les paramètres des modules. Pour voir la doc d'un module, tu peux utiliser la commande:

.. code-block:: bash

    ansible-doc apache2_module

Tu exécutes ton *playbook*:

.. code-block:: bash

    ansible-playbook myplaybook1.yml

Et si tu te rends sur *http://127.0.0.1:8010/* et *http://127.0.0.1:8011/*, tu obtiens bien la page
par défaut de Apache:

.. code-block:: bash

    wget http://127.0.0.1:8010/
    wget http://127.0.0.1:8011/

Tu peux relancer plusieurs fois de suite le playbook, Ansible ne fera rien de plus sur les serveurs car rien n'a changé.



Templates
=========

Dans ton playbook, tu peux également utiliser des templates pour déployer des fichiers de configuration.
Si tu as l'habitude de Django ou Flask, ça tombe bien car c'est `Jinja <http://jinja.pocoo.org/>`_ qui est utilisé par Ansible !

Tu vas maintenant mettre en place un *message du jour* (motd) sur les serveurs à l'aide d'un template.

Tu crées le template **motd** suivant dans *~/tuto_ansible/motd*:

.. code-block:: bash

    IP = {{ ansible_default_ipv4.address }}
    OS = {{ ansible_distribution }} 
    {% if env == 'prod' %}
    ENV = Production
    {% elif env == 'test' %}
    ENV = Test
    {% endif %}

Et le playbook associé dans *~/tuto_ansible/motd.yml*:

.. code-block:: yaml

    - hosts: ubuntu
      become: true
      tasks:
      - template:
          src: motd
          dest: /etc/motd
          owner: ansible
          group: ansible
          mode: 0640
          backup: yes

Tu lances ton playbook et tu testes tout ça:

.. code-block:: bash

    ansible-playbook motd.yml

Tu devrais voir:

.. code-block:: bash

    ssh -p 2200 ubuntu@127.0.0.1
    ...
    IP = 10.0.2.15
    OS = Ubuntu
    ENV = Test
    Last login: Fri Sep 29 06:45:30 2017 from 10.0.2.2
    ubuntu@ubuntu-xenial:~$

Et:

.. code-block:: bash

    ssh -p 2201 ubuntu@127.0.0.1
    ...
    IP = 10.0.2.15
    OS = Ubuntu
    ENV = Production
    Last login: Fri Sep 29 06:45:30 2017 from 10.0.2.2
    ubuntu@ubuntu-xenial:~$

Rôles
=====

Ce qui serait bien, ça serait de pouvoir organiser un peu mieux tout ça pour que tes playbooks soient réutilisables.
Tu vas pour ce faire créer un rôle **apache** qui va installer Apache et le configurer à l'aide d'un template.

C'est parti ! Tu crées un répertoire *~/tuto_ansible/roles* qui contient l'arborescence suivante:

.. code-block:: bash

    roles
    └── apache
        ├── handlers
        │   └── main.yml
        ├── tasks
        │   └── main.yml
        └── templates
            └── mysite.j2

Ou alors tu peux utiliser la commande **ansible-galaxy** pour initialiser l'arborescence complète d'un rôle:

.. code-block:: bash

    ansible-galaxy init --offline --init-path ~/tuto_ansible/roles apache

Le dossier *handlers* va te permettre d'y mettre des tâches qui vont être exécutées à chaque notification de changement.
C'est utile pour redémarrer Apache dès que c'est nécessaire par exemple.

Dans *~/tuto_ansible/roles/apache/handlers/main.yml*, tu mets:

.. code-block:: yaml

    ---
    - name: Restart Apache
      service:
        name: apache2
        state: restarted

Le dossiers *tasks* va tout simplement contenir tes tâches.

Dans *~/tuto_ansible/roles/apache/tasks/main.yml*, tu mets:

.. code-block:: yaml

    ---
    - name: Install Apache
      apt:
        name: apache2
        state: present
    - name: Check Apache
      service:
        name: apache2
        enabled: true
        state: started    
    - name: Installation d'un vhost
      template:
        src: mysite.j2
        dest: /etc/apache2/sites-available/mysite.conf
    - name: a2ensite mysite
      command: a2ensite mysite
      notify:
      - Restart Apache

Ça installe et démarre Apache, et ça déploie et active un site qui va utiliser la configuration du template *mysite.j2*.

Pour finir, dans le dossier *templates* sous *~/tuto_ansible/roles/apache/templates/mysite.j2*, tu vas mettre la configuration de ton Virtual Host Apache:

.. code-block:: bash

    <VirtualHost *:{{ http_port }}>
        ServerAdmin webmaster@{{ domain }}
        ServerName {{ domain }}
        DocumentRoot /var/www/
        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
    </VirtualHost>

Les variables **http_port** et **domain** seront à définir dans ton playbook principal.
Tu édites donc un fichier *~/tuto_ansible/playbook-apache.yml* et tu y configures ton rôle **apache**:

.. code-block:: yaml

    ---
    # role apache
    
    - hosts: ubuntu
      become: true
      vars:
        http_port: 80
        domain: localhost
      roles:
      - apache

Tu l'exécutes:

.. code-block:: bash

    ansible-playbook playbook-apache.yml

Et voilà Apache est bien installé et configuré !

Pour aller un peu plus loin, tu peux jeter un oeil aux rôles disponibles sur `Galaxy <https://galaxy.ansible.com/>`_,
tu y trouveras sûrement ton bonheur !