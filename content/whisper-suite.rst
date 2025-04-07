Utiliser un LLM pour générer un compte-rendu stylisé en Markdown
################################################################

:date: 2025-04-04
:tags: Python, Streamlit, LLM, Whisper
:category: IA
:slug: whisper-suite
:authors: Morgan
:summary: Utiliser un LLM pour générer un compte-rendu stylisé en Markdown

.. image:: ./images/openai.png
    :alt: Whisper
    :align: right

On enchaîne avec la suite de l'article sur `Whisper <https://dotmobo.xyz/whisper.html>`_ et on va utiliser un LLM pour générer un compte-rendu stylisé en Markdown.

Précédemment, on avait utilisé Ollama pour faire tourner notre LLM. Histoire de changer, on va utiliser cette fois-ci
`vLLM <https://vllm.ai/>`_, qui est une alternative qui se veut plus performante pour la production.

Par contre, il ne tourne que sous GPU, donc si tu n'as qu'un CPU, il te faudra rester sur `Ollama <https://ollama.ai/>`_.

vLLM
----

En amont, il te faudra avoir installé `CUDA <https://developer.nvidia.com/cuda-toolkit>`_ sur ton système. Ensuite, pour exécuter vLLM, on va utiliser le container Docker officiel.
Il te faudra un token `Hugging Face <https://huggingface.co/>`_ et définir une clé API pour vLLM.

.. code-block:: bash
    
    docker run --runtime nvidia --gpus all \
        -v ~/.cache/huggingface:/root/.cache/huggingface \
        -e "HUGGING_FACE_HUB_TOKEN=S3CR3T" \
        -e "VLLM_API_KEY=S3CR3T" \
        -p 8000:8000 --ipc=host \
        vllm/vllm-openai:latest --model mlabonne/Daredevil-8B

On le lance ici avec le modèle `Daredevil-8B <https://huggingface.co/mlabonne/Daredevil-8B>`_, qui est un llama 3.1 Instruct amélioré et qui marche plutôt bien pour ce qu'on veut faire.

Tu peux tester qu'il tourne correctement en testant l'url :

.. code-block:: bash

    curl http://localhost:8000/v1/models

Ok, notre LLM est prêt ! On va pouvoir modifier le code de notre application whisper pour améliorer le compte-rendu généré.

Il te faudra installer dans ton environnement virtuel la librairie `openai` :

.. code-block:: bash

    pip install openai

En effet, l'api de vLLM est directement compatible avec l'api de OpenAI, donc tu peux utiliser la même librairie !

Tu reprends le fichier `main.py` du `précédent article <https://dotmobo.xyz/whisper.html>`_ et tu vas modifier la fonction `summarize` pour y ajouter une
étape de formatage des phrases récupérées par sumy en Markdown.

On prévoit donc l'utilisation d'une fonction `format_summary` pour le faire.

.. code-block:: python

    @st.cache_data
    def summarize(text: str, num_sentences: int, language: str) -> str:
        summarize = summarize_text(text, num_sentences=num_sentences, language=language)
        format = format_summary(
            "http://localhost:8000",
            "S3CR3T",
            "mlabonne/Daredevil-8B",
            summarize,
            language=language,
        )
        return format


    from openai import OpenAI

    def format_summary(base_url: str, authtoken: str, model: str, summary: str, language="en") -> str:
        client = OpenAI(api_key=authtoken, base_url=base_url)

        prompt = f"""
        You are an advanced assistant specialized in summarizing meetings.
        Reformat the following summary into a structured meeting report **without changing or adding any information**.
        You must **only use the sentences provided**. Do not invent, modify, or infer any details.

        The output **should be in the following language**: {language.upper()}.

        Structure:
        - **Introduction**
        - **Points**
        - **Decisions**
        - **Actions**

        Ensure that all section titles are also in the same language as the output.

        **Raw Summary (Use only these sentences):**
        {summary}

        **Structured Meeting Report in Markdown:**
        """

        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4096,
            temperature=0.3,
        )

        return response.choices[0].message.content  # type: ignore


Toute l'intelligence de l'assistant est dans le prompt. Tu peux le modifier pour changer le style de ton compte-rendu.

Ici, on s'assure qu'il ne va utiliser que les phrases récupérées par sumy et qu'il ne va pas en inventer de nouvelles.

Lui spécifier la structure permet d'avoir des résultats homogènes lors de chaque génération.

On lui précise bien qu'on veut du Markdown en sortie et qu'il conserve la langue du résumé.

La température plutôt basse ici renforce l'idée de ne pas inventer d'informations.

Au début, sans ces recommandations, il m'inventait des dates de réunion, des noms de personnes, etc.

Certains LLMs sont plus performants que d'autres pour ce genre de tâche. Ici, Daredevil-8B fait le taf, mais j'imagine
qu'il existe sûrement sur Hugging Face des modèles encore plus performants ! A toi de voir.

Tu relances streamlit et tu peux voir le résultat.

.. code-block:: bash

    streamlit run main.py

Pour exemple, à partir de cette transcription :

.. code-block:: markdown

    Bonjour à tous, nous allons commencer la réunion pour savoir si nous allons changer notre parc de voiture ou pas.
    Il faut savoir qu'il y a 5 voitures et il y en a 2 qui sont actuellement cassés.
    Qu'est-ce qu'on fait ?
    On va vendre les 2 voitures cassés et on va en acheter de nouvelles.
    Jim, tu vas aller chez Renault et tu vas t'occuper de l'avance.
    Jim, tu vas aller chez Mercedes et on va acheter de nouveaux véhicules pour compléter le parc.
    C'est ok pour tout le monde.
    Bien, je vous remets fin à la réunion.

On obtient le résumé stylisé suivant :

.. code-block:: markdown

    **Introduction**
    Bonjour à tous, nous allons commencer la réunion pour savoir si nous allons changer notre parc de voitures ou pas.

    **Points**
    Il faut savoir qu'il y a cinq voitures et il y en a deux qui sont actuellement cassées.

    **Decisions**
    On va vendre les deux voitures cassées et on va en acheter deux nouvelles.

    **Actions**
    - Jim, tu vas aller chez Renault et tu vas t'occuper de la vente.
    - John, tu vas aller chez Mercedes et on va acheter de nouveaux véhicules pour compléter le parc.

Pas si mal non ?