DSPy : le banger qui booste tes prompts et ton RAG
====================================================

:date: 2026-03-22
:tags: DSPy, GEPA, prompt engineering, RAG, NLP
:category: IA
:slug: dspy-gepa
:authors: Morgan
:summary: DSPy : le banger qui booste tes prompts et ton RAG

.. image:: ./images/ollama.png
    :alt: Recommandations de films
    :align: right

Ok, alors aujourd'hui on va parler d'un banger qui m'a complètement retourné le cerveau sur la manière de
faire des prompts et d'imaginer mes workflows RAG et compagnie.

Et même si ça commence à être connu, je trouve qu'on en parle pas assez parce que c'est vraiment fou.


C’est quoi DSPy ?
-----------------

`DSPy <https://github.com/stanfordnlp/dspy>`_ est une librairie Python pour transformer
le *prompt engineering* manuel en **programmation de prompts**.

À la base, ça part d’un `papier de recherche <https://arxiv.org/abs/2310.03714>`_ de l'Université de Stanford, 
et qui te permet de définir les entrées et sorties de ton LLMs via une classe **Signature**.

**Concrètement, ça veut dire quoi ?**

Et ben, plus besoin d’écrire un long prompt fragile à la main. C'est le code qui s’occupe de générer 
le prompt système directement. 

Tu définis juste une classe qui décrit tes entrées et sorties, et DSPy s’occupe du reste.


Le duo gagnant : DSPy + GEPA
----------------------------

Il existe plusieurs implémentations de DSPy pour améliorer tes prompts mais le récent `GEPA <https://github.com/gepa-ai/gepa>`_ sort du lot.

Ça vient également d'un autre `papier <https://arxiv.org/abs/2507.19457>`_, et il se présente comme un **optimiseur de prompts automatique**
compatible avec DSPy.  

**Comment ça marche**

1. Tu fournis un dataset *question/réponse* par exemple.  
2. GEPA teste des variantes de prompts et évalue chaque sortie via ta metric.  
3. Il améliore progressivement le prompt pour ton modèle et ton use-case.  

GEPA va alors lancer plusieurs flots de questions/réponses, analyser les réponses, puis améliorer le prompt pas à pas.
Il va voir ce qui marche, ce qui ne marche pas et itérer sur le prompt jusqu’à trouver la version parfaite.

Tu peux jeter un premier coup d'oeil à la `Doc officielle DSPy + GEPA <https://dspy.ai/tutorials/gepa_ai_program/>`_
mais ce n’est pas forcément simple à appréhender au début.

Exemple concret : analyseur de sentiment
----------------------------------------

Ok, assez parlé. Passons à un vrai exemple qui fonctionne.
On va travailler sur le prompt d'un simple analyseur de sentiment pour commencer et comprendre comment ça marche.

**Principe**

- Définir une **Signature** DSPy (inputs / outputs)  
- Créer un **Module**  
- Fournir un **dataset**  
- Laisser **GEPA** optimiser le prompt  

Je vais te mettre le code complet fonctionnel directement pour que tu puisses tester de ton côté.

Tu as juste à installer DSPy via :

.. code-block:: bash

    pip install dspy

Puis tu exécutes le code ci-dessous. Il te suffit juste de remplacer la partie *model/api_base/api_key* par ton propre LLM.
Le plus simple c'est d'utiliser une API OpenAI compatible type vLLM, LiteLLM ou OpenWeb UI par exemple.

