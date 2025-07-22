Mettre en place une architecture LLM OpenAI-compatible
######################################################

:date: 2025-07-22
:tags: Python, LLM, vLLM, Ollama, Infinity, Speaches, LiteLLM, Open WebUI
:category: IA
:slug: archi-llm
:authors: Morgan
:summary: Mettre en place une architecture LLM OpenAI-compatible

.. image:: ./images/openai.png
    :alt: OpenAI
    :align: right


On va voir comment mettre en place une architecture de LLMs compatible avec l'API d'`OpenAI <https://platform.openai.com/docs/overview>`_, en utilisant des outils comme **vLLM**, **Ollama**, **Infinity**, **Speaches** et **LiteLLM**.
De ce faire, ton service sera utilisable avec n'importe quelle application ou librairie qui se base sur l'API d'OpenAI.

Je ne vais pas rentrer dans le détail concernant l'installation de chaque brique, car tu trouveras facilement les informations
nécessaires sur leurs sites officiels, et il existe déjà tout un tas de tutoriels sur le sujet. On va juste se contenter de
les déployer avec **Docker**.

Docker compose
==============

On initie un fichier `docker-compose.yml` pour orchestrer le déploiement de nos services, qu'on va alimenter au fur et à mesure.
Voici la structure de base de notre fichier, avec le réseau et les volumes que nous utiliserons. On va tout mettre dans le même docker compose pour plus de clarté
dans cet article, mais tu pourras le découper en morceaux si tu souhaites déployer plusieurs services sur plusieurs machines.

.. code-block:: yaml

    version: '3.8'

    networks:
      vllm:
        name: vllm
        external: true

    services:
        # On va ajouter nos services ici au fur et à mesure

    volumes:
        huggingface_data:
        ollama_data:
        infinity_data:
        speaches_data:
        postgresql_data:
        redis_data:


On crée un réseau externe qu'on appelle **vllm**, qui va nous permettre de connecter nos services entre eux.
Bien sûr en amont de tout ça il te faut **Docker**, **Docker Compose**, **Cuda** et les **drivers NVIDIA** installés sur ta machine.

Tu le crées via :

.. code-block:: bash

    docker network create \
    --driver bridge \
    --subnet 192.168.0.0/24 \
    --gateway 192.168.0.1 \
    vllm


LLM principal
===============

On attaque avec le déploiement de notre **LLM principal** :

- **Qwen 3 30B A3B** est un modèle plutôt intéressant actuellement avec son mode de **reasoning**
- `vLLM <https://docs.vllm.ai/en/latest/>`_ est le serveur d'inférence le plus populaire et le plus simple à mettre en place pour de la production

On ajoute le service dans notre `docker-compose.yml` :

.. code-block:: yaml

  vllm:
    image: vllm/vllm-openai:v0.9.2
    restart: always
    runtime: nvidia
    environment:
      NVIDIA_VISIBLE_DEVICES: "all"
      HUGGING_FACE_HUB_TOKEN: "your_huggingface_token"
      VLLM_API_KEY: "your_vllm_api_key"
    volumes:
      - "huggingface_data:/root/.cache/huggingface"
    command: "--disable-log-stats --disable-log-requests --model 'Qwen/Qwen3-30B-A3B-FP8' --max-model-len 131072 --gpu-memory-utilization 0.8 --swap-space 8 --kv-cache-dtype 'auto' --enable-auto-tool-choice --tool-call-parser 'hermes' --enable-reasoning --reasoning-parser 'deepseek_r1' --rope-scaling '{\"rope_type\":\"yarn\",\"factor\":4.0,\"original_max_position_embeddings\":32768}'"
    shm_size: 32g
    networks:
      - vllm
    healthcheck:
      test: ["CMD", "curl", "-sf", "http://localhost:8000/metrics"]
      interval: 60s
      timeout: 30s
      retries: 5

Au niveau des options de vLLM :

- on désactive les logs des requêtes pour éviter de polluer les logs
- on utilise le max de la taille de contexte du modèle à l'aide de **rope**
- on active le **reasoning** et le **tooling**
- on utilise 80% du GPU pour laisser de la place pour les autres services tout en lui donnant assez de mémoire pour être tranquille

On mettra systématiquement en place un **healthcheck** pour monitorer les services.


LLM secondaire
==============

On va désormais déployer un service `Ollama <https://ollama.ai/>`_ pour nos **LLMs secondaires**. Ollama n'est pas vraiment prévu pour gérer
beaucoup d'utilisateurs en parallèle, mais il va permettre de faire des tests avec d'autres modèles pour prototyper par exemple.
Ça reste un outil intéressant mais il faut juste garder en tête que lorsque tu veux vraiment des performances, bascule sur vLLM.

On ajoute le service dans notre `docker-compose.yml` :

