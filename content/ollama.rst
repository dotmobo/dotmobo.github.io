Ma première IA locale avec Ollama et OpenWebUI
##############################################

:date: 2025-11-24
:tags: python, ollama, openwebui, openai
:category: IA
:slug: ollama
:authors: Morgan
:summary: Ma première IA locale avec Ollama et OpenWebUI

.. image:: ./images/ollama.png
    :alt: Ollama
    :align: right

Après avoir parlé d'architecture LLM et d'agents, on va revenir à la
base de la base : **installer une IA sur son poste et la faire parler**.

L'objectif ? Démystifier ce qu'est un moteur d'inférence, manipuler un
premier modèle, jouer avec les paramètres, et monter une petite
interface web pour chatter avec ton LLM. Le tout **en local**, sans
cloud, sans clé API, juste avec ton Linux et deux outils : **Ollama** et
**OpenWebUI**.

C'est quoi un LLM, déjà ?
=========================

Avant de lancer des commandes dans le terminal, petit rappel rapide.

Un **LLM** (*Large Language Model*), c'est un gros réseau de neurones
entraîné à un niveau indécent sur des montagnes de texte. Son job est
simple : **prédire le mot suivant**.

Mais derrière ce côté simpliste, tu as tout un pipeline :

-  des **tokens** (morceaux de mots),
-  une **vectorisation** (représentation mathématique des idées),
-  un mécanisme **Transformer** qui pige le contexte d'une phrase,
-  et un modèle qui sort une probabilité pour chaque mot possible.

Tu lui donnes une phrase, il complète. Tu lui poses une question, il
infère. Tu lui fournis un contexte, il adapte sa réponse.

Les modèles modernes comme Qwen, Llama 3 ou Mistral tournent aujourd'hui
très bien **en local**, même sur de petites machines. Et c'est
exactement ce qu'on va exploiter.

Ollama : ton premier moteur d'inférence
=======================================

`Ollama <https://ollama.com/>`_, c'est un petit bijou : un moteur d'inférence ultra simple à
installer, compatible Linux/macOS/Windows, et surtout très efficace pour
gérer et exécuter des modèles LLM localement.

Tu l'installes en une commande:

.. code-block:: bash

   curl -fsSL https://ollama.com/install.sh | sh

Tu vérifies:

.. code-block:: bash

   ollama -v

Et tu lances le moteur:

.. code-block:: bash

   ollama serve

Pour être sûr que c'est ok, tu peux vérifier le port via telnet:

.. code-block:: bash

   telnet localhost 11434

Maintenant, le plus sympa : télécharger un modèle.

Par exemple un **qwen3:0.6b**, petit mais très rapide:

.. code-block:: bash

   ollama pull qwen3:0.6b

L'avantage de ce modèle, c'est que tu peux le faire tourner sur un CPU. Pas besoin de carte graphique.

Tu listes alors tes modèles:

.. code-block:: bash

   ollama list

Et tu discutes avec lui:

.. code-block:: bash

   ollama run qwen3:0.6b


Jouer avec les paramètres : créativité et contrôle
==================================================

Une des forces d'Ollama, c'est la possibilité de régler très simplement
les paramètres:

-  **température** : créativité / chaos
-  **top-k** : combien de candidats on garde avant de choisir
-  **top-p** : probabilité cumulée à couvrir
-  **repeat-penalty** : éviter que le modèle te fasse un copier-coller de lui-même

Tu lances:

.. code-block:: bash

   /show parameters

Puis tu modifies:

.. code-block:: bash

   /set parameter temperature 0

Des paramètres plus bas donnent des réponses plus précises et conservatrices, tandis que des valeurs plus élevées
rendent les réponses plus variées et créatives. Tout dépend de ton usage !

Créer ton propre modèle : le Modelfile
======================================

Ollama te permet d'ajouter un **comportement système** directement dans un fichier ``Modelfile``:

.. code-block:: bash

   FROM qwen3:0.6b

   PARAMETER temperature 0.7
   PARAMETER top_k 30
   PARAMETER top_p 0.9
   PARAMETER repeat_penalty 1

   SYSTEM """
   Rôle : Tu es un chat qui découvre un objet mystérieux dans son jardin.
   Langue : Tu parles un français soutenu.
   Personnalité : Tu es farceur.
   """

Compilation:

.. code-block:: bash

   ollama create chat -f ./Modelfile

Tu peux alors discuter avec ton modèle personnalisé de la même façon que précédemment:

.. code-block:: bash

   ollama run chat

Utiliser Ollama avec Python
===========================

Créer l'environnement virtuel:

.. code-block:: bash

   python -m venv .env
   source .env/bin/activate
   pip install ollama

Script ``main.py`` pour chatter avec le modèle ``chat:latest``:

.. code-block:: bash

   from ollama import Client

   client = Client()

   messages = [
     {
       'role': 'user',
       'content': "Qui es-tu et que fais-tu aujourd'hui?",
     },
   ]

   for part in client.chat('chat:latest', messages=messages, stream=True):
     print(part['message']['content'], end='', flush=True)

Exécution du code:

.. code-block:: bash

   python main.py

Tu remarqueras qu'on a utilisé ici le mode streaming pour afficher la
réponse au fur et à mesure. Pratique pour les interfaces web !

OpenWebUI : une interface web pour ton LLM
==========================================

`OpenWebUI <https://github.com/open-webui/open-webui>`_ est une interface web open-source qui te permet de chatter
avec tes modèles locaux (Ollama, LocalAI, etc.) via une interface
moderne. C'est l'outil le plus suivi dans le monde des LLM locaux avec LibreChat.

Installation Python:

.. code-block:: bash

   pip install open-webui
   open-webui serve

Ou via Docker:

.. code-block:: bash

   docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway \
   -v open-webui:/app/backend/data --name open-webui \
   --restart always ghcr.io/open-webui/open-webui:main

Tu ouvres:

.. code-block:: bash

   http://localhost:8080/

Tu y retrouveras :

-  chat multi-modèles
-  historique
-  RAG intégré
-  administration
-  API
-  paramètres avancés

Première expérience RAG
=======================

OpenWebUI permet de créer un petit RAG local : uploader un PDF, notes,
markdown. On peut poser des questions comme :

-  *Explique la page 12 du PDF*
-  *Fais-moi un résumé*
-  *Trouve tous les passages sur Kubernetes*

Conclusion
==========

Avec Ollama et OpenWebUI tu as :

-  un moteur d'inférence local,
-  une interface moderne,
-  la possibilité d'ajouter une personnalité (Modelfile),
-  une API Python,
-  un premier RAG,
-  bref : **ta première IA personnelle**.

Bonne exploration !
