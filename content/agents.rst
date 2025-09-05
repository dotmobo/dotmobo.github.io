Développement d'agents IA
#########################

:date: 2025-09-05
:tags: python, agents, openai, sdk, agno
:category: IA
:slug: agents-ia
:authors: Morgan
:summary: Développement d'agents IA

.. image:: ./images/openai.png
    :alt: OpenAI
    :align: right

Après avoir passé en revue l'architecture de base des LLMs avec `les moteurs d'inférence et l'orchestration de base <https://dotmobo.xyz/archi-llm.html>`_,
on va faire une petite introduction aux agents IA avec un outil ultra léger qui nous vient d'OpenAI appelé **OpenAI Agents SDK**.

Qu'est ce qu'un agent IA ?
==========================

Déjà pour commencer, démystifions le terme agent. On l'entend à toutes les sauces et ça veut tout et rien dire au premier abord.

Donc déjà, **un agent c'est quoi ?**

Un agent, c'est juste une fonction qui va prendre ton prompt d'entrée, faire l'appel au LLM et te restituer la réponse.

La spécificité d'un agent réside dans ce qu'il peut utiliser autour de ça :

- des **instructions** : pour indiquer le comportement de l'agent. Il s'agit du **prompt système** en réalité.
- un **historique** : pour garder le contexte de la conversation en cours. On pourra le stocker dans une **base de données ou en mémoire**.
- une **mémoire** : pour se souvenir des préférences de l'utilisateur, de ses habitudes, du style de réponse et autres.
- des **outils** : pour appeler des fonctions personnalisées comme l'appel à des API externes, l'exécution de calculs ou autres.
- des **connaissances** : pour enrichir le contexte de l'agent et lui permettre de mieux comprendre et répondre aux requêtes. En général, c'est couplé à une **base de données vectorielle**. C'est la technique qu'on appelle communément **RAG**.
- du **raisonnement** : pour réfléchir en amont et décider de la stratégie à adopter sur les appels d'outils par exemple.

Un agent peut également déléguer des tâches à d'autres agents spécialisés, c'est ce qu'on appelle un **workflow** d'agents.

Agno
====

Il existe plusieurs bibliothèques d'agents, plus ou moins complexes et complètes. La première que j'ai découverte qui m'avait tapé dans l'œil était
`Agno <https://docs.agno.com/>`_ qui est vraiment complet et qui permet de faire beaucoup de choses. C'est elle qui m'a permis de comprendre le
concept d'agent.

Elle définit plusieurs niveaux d'agents, ce qui permet de se lancer progressivement en fonction des besoins.
Tu l'installes déjà avec pip par exemple :

.. code-block:: bash

    pip install agno

Niveau 1 : Agents avec des outils et des instructions
-----------------------------------------------------

Ici, on a notre premier agent qui va utiliser le modèle **Claude** pour récupérer des données
sous forme de tableau via une recherche web avec un outil permettant d'interroger **DuckDuckGo**.

.. code-block:: python

    from agno.agent import Agent
    from agno.models.anthropic import Claude
    from agno.tools.duckduckgo import DuckDuckGoTools

    agent = Agent(
        model=Claude(id="claude-sonnet-4-20250514"),
        tools=[DuckDuckGoTools()],
        instructions="Use tables to display data. Don't include any other text.",
        markdown=True,
    )
    agent.print_response("What is the stock price of Apple?", stream=True)

Niveau 2 : Agents avec un historique et des connaissances
---------------------------------------------------------

Cet agent stocke la conversation dans une base de données **SQLite** pour pouvoir par la suite la passer en contexte.

Il utilise également une base de données vectorielle **LanceDB** pour stocker des connaissances issues de fichiers Markdown.

Avant de répondre à la question, l'agent va automatiquement chercher les infos dans la base de connaissances pour enrichir le contexte.

.. code-block:: python

    from agno.agent import Agent
    from agno.embedder.openai import OpenAIEmbedder
    from agno.knowledge.url import UrlKnowledge
    from agno.models.anthropic import Claude
    from agno.storage.sqlite import SqliteStorage
    from agno.vectordb.lancedb import LanceDb, SearchType

    knowledge = UrlKnowledge(
        urls=["https://docs.agno.com/introduction.md"],
        vector_db=LanceDb(
            uri="tmp/lancedb",
            table_name="agno_docs",
            search_type=SearchType.hybrid,
            embedder=OpenAIEmbedder(id="text-embedding-3-small", dimensions=1536),
        ),
    )

    storage = SqliteStorage(table_name="agent_sessions", db_file="tmp/agent.db")

    agent = Agent(
        name="Agno Assist",
        model=Claude(id="claude-sonnet-4-20250514"),
        instructions=[
            "Search your knowledge before answering the question.",
            "Only include the output in your response. No other text.",
        ],
        knowledge=knowledge,
        storage=storage,
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_runs=3,
        markdown=True,
    )

    if __name__ == "__main__":
        agent.knowledge.load(recreate=False)
        agent.print_response("What is Agno?", stream=True)

Niveau 3 : Agents avec une mémoire et du raisonnement
-----------------------------------------------------

La mémoire est stockée dans une base SQLite et on laisse le modèle la gérer comme il l'entend.

Le raisonnement est ici géré par un outil appelé **ReasoningTools** et tu peux voir l'intégralité du
raisonnement grâce à **show_full_reasoning=True**.

.. code-block:: python


    from agno.agent import Agent
    from agno.memory.v2.db.sqlite import SqliteMemoryDb
    from agno.memory.v2.memory import Memory
    from agno.models.anthropic import Claude
    from agno.tools.reasoning import ReasoningTools
    from agno.tools.duckduckgo import DuckDuckGoTools

    memory = Memory(
        model=Claude(id="claude-sonnet-4-20250514"),
        db=SqliteMemoryDb(table_name="user_memories", db_file="tmp/agent.db"),
        delete_memories=True,
        clear_memories=True,
    )

    agent = Agent(
        model=Claude(id="claude-sonnet-4-20250514"),
        tools=[
            ReasoningTools(add_instructions=True),
            DuckDuckGoTools(search=True, news=True),
        ],
        user_id="ava",
        instructions=[
            "Use tables to display data.",
            "Include sources in your response.",
            "Only include the report in your response. No other text.",
        ],
        memory=memory,
        enable_agentic_memory=True,
        markdown=True,
    )

    if __name__ == "__main__":
        agent.print_response(
            "My favorite stocks are NVIDIA and TSLA",
            stream=True,
            show_full_reasoning=True,
            stream_intermediate_steps=True,
        )
        agent.print_response(
            "Can you compare my favorite stocks?",
            stream=True,
            show_full_reasoning=True,
            stream_intermediate_steps=True,
        )

OpenAI Agents SDK
=================

Une autre bibliothèque minimaliste sortie récemment est `OpenAI Agents SDK <https://github.com/openai/openai-agents-python>`_.

Elle est assez proche du fonctionnement d'Agno mais plus légère et plus simple à prendre en main.
Si tu utilises l'API d'OpenAI ou que tu as une architecture locale avec **LiteLLM**, ça s'intègre parfaitement bien.

Tu l'installes avec pip :

.. code-block:: bash

    pip install "openai-agents[litellm]"

Tu crées un agent qui va utiliser un modèle exposé par LiteLLM et un outil personnalisé, ici une fonction Python
qui retourne la météo.

N'importe quelle fonction avec le décorateur **@function_tool** peut être utilisée.

L'important pour que l'agent s'en sorte facilement est d'utiliser le typage optionnel avec **mypy**, **ty** ou **pyright**.
Et de bien documenter la fonction avec une **docstring** valide.

.. code-block:: python

    from __future__ import annotations
    import asyncio
    from agents import Agent, Runner, function_tool, set_tracing_disabled
    from agents.extensions.models.litellm_model import LitellmModel

    @function_tool
    def get_weather(city: str) -> str:
        """
        Get the weather for a city.
        Args:
            city (str): The city to get the weather for.
        Returns:
            str: The weather in the city.
        """
        return f"The weather in {city} is sunny."


    async def main():
        agent = Agent(
            name="Assistant",
            instructions="You only respond in haikus.",
            model=LitellmModel(base_url="https://mylitellm", model="qwen3", api_key="S3CRET"),
            tools=[get_weather],
        )
        result = await Runner.run(agent, "What's the weather in Tokyo?")
        print(result.final_output)

    if __name__ == "__main__":
        asyncio.run(main())

Si tu veux gérer plusieurs agents, tu peux utiliser le paramètre **handoffs**.

Par exemple, on a un agent de booking, un agent de remboursement et un agent de triage qui va rediriger
les questions vers le bon agent en fonction du sujet.

.. code-block:: python


    from agents import Agent

    booking_agent = Agent(...)
    refund_agent = Agent(...)

    triage_agent = Agent(
        name="Triage agent",
        instructions=(
            "Help the user with their questions. "
            "If they ask about booking, hand off to the booking agent. "
            "If they ask about refunds, hand off to the refund agent."
        ),
        handoffs=[booking_agent, refund_agent],
    )


Et voilà, tu as un bon premier aperçu des agents avec ces deux bibliothèques sympas.

Si ça t'intéresse, on pourra aller plus loin dans un prochain article avec la gestion de workflows complets.

Notia
=====

Pour appréhender un peu tout ça, je me suis amusé à créer un outil appelé `Notia <https://github.com/dotmobo/notia>`_,
qui est un assistant de prise de notes basé sur un agent avec des outils.

J'y ai défini un certain nombre de fonctions que l'agent est capable d'utiliser pour gérer les notes de l'utilisateur,
ainsi qu'un prompt système qui permet à l'agent de les utiliser convenablement.

.. code-block:: python

    agent = Agent(
        name="Notia",
        instructions=dedent("""
            /no_think

            You are Notia, a powerful AI assistant designed to be a developer's second brain.
            
            Your purpose is to help manage project-related notes, ideas, tasks, and code snippets.
            
            You have access to a set of tools to add, list, delete, and search notes in a vector database.
            
            Be helpful, concise, and proactive. When a user asks a question, use your search tool to find
            the most relevant notes to answer it.
            
            Pay close attention to the 'Rerank Score' provided by the search tool;
            a higher score indicates greater relevance to the query.
        """),
        model=LitellmModel(base_url="https://mylitellm", model="qwen3", api_key="S3CRET"),
        tools=[
            add_note,
            list_all_notes,
            delete_note,
            search_notes,
            edit_note,
            get_note_by_id,
            search_notes_by_project,
            list_all_projects,
            export_notes_by_project_to_csv,
            analyze_all_notes,
            extract_top_keywords,
        ]
    )

On gère une session SQLite qui permet de conserver l'historique de la conversation et de la passer dans le contexte à l'exécution de la requête.

.. code-block:: python

    session = SQLiteSession("notia")

Avec ça, je lui envoie des messages (query) du type

- *"Ajoute une note pour mon projet X avec comme contenu Y"*
- *"Liste moi toutes les notes que j'ai sur le projet X"*
- *"Supprime la note avec l'ID X"*
- *"Cherche dans mes notes tout ce qui parle de X"*
- *"Extrait les mots-clés de mes notes"*

On l'exécute et ça marche tout seul :

.. code-block:: python

    response = await Runner.run(agent, query, session=session)

Certaines des fonctions sont même `écrites en Rust à l'aide de Maturin <https://dotmobo.xyz/maturin.html>`_ pour le fun et la performance.

Have fun !