.. code-block:: yaml

  ollama:
    image: ollama/ollama:0.9.6
    restart: always
    runtime: nvidia
    environment:
      NVIDIA_VISIBLE_DEVICES: "all"
      OLLAMA_KV_CACHE_TYPE: "q8_0"
      OLLAMA_KEEP_ALIVE: "24h"
      OLLAMA_MAX_LOADED_MODELS: "2"
      OLLAMA_FLASH_ATTENTION: "1"
    volumes:
      - ollama_data:/root/.ollama
    shm_size: 2g
    networks:
      - vllm
    healthcheck:
      test: ["CMD", "ollama", "list", "||", "exit", "1"]
      interval: 60s
      timeout: 30s
      retries: 5

On quantifie le **KV cache** et on active le **flash attention** pour améliorer les performances.

Et après à travers ton container, tu pourras pull des modèles, ici par exemple on va mettre un modèle **Vision** :

.. code-block:: bash

    ollama pull qwen2.5vl:7b-q4_K_M


Embedding et reranking
========================

Pour faire du **RAG**, tu vas avoir besoin d'un modèle d'**embedding** afin d'alimenter ta base de données vectorielle type `Qdrant <https://qdrant.tech/>`_ ainsi
qu'un modèle de **reranking** pour améliorer la pertinence des résultats.

Personnellement j'utilise `Infinity <https://github.com/michaelfeil/infinity>`_ qui est un petit service dédié à ces modèles. Certains partent sur `TGI de Hugging Face <https://huggingface.co/docs/text-generation-inference>`_ qui peut aussi faire l'affaire.

On ajoute le service dans notre `docker-compose.yml` :

.. code-block:: yaml

  infinity:
    image: michaelf34/infinity:0.0.76
    restart: always
    runtime: nvidia
    environment:
      NVIDIA_VISIBLE_DEVICES: "all"
      DO_NOT_TRACK: "1"
      INFINITY_ANONYMOUS_USAGE_STATS: "0"
    volumes:
      - infinity_data:/app/.cache
    command: v2 --model-id 'BAAI/bge-reranker-v2-m3' --model-id 'nomic-ai/nomic-embed-text-v1.5' --port 7997
    shm_size: 2g
    networks:
      - vllm
    healthcheck:
      test: ["CMD", "curl", "-sf", "http://localhost:7997/health"]
      interval: 60s
      timeout: 30s
      retries: 5

Infinity est intéressant car il permet de déployer plusieurs modèles en même temps. Ici on utilise **nomic** pour l'embedding et **BGE** pour le reranking.

Text-to-speech et Speech-to-text
=================================


`Speaches <https://github.com/speaches-ai/speaches>`_ est un service qui permet de déployer des modèles **TTS** et **STT** en mode OpenAI-compatible.
Il te permettra d'utiliser les routes **/audio/transcriptions** et **/audio/speech**.

On ajoute le service dans notre `docker-compose.yml` :

.. code-block:: yaml

  speaches:
    image: ghcr.io/speaches-ai/speaches:0.8.2-cuda-12.6.3
    restart: always
    runtime: nvidia
    environment:
      NVIDIA_VISIBLE_DEVICES: "all"
      LOG_LEVEL: "INFO"
    volumes:
      - speaches_data:/home/ubuntu/.cache/huggingface/hub
    shm_size: 2g
    networks:
      - vllm
    healthcheck:
      test: ["CMD", "curl", "-sf", "http://localhost:8000/health"]
      interval: 60s
      timeout: 30s
      retries: 5

Depuis le container, tu pourras récupéerer fast-whisper pour le STT et Piper pour le TTS via :

.. code-block:: bash

    huggingface-cli download speaches-ai/piper-fr_FR-siwis-medium
    huggingface-cli download Systran/faster-whisper-small

Orchestration avec LiteLLM
============================

Et voilà, tu as tous tes services prêts à être orchestrés.

Ok maintenant qu'on a nos différents services, on va les orchestrer avec `LiteLLM <https://www.litellm.ai/>`_.

LiteLLM va se charger de faire le routage des requêtes OpenAI vers les services adéquats, en fonction de la route demandée.

On imagine que tu crées le fichier de configuration suivant dans `/root/litellm/config.yaml` :

.. code-block:: yaml

    general_settings:
      master_key: your_master_key
      proxy_batch_write_at: 60
      database_connection_pool_limit: 10

    model_list:
      # Notre LLM principal
      - model_name: qwen3
        model_info:
          max_tokens: 65536
          max_input_tokens: 65536
          max_output_tokens: 65536
        litellm_params:
          model: hosted_vllm/Qwen/Qwen3-30B-A3B-FP8
          api_base: http://vllm:8000
          api_key: your_vllm_api_key
      # Notre LLM secondaire
      - model_name: qwen2.5-vl
        model_info:
          max_tokens: 16384
          max_input_tokens: 16384
          max_output_tokens: 16384
        litellm_params:
          model: ollama/qwen2.5vl:7b-q4_K_M
          api_base: http://ollama:11434
      # Embedding et reranking
      - model_name: nomic
        litellm_params:
          model: infinity/nomic-ai/nomic-embed-text-v1.5
          api_base: http://infinity:7997
        model_info:
          mode: embedding
      - model_name: bge-reranker
        litellm_params:
          model: infinity/BAAI/bge-reranker-v2-m3
          api_base: http://infinity:7997
        model_info:
          mode: rerank
      # TTS et STT
      - model_name: whisper
        litellm_params:
          model: openai/Systran/faster-whisper-small
          api_base: http://speaches:8000
        model_info:
          mode: audio_transcription
      - model_name: piper
        litellm_params:
          model: openai/speaches-ai/piper-fr_FR-siwis-medium
          api_base: http://speaches:8000
        model_info:
          mode: audio_speech

    litellm_settings:
      num_retries: 3
      request_timeout: 3600
      fallbacks: []
      allowed_fails: 5
      cooldown_time: 30
      set_verbose: False
      json_logs: True
      cache: False
      drop_params: True
      telemetry: False


