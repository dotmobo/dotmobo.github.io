Booster les performances de son RAG avec la quantification
##########################################################

:date: 2024-12-12
:tags: RAG, LLM, ChromaDB, Ollama, Python, Streamlit
:category: IA
:slug: quantification
:authors: Morgan
:summary: Booster les performances de son RAG avec la quantification

.. image:: ./images/sentencetransformers.png
    :alt: SentenceTransformer de films
    :align: right


Dans `mon article précédent <https://dotmobo.xyz/first-rag.html>`_, tu as découvert comment mettre en place un RAG pour recommander des films.
On avait utilisé un petit fichier JSON pour stocker les films, mais imagine maintenant que ton RAG doive parcourir des
millions de documents. Là, tu vas vite voir que les requêtes deviennent de plus en plus longues et que la mémoire explose.

La bonne nouvelle, c’est qu’avec la quantification, tu peux réduire significativement la taille des embeddings,
ce qui améliore la performance.



Tweaking de SentenceTransformer avec la quantification
------------------------------------------------------

Reprends ton projet de RAG et tweake `SentenceTransformers <https://sbert.net/>`_ pour intégrer la quantification binaire.
La modification est simple et se résume à une ligne :

.. code-block:: python

    def generate_embeddings(model, content):
        """Génère des embeddings pour un contenu donné avec quantification binaire."""
        return model.encode(content, precision="binary")

On ajoute **precision="binary"** lors de l'encodage du contenu. Mais concrètement, qu’est-ce que ça signifie ?

La précision "binary" implique qu’au lieu de stocker chaque valeur de l’embedding comme un nombre flottant
(qui utilise 4 octets par valeur), chaque dimension est convertie en une valeur binaire (0 ou 1).
Cela réduit la taille des embeddings d’un facteur 32 et accélère les recherches.


Gain de performance à quel prix ?
---------------------------------

Grâce à cette méthode, tu réduis considérablement l’espace disque et la mémoire nécessaires pour stocker tes embeddings.
Tu peux maintenant effectuer des recherches sur des millions de documents sans souci.

Un aperçu des différences entre les embeddings flottants et binaires en terme de taille :

.. code-block:: python

    >>> embeddings.shape
    (2, 1024)
    >>> embeddings.nbytes
    8192
    >>> embeddings.dtype
    float32
    >>> binary_embeddings.shape
    (2, 128)
    >>> binary_embeddings.nbytes
    256
    >>> binary_embeddings.dtype
    int8

Mais il y a un **mais** : la perte de précision est l’un des inconvénients majeurs.
La quantification est une méthode de compression, et donc les valeurs binaires ne peuvent pas contenir autant
d’informations que les valeurs flottantes. Selon l’application, cela peut ne pas être adapté.

Pour un système de recherche de films, cette approche reste largement suffisante. En revanche, si tes embeddings doivent capter des nuances très fines,
la quantification peut affecter la qualité des résultats.

À toi de décider si cette solution est adaptée à ton cas, mais c’est une technique intéressante à garder en tête.

