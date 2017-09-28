Thématique DevOps avec Ansible
##############################

:date: 2017-09-29
:tags: python,ansible,fabric,devops,linux,déploiement
:category: Linux
:slug: ansible
:authors: Morgan
:summary: Thématique DevOps avec Ansible

.. image:: ./images/ansible.png
    :alt: Ansible
    :align: right


`Ansible <https://www.ansible.com/>`_ est un *configuration management tool*, c'est-à-dire que c'est un outil qui va te permettre
d'administrer tes serveurs et d'y déployer automatiquement tes applications. Et franchement, ça bute. 

C'est très puissant tout en étant relativement simple à prendre en main, à l'inverse d'outils plus compliqués comme *Chef* ou *Puppet* par exemple.

En gros, ça va remplacer tes bons vieux scripts shell ou `fabfile <http://www.fabfile.org/>`_.


Installation
============

Vagrant
-------

Pour tester Ansible, tu vas utiliser `Virtualbox <https://www.virtualbox.org/>`_ avec `Vagrant <https://www.vagrantup.com/downloads.html>`_
pour te monter deux petites VMs Ubuntu Xenial.

Sous Ubuntu tu peux installer tout ça via la commande suivante (et redémarre ta machine si besoin):

.. code-block:: bash

    sudo apt-get install virtualbox virtualbox-dkms vagrant

Ensuite, tu te créés le fichier *Vagrantfile* suivant dans *~/tuto_ansible/vagrant/Vagrantfile* par exemple:

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

Et tu démarres tes deux Vms via:

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

Puis tu créés un ficher *hosts* à la racine du projet, dans *~/tuto_ansible/hosts* par exemple:

.. code-block:: bash

    [ubuntu]
    vm1 ansible_host=127.0.0.1 ansible_port=2200 ansible_user=ubuntu ansible_become=yes env=test
    vm2 ansible_host=127.0.0.1 ansible_port=2201 ansible_user=ubuntu ansible_become=yes env=prod

Et tu créés un fichier *ansible.cfg* qui va contenir ta configuration Ansible, dans *~/tuto_ansible/ansible.cfg* par exemple:

.. code-block:: bash

    [defaults]
    inventory      = hosts

On a désormais indiqué à Ansible d'utiliser nos deux Vms précédemment créées.

Tout est prêt !

La commande ansible
===================

Déjà, tu te places dans le répertoire *~/tuto_ansible* pour pouvoir lancer les commandes:

.. code-block:: bash

    cd ~/tuto_ansible


Ansible a besoin de python sur les machines clientes, donc si c'est pas installé par défaut: 

.. code-block:: bash

    ansible all -m raw -a "apt install -y python" --ask-sudo-pass

L'astuce ici c'est que l'option **-m raw** permet d'exécuter une commande ssh sans ansible.

Et tu essayes maintenant de contacter tes deux Vms via:

.. code-block:: bash
    
    ansible all -m ping 

Si tout est ok à ce niveau là, tu peux passer à la suite. Sinon c'est qu'il y a un souci quelque-part.

Tu vas maintenant pouvoir utiliser la commande **ansible** pour faire des trucs sur les serveurs comme :

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

Playbook
========

La commande **ansible** c'est bien mais ça va un moment. Ce que tu veux, c'est avoir une recette à exécuter qui s'occupe de mettre
à jour ou non ce dont tu as besoin sur les machines distantes. Cette recette, ça s'appelle un **playbook**.

Tu vas donc écrire un **playbook** permettant de :

* installer le paquet sudo
* créer un utilisateur ansible
* importer une clé SSH publique pour cet utilisateur
* configurer sudo pour cet utilisateur (sans mot de passe)
* installer Apache avec le support de PHP activé pour les distributions Ubuntu

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

Tu exécutes ton *playbook*:

.. code-block:: bash

    ansible-playbook myplaybook1.yml

Et si te te rends sur *http://127.0.0.1:8010/* et *http://127.0.0.1:8011/*, tu obtiens bien la page
par défaut de apache:

.. code-block:: bash

    wget http://127.0.0.1:8010/
    wget http://127.0.0.1:8011/

Tu peux relancer plusieurs fois de suite le *playbook*, Ansible ne fera rien de plus sur les serveurs car rien n'a changé.