On a ici une configuration de base pour servir nos modèles. En amélioration, tu pourrais gérer des modèles de **fallbacks** et des
limites en **rpm** et en **tpm**. Si tu as plusieurs cartes graphiques, tu peux dupliquer tes modèles dessus et liteLLM se chargera
de faire la répartition de charge en fonction de la stratégie de **routing** que tu auras choisie.


On ajoute le service dans notre `docker-compose.yml`. Note qu'il nous faut un **postgresql** et un **redis** pour stocker les données de LiteLLM :

.. code-block:: yaml

    redis:
      image: redis:8
      restart: always
      networks:
        - vllm
      volumes:
        - redis_data:/data
      environment:
        REDIS_PASSWORD: "your_redis_password"
      command: ["redis-server", "--appendonly", "yes"]
      healthcheck:
        test: ["CMD", "redis-cli", "ping"]
        interval: 60s
        timeout: 30s
        retries: 5

    postgres:
      image: postgres:17
      restart: always
      networks:
        - vllm
      environment:
        POSTGRES_USER: "your_postgres_user"
        POSTGRES_PASSWORD: "your_postgres_password"
        POSTGRES_DB: "your_postgres_db"
      volumes:
        - postgresql_data:/var/lib/postgresql/data
      healthcheck:
        test: ["CMD", "pg_isready", "-U", "your_postgres_user"]
        interval: 60s
        timeout: 30s
        retries: 5

    litellm:
      image: ghcr.io/berriai/litellm:main-v1.74.0-stable
      container_name: litellm
      restart: always
      depends_on:
        - postgres
        - redis
      environment:
        - LITELLM_MODE=PRODUCTION
        - LITELLM_LOG=ERROR
        - LITELLM_SALT_KEY=your_salt_key
        - DATABASE_URL=postgresql://your_postgres_user:your_postgres_password@postgres:5432/your_postgres_db
        - REDIS_URL=redis://redis:6379/0
      ports:
        - "4000:4000"
      command: --config /app/config.yaml --telemetry False
      volumes:
        - /root/litellm/config.yaml:/app/config.yaml
      networks:
        - vllm
      healthcheck:
        test: ["CMD-SHELL", "wget --quiet --tries=1 http://localhost:4000/health/liveliness || exit 1"]
        interval: 60s
        timeout: 30s
        retries: 5

Et voilà, tu démarres tout ça et tu peux accéder à ton API OpenAI compatible sur http://localhost:4000.

Utilisation de l'API
====================

Tu peux alors par exemple utiliser la librairie **OpenAI** en python ou utiliser **curl** directement pour faire des requêtes du type :

.. code-block:: bash

    curl -X POST http://localhost:4000/chat/completions \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer your_master_key" \
    -d '{
        "model": "qwen3",
        "messages": [
            {
                "role": "user",
                "content": "Hello, how are you?"
            }
        ]
    }'

Tu peux utiliser les routes :

- **/chat/completions** pour les modèles de chat avec **qwen3** et **qwen2.5-vl**
- **/embeddings** pour les modèles d'embeddings avec **nomic**
- **/rerank** pour les modèles de reranking avec **bge-reranker**
- **/audio/transcriptions** pour les modèles de transcription audio avec **whisper**
- **/audio/speech** pour les modèles de synthèse vocale avec **piper**


Tu pourras aussi utiliser ton API sur des interfaces graphiques comme `Open WebUI <https://openwebui.com/>`_ ou `LibreChat <https://librechat.ai/>`_.
Étant OpenAI compatible, tu pourras l'utiliser dans des workflows d'agents comme `N8N <https://n8n.io/>`_ ou encore utiliser dans des librairies comme `LangChain <https://www.langchain.com/>`_.

L'archi finale que tu pourras mettre en place pourra ressembler à ça :

.. image:: ./images/archi-llm.png
    :alt: Architecture LLM OpenAI-compatible
    :align: center

Et voilà ! Tu disposes maintenant d'une architecture LLM complète, flexible et compatible avec l'écosystème OpenAI. N'hésite pas à expérimenter avec d'autres modèles et à adapter cette configuration à tes besoins. Bon déploiement !