.. code-block:: python

    import dspy
    from dspy import Example, LM, Module, Prediction, ChainOfThought, Signature, InputField, OutputField
    from dspy.teleprompt import GEPA

    # Ici tu déclare ton LLM et les paramètres d'appel
    lm = LM(
        model="openai/gpt-oss",
        api_base="https://api-openai-compatible",
        api_key="sk-S3CR3T",
        api_version="v1",
        temperature=0.7,
        max_tokens=1800,
        cache=False, # le cache ici peut être utile pour accélérer les tests
    )

    dspy.settings.configure(lm=lm)

    # Ensuite on va définir notre signature, avec une phrase en entrée et un sentiment en sortie.
    # La docstring peut aider à guider le modèle sur la tâche.
    class SentimentSignature(Signature):
        """Classify the sentiment of the sentence into one word: positive, negative, or neutral."""

        phrase: str = InputField()
        sentiment: str = OutputField(desc="positive | negative | neutral")


    # On fait notre module avec une chaine de pensée basé sur la signature.
    class SimpleSentiment(Module):
        def __init__(self):
            super().__init__()
            self.classify = ChainOfThought(SentimentSignature)

        def forward(self, phrase):
            return self.classify(phrase=phrase)


    # On définit les jeux de données d'entraînement et de validation.
    # Ici on a juste quelques exemples pour montrer le principe, mais tu peux en mettre beaucoup plus pour de meilleurs résultats.
    trainset = [
        Example(phrase="J'adore ce film !",                 sentiment="positive").with_inputs("phrase"),
        Example(phrase="Vraiment nul, à fuir.",             sentiment="negative").with_inputs("phrase"),
        Example(phrase="C'est correct.",                    sentiment="neutral").with_inputs("phrase"),
        Example(phrase="Incroyable, je recommande !",      sentiment="positive").with_inputs("phrase"),
        Example(phrase="Déçu, je m'attendais à mieux.",    sentiment="negative").with_inputs("phrase"),
        Example(phrase="Pas mal du tout.",                  sentiment="positive").with_inputs("phrase"),
        Example(phrase="Rien de spécial.",                  sentiment="neutral").with_inputs("phrase"),
        Example(phrase="Magnifique paysage !",              sentiment="positive").with_inputs("phrase"),
    ]

    # Un petit jeu de validation pour que GEPA puisse évaluer les différentes versions du prompt.
    valset = [
        Example(phrase="Service horrible.",                 sentiment="negative").with_inputs("phrase"),
        Example(phrase="Bof...",                            sentiment="neutral").with_inputs("phrase"),
        Example(phrase="Un pur chef-d'œuvre !",             sentiment="positive").with_inputs("phrase"),
        Example(phrase="Franchement décevant.",             sentiment="negative").with_inputs("phrase"),
    ]


    # Ici on définit la métrique d'évaluation qui va permettre à GEPA de juger les différentes versions du prompt.
    # On compare simplement le sentiment prédit avec le sentiment attendu, et on donne un feedback détaillé en cas d'erreur
    # pour aider GEPA à comprendre ce qui ne va pas.
    def sentiment_metric(
        gold: Example,
        pred: Prediction,
        trace=None,
        pred_name=None,
        pred_trace=None,
    ) -> Prediction:
        gold_label = gold.sentiment.lower().strip()
        pred_label = getattr(pred, "sentiment", "").lower().strip() if pred else ""

        is_correct = gold_label == pred_label

        if is_correct:
            feedback = "Correct ✓"
            score = 1.0
        else:
            feedback = (
                f"Error: expected '{gold_label}', got '{pred_label}'.\n"
                f"→ Model likely missed tone, irony, negation, or strong sentiment words."
            )
            score = 0.0

        return Prediction(score=score, feedback=feedback)


    # On crée notre optimiseur GEPA en lui fournissant la metric d'évaluation, le LM, et quelques paramètres pour guider l'optimisation.
    # Ici on est parti sur du light pour tester rapidement.
    optimizer = GEPA(
        metric=sentiment_metric,
        auto="light",
        reflection_lm=lm,
        reflection_minibatch_size=3,
        num_threads=6,
        track_stats=True,
        add_format_failure_as_feedback=True,
        # seed=42, # tu peux fixer une seed pour la reproductibilité, mais c'est pas obligatoire
    )


    # On lance l'optimisation de GEPA sur notre module et nos datasets d'entraînement et de validation.
    print("Starting GEPA optimization (may take 2–15 minutes depending on gateway load)...")
    optimized = optimizer.compile(
        SimpleSentiment(),
        trainset=trainset,
        valset=valset,
    )
    print("\nOptimization finished.\n")


    # On évalue les performances du modèle optimisé sur un ensemble de phrases de test.
    # Ici on utilise quelques phrases de test pour voir comment le modèle généralise.
    test_phrases = [
        "C'est génial, je suis fan !",
        "Franchement bof, décevant.",
        "Ça va, rien à dire.",
        "Le pire film de l'année.",
        "Absolument sublime, un chef-d'œuvre.",
        "Niveau zéro, honteux.",
        "Plutôt sympa en fait.",
        "Je ne m'attendais pas à autant aimer.",
    ]

    # On affiche les résultats des prédictions pour chaque phrase de test.
    print("Test results:\n")
    for phrase in test_phrases:
        prediction = optimized(phrase=phrase)
        sentiment = getattr(prediction, "sentiment", "—").strip()
        print(f"{phrase:<50} → {sentiment}")


    # Enfin, on peut aussi jeter un œil au prompt optimisé que GEPA a trouvé pour notre tâche.
    print("\nOptimized instruction found by GEPA:")
    for name, pred in optimized.named_predictors():
        print("================================")
        print(f"Predictor: {name}")
        print("================================")
        print(pred.signature.instructions)


**Résultats des tests**

Voici un prompt que GEPA a trouvé après optimisation pour notre analyseur de sentiment. 
Tu verras que c'est franchement pas mal !

