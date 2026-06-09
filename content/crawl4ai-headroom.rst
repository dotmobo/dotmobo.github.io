Découverte de Crawl4AI et de Headroom
#####################################

:date: 2026-06-09
:tags: python, agents, crawl4ai, headroom, llm
:category: IA
:slug: crawl4ai-headroom
:authors: Morgan
:summary: Découverte de Crawl4AI et de Headroom

.. image:: ./images/python.png
    :alt: Python
    :align: right


Suite à un atelier sur le développement d'agents que j'ai fait récemment, j'en profite pour vous faire partager
deux petites librairies que j'ai trouvées vraiment pratiques. Je pose ça là, vous en faites ce que vous voulez !

Crawl4AI
=========

`Crawl4AI <https://github.com/unclecode/crawl4ai>`_ est un web crawler et scraper prévu spécialement pour les agents
IA. Il permet tout simplement de récupérer n'importe quelle page web en un Markdown clean et épuré.

Derrière, il exécute réellement un Chromium en headless avec Playwright pour récupérer la page, ce qui lui permet
d'être compatible avec les SPA en pure JS.

Tu l'installes avec pip et tu lances l'outil de configuration qui va télécharger toutes les librairies et outils nécessaires
comme Chromium :

.. code-block:: bash

    pip install crawl4ai
    crawl4ai-setup
    crawl4ai-doctor

La commande **crawl4ai-doctor** permet de vérifier que tout est prêt.

Un exemple de fonction que tu peux mettre sur un MCP par exemple pour récupérer une page

.. code-block:: python

    async def fetch_page_content(url: str) -> str:
        """
        Fetch the full text content of a documentation page.

        Args:
            url: The full URL of the page to fetch.
        """

        try:
            async with AsyncWebCrawler(config=BrowserConfig(headless=True)) as crawler:
                result = await crawler.arun(
                    url=url,
                    config=CrawlerRunConfig(
                        cache_mode=CacheMode.ENABLED, check_cache_freshness=True
                    ),
                )
                if result.success:
                    content = result.markdown or ""
                    return str(content)
                else:
                    return f"Error: Crawler failed to fetch content. {result.error if hasattr(result, 'error') else ''}"
        except Exception as e:
            return f"Error fetching page content: {str(e)}"

On va rapidement décortiquer le code :

- On utilise Chromium en Headless via **config=BrowserConfig(headless=True)**
- On active le cache via **cache_mode=CacheMode.ENABLED**, ce qui permet à l'outil de conserver le markdown d'une page déjà explorée.
- On met à jour le cache en vérifiant via une requête HEAD la date de création de la page via **check_cache_freshness=True**
- On récupère le markdown de la page via **result.markdown**

Et c'est tout ! Si tu combines **fetch_page_content** dans un MCP avec un autre tool du type **search_documentation**,
tu peux facilement te faire un MCP qui va récupérer de la documentation sur n'importe quel site web.

Headroom
========

Avec nos agents qui deviennent de plus en plus complexes et avec une taille de contexte qui augmente tous les mois sur les modèles
de LLM, il devient important d'étudier la manière de compresser le contexte pour optimiser les coûts en tokens des requêtes.

Il y a eu des premières initiatives avec le très fun `caveman <https://github.com/JuliusBrussee/caveman>`_
et avec `rtk <https://github.com/rtk-ai/rtk>`_, mais c'est le récent `Headroom <https://github.com/chopratejas/headroom>`_ qui a été
récemment diffusé en open source par un développeur de chez Netflix qui est l'outil le plus complet.

Comme d'habitude on l'installe avec pip :

.. code-block:: bash

    pip install "headroom-ai[all]"

Il s'utilise de la manière suivante. Imaginons un contexte assez gros avec des résultats d'appels de fonctions stockés à
l'intérieur.

.. code-block:: python

    from headroom import compress
    import json
    from openai import OpenAI

    messages = [
        {"role": "system", "content": "You analyze search results."},
        {"role": "user", "content": "Search for Python tutorials."},
        {
            "role": "assistant",
            "content": None,
            "tool_calls": [{
                "id": "call_1",
                "type": "function",
                "function": {"name": "search", "arguments": '{"q": "python"}'},
            }],
        },
        {
            "role": "tool",
            "tool_call_id": "call_1",
            "content": json.dumps({
                "results": [
                    {"title": f"Result {i}", "snippet": f"Description {i}", "score": 100 - i}
                    for i in range(500)
                ]
            }),
        },
        {"role": "user", "content": "What are the top 3 results?"},
    ]

    result = compress(messages, model="qwen3", model_limit=224000)

    client = OpenAI(base_url="https://my-openai-like-api", api_key="sk-secret")
    response = client.chat.completions.create(
        model="qwen3",
        messages=result.messages,
    )

    print(response.choices[0].message.content)

    print(f"Tokens before: {result.tokens_before}")
    print(f"Tokens after:  {result.tokens_after}")
    print(f"Tokens saved:  {result.tokens_saved}")
    print(f"Compression:   {result.compression_ratio:.0%}")
    print(f"Transforms:    {result.transforms_applied}")

Tout s'effectue sur la ligne **compress(messages, model="qwen3", model_limit=224000)**.
Headroom prend tous les messages du contexte et le compresse avec diverses techniques comme rtk notamment.
On précise le type de modèle et la limite du modèle et c'est parti !

A l'exécution de ce script, on remarque qu'il a fait économiser 41% de tokens !


.. code-block:: bash

    Tokens before: 13626
    Tokens after:  8039
    Tokens saved:  5587
    Compression:   41%
    Transforms:    ['router:protected:user_message', 'router:protected:user_message', 'router:smart_crusher:0.25']

De plus, il fournit également un mode proxy au besoin et il est intégrable dans **litellm** via des callbacks en ajoutant les lignes suivantes dans
le fichier de configuration de litellm :

.. code-block:: yaml

    # litellm_config.yaml
    litellm_settings:
        callbacks: ["headroom.integrations.litellm_callback.HeadroomCallback"]

Bonne découverte !
