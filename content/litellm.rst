Moteurs d'inférence et passerelle LiteLLM
#########################################

:date: 2025-11-24
:tags: python, llm, litellm, vllm, IA
:category: IA
:slug: moteurs-inference-litellm
:authors: Morgan
:summary: Moteurs d'inférence et passerelle LiteLLM

.. image:: ./images/litellm.png
    :alt: LiteLLM
    :align: right

Après avoir exploré la création d'une première IA locale avec Ollama et OpenWebUI, nous passons à l'étape suivante:
déployer des modèles sur des moteurs d'inférence de production et les servir avec `LiteLLM <https://www.litellm.ai/>`_.

Qu'est-ce qu'un moteur d'inférence ?
====================================

Un moteur d'inférence charge un modèle de LLM en mémoire et exécute les requêtes entrantes.
Il peut gérer différents types de modèles, appliquer des paramètres d'exécution et servir les réponses via une API.
Dans l'atelier précédent, nous avons utilisé **Ollama**, simple et efficace pour un usage local.

LiteLLM
=======

**LiteLLM** est une passerelle entre les moteurs d'inférence (Ollama, vLLM, etc.) et des clients comme OpenWebUI.
Il offre :

* Une API compatible OpenAI
* L'agrégation de modèles
* Le load-balancing et fallback
* La gestion du budget et des utilisateurs
* Des contrôles de santé (health checks)

Installation et configuration
=============================

On commence par créer un projet, activer un environnement virtuel Python et installer litellm :

.. code-block:: bash

    mkdir monprojet && cd monprojet
    python -m venv .env && source .env/bin/activate
    pip install litellm[proxy]

Ensuite, un fichier **config.yaml** définit les modèles et paramètres :

.. code-block:: yaml

    general_settings:
        master_key: sk-secret

    model_list:
    - model_name: qwen3
        model_info:
            max_tokens: 32768
            max_input_tokens: 16384
            max_output_tokens: 16384
        litellm_params:
            model: ollama/qwen3:0.6b
            api_base: http://localhost:11434
            temperature: 0.7
            max_tokens: 4096
            top_p: 0.9
            frequency_penalty: 1
            tpm: 300000
            rpm: 300

    litellm_settings:
        num_retries: 3
        request_timeout: 3600
        allowed_fails: 5
        cooldown_time: 30

Ici, on sert le modèle "qwen3" via LiteLLM qu'on a configuré lors de `l'article précédent <https://dotmobo.xyz/ollama.html>`_.
On peut ajuster les paramètres de génération comme la température, top_p, ou les pénalités de fréquence.

Exécution et requêtes
=====================

On démarre litellm avec cette configuration :

.. code-block:: bash

    litellm --config config.yaml

L'API est disponible sur `http://localhost:4000/ <http://localhost:4000/>`_.
On peut vérifier l'état du serveur avec :

.. code-block:: bash

    curl -H "Authorization: Bearer sk-secret" http://localhost:4000/health


Et pour interroger le modèle, tu peux faire un appel POST comme suit :

.. code-block:: bash

    curl -X POST http://localhost:4000/chat/completions \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer sk-secret" \
    -d '{
        "model": "qwen3",
        "messages": [{"role": "user", "content": "Hello!"}]
    }'


Support multi-modèles et fallback
=================================

LiteLLM permet d’ajouter un second modèle (ex. qwen2.5) et de configurer le fallback.

.. code-block:: yaml

    model_list:
    - model_name: qwen2.5
        model_info:
            max_tokens: 32768
            max_input_tokens: 16384
            max_output_tokens: 16384
        litellm_params:
            model: ollama/qwen2.5:0.5b
            api_base: http://localhost:11434

    litellm_settings:
        fallbacks:
            [
                {"qwen3": ["qwen2.5"]}
            ]

Pour faire du load-balancing, il suffit de donner le même *model_name* à plusieurs moteurs.

Les requêtes sont alors réparties selon la configuration des poids et priorités avec les paramètres *weight*,
*rpm* (requests per minute) et *tpm* (tokens per minute).

Utilisation avec Python
=======================

L'api de litellm étant openai compatible, tu peux utiliser le client OpenAI pour faire des requêtes :

.. code-block:: bash

    pip install openai


Exemple d'appel depuis Python :

.. code-block:: python

    import openai

    client = openai.OpenAI(api_key="sk-secret", base_url="http://localhost:4000")
    response = client.chat.completions.create(
        model="qwen",
        messages=[{"role": "user", "content": "Écris un court poème"}]
    )
    print(response.choices[0].message.content)


vLLM : moteur pour de la production
==============================

Pour des usages plus lourds, **vLLM** offre :

* Optimisation mémoire GPU avec PagedAttention
* Exécution simultanée de plusieurs requêtes
* Tensor Parallelism pour multi-GPU
* API OpenAI compatible
* Support LoRA et quantification
* Intégration Kubernetes avancée
* Métriques exposées pour Prometheus

Tu peux l'installer et démarrer un modèle Qwen 3 FP8 avec :

.. code-block:: bash

    pip install vllm
    vllm serve Qwen/Qwen3-0.6B-FP8

Et tu peux faire du paramétrage avancé sur deux GPUs avec :

.. code-block:: bash

    vllm serve --model Qwen/Qwen3-0.6B-FP8 \
    --max-model-len 40960 \
    --gpu-memory-utilization 0.8 \
    --swap-space 8 \
    --dtype bfloat16 \
    --kv-cache-dtype fp8 \
    --tensor-parallel-size 2 \
    --enable-auto-tool-choice --tool-call-parser hermes \
    --enable-reasoning --reasoning-parser deepseek_r1 \
    --disable-log-stats --disable-log-requests


Métriques Prometheus et tableau de bord Grafana
================================================

Les métriques sont exposées sur `http://localhost:8000/metrics <http://localhost:8000/metrics>`_, permettant le suivi de l’utilisation GPU, des requêtes et des performances.

Autres moteurs
=================

* **SGLang** : concurrent direct de vLLM (`http://sglang.ai/ <http://sglang.ai/>`_)
* **MAX** : alternative sans CUDA (`https://www.modular.com/max <https://www.modular.com/max>`_)
* **Speaches** : spécialisé en TTS et STT (`https://speaches.ai/ <https://speaches.ai/>`_)
* **Infinity** : embeddings et reranking (`https://github.com/michaelfeil/infinity <https://github.com/michaelfeil/infinity>`_)

Conclusion
============

Avec LiteLLM et vLLM, tu peux passer d’un prototype local à un déploiement de modèles LLM en production, avec gestion des utilisateurs, load-balancing, métriques et intégration multi-GPU.
Ces outils constituent la passerelle idéale entre la facilité d’Ollama et la robustesse des moteurs professionnels.