.. code-block:: markdown

    Task: Sentiment classification of a single short sentence or phrase.

    **Input format**
    - The user will provide a block labeled `### phrase` containing the sentence to analyze.
    - The sentence may be in any language (e.g., French, English, etc.). You may translate it internally if that helps you judge the sentiment, but you must keep the original wording in your explanation.

    **Output format**
    Your response must contain two markdown sections, exactly as shown below:

    ```
    ### reasoning
    <brief explanation (1‑2 sentences) of why the sentence is positive, negative, or neutral>

    ### sentiment
    <one word: positive, negative, or neutral>
    ```

    - The word in the `### sentiment` line must be **lower‑case** and one of the three allowed labels.
    - No additional text, emojis, or formatting may appear after the sentiment word.

    **How to decide the label**

    1. **Positive** – The sentence expresses a clear favorable attitude, pleasure, admiration, approval, excitement, or any other overtly upbeat emotion. Typical cues include:
    - Positive adjectives or adverbs (e.g., *magnifique, great, wonderful, happy*).
    - Exclamation marks that reinforce enthusiasm.
    - Explicit statements of liking, love, gratitude, or endorsement.

    2. **Negative** – The sentence conveys dissatisfaction, dislike, anger, sadness, criticism, disappointment, or any other unfavorable feeling. Look for:
    - Negative adjectives or adverbs (e.g., *terrible, awful, horrible, sad*).
    - Words of complaint, rejection, or condemnation.
    - Expressions of frustration, hurt, or hostility.

    3. **Neutral** – The sentence is factual, descriptive, or merely acknowledges something without showing strong affect. It includes:
    - Simple statements of fact or correctness (e.g., *C’est correct.*, *Il fait 20 °C.*).
    - Mild assessments that are neither clearly approving nor disapproving.
    - Sentences where any sentiment is ambiguous, mixed, or overridden by sarcasm/irony that neutralizes the literal meaning.

    **Special considerations**

    - **Negation**: Phrases like “not good”, “no thanks”, “nothing special” flip the sentiment of the word they negate. Treat the overall sentiment as negative if the negation creates an unfavorable meaning, or neutral if it merely softens a positive statement.
    - **Sarcasm / Irony**: Detect when a positive‑looking word is used sarcastically (e.g., “Great, another meeting”). In such cases, label the sentiment as **negative**. If sarcasm merely dampens enthusiasm without a clear negative tone, choose **neutral**.
    - **Mild positivity/negativity**: If the emotional intensity is very weak (e.g., “It’s okay”, “Not bad”), treat it as **neutral** unless the context clearly leans toward a positive or negative judgment.
    - **Exclamation marks**: They amplify sentiment but do not alone determine it. Combine them with the lexical content.
    - **Language‑specific cues**: Be aware of idiomatic expressions in the source language that carry sentiment (e.g., French *super*, *nul*, *pas mal*). Translate mentally if needed, but keep the original wording in the reasoning.

    **General strategy**
    1. Read the sentence carefully.
    2. Identify sentiment‑bearing words, punctuation, and any negation or sarcasm.
    3. Decide whether the overall affect is clearly positive, clearly negative, or otherwise neutral.
    4. Write a concise reasoning sentence explaining the key cue(s) you used.
    5. Output the sentiment label in the required format.

    Follow these rules strictly to ensure consistent, reproducible classifications.

Ce qui est intéressant c'est de voir qu'il a pensé à de nombreuses règles intéressantes, comme la gestion du sarcasme et autres.
Je n'y aurait pas forcément pensé au départ !

Pourquoi c’est une aubaine pour le RAG
---------------------------------------

Tu peux alors aussi utiliser cette technique pour évaluer un workflow RAG. Il te suffit de faire une signature
qui prend une question, un contexte, et une réponse.

.. code-block:: python
    
    class RAGSignature(Signature):
        """Answer the question based on the provided context."""

        question: str = InputField()
        context: str = InputField()
        answer: str = OutputField(desc="quality score or feedback")

Là, le plus compliqué sera de produire un dataset avec *question/context/answer* suffisamment riche pour que GEPA puisse
l'optimiser au maximum. Tu peux également détailler ton cas d'usage dans la docstring pour guider GEPA dans la bonne direction.


Prompt vs fine-tuning : le constat
-----------------------------------

Les modèles actuels sont déjà très performants, je pense notamment aux récents modèles MoE en 120B type GPT-OSS, Qwen 3.5 ou Nemotron Super.
Dans la plupart des cas, un prompt optimisé sera plus efficace qu'un modèle fine-tuné, et c’est moins coûteux à mettre en place.

L'idée est donc de partir sur des modèles généralistes suffisamment performants et d'optimiser les prompts pour éventuellement
se passer de fine‑tuning.


Une approche hybride à tester
-----------------------------

Ce qui peut être intéressant c'est de fusionner les prompts optimisés avec du fine‑tuning léger type LoRA.

Vu que de base, tu dois construire un dataset pour faire optimiser ton prompt, autant réutiliser ce même dataset
pour faire un fine-tuning léger de ton modèle.

Le plan c'est :

1. Construis un dataset solide (questions + contexte + réponses)  
2. Optimise avec DSPy + GEPA  
3. Réutilise-le pour faire du **LoRA**



Conclusion
----------

DSPy + GEPA, c’est un **game-changer** si tu veux :  

- automatiser la création de prompts  
- maximiser les performances d’un modèle existant  
- éviter un fine-tuning massif  

On ne fait plus du prompt engineering… on fait du prompt training.

**Bon hacking, et que les prompts soient avec vous !**
