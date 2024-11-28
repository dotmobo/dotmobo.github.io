Développer son propre RAG local avec Ollama, ChromaDB et Streamlit
##################################################################

:date: 2024-11-28
:tags: RAG, LLM, ChromaDB, Ollama, Python, Streamlit
:category: IA
:slug: first-rag
:authors: Morgan
:summary: Développer son propre RAG local avec Ollama, ChromaDB et Streamlit

.. image:: ./images/ollama.png
    :alt: Recommandations de films
    :align: right

Tu veux créer une application de recommandations de films basée sur **Retrieval-Augmented Generation (RAG)** ?

Super, dans cet article, on va utiliser plusieurs technologies pour construire une application intelligente qui te recommande des films en fonction
de tes préférences.

On va utiliser **ChromaDB** pour stocker et indexer les films, **Sentence-Transformers** pour générer des embeddings, et **Ollama** pour faire les recommandations.

Charger les Données des Films
-----------------------------

On commence par préparer les données des films. Imaginons que tu aies un fichier `data/data.json` qui contient des informations comme le titre du film, le synopsis, l'ID IMDb, etc.

.. code-block:: python

    def load_movies(file_path="data/data.json"):
        """Loads movie data from the JSON file."""
        with open(file_path, "r") as f:
            return json.load(f)

Cette fonction va simplement charger les films depuis le fichier JSON et nous permettra d’ajouter ces films à notre index dans ChromaDB.

Initialiser ChromaDB
--------------------

Ensuite, on initialise **ChromaDB**, une base de données qui nous permet de stocker les embeddings des films. Cela nous permettra de rechercher efficacement les films en fonction des requêtes de l'utilisateur.

.. code-block:: python

    def initialize_chromadb():
        """Initializes and returns a ChromaDB client with a movie collection."""
        client = chromadb.Client(Settings(is_persistent=True, anonymized_telemetry=False))
        return client

Générer les Embeddings
----------------------

On utilise **Sentence-Transformer** pour transformer chaque film en un vecteur d'embedding. Cela permet d'effectuer des recherches sémantiques, c’est-à-dire que tu peux rechercher des films en fonction de leur contenu et non de mots-clés exacts.

.. code-block:: python

    def generate_embeddings(model, content):
        """Generates embeddings for a given content."""
        return model.encode(content)

Indexer les Films
-----------------

Une fois qu'on a les embeddings, on va les ajouter dans **ChromaDB**. On va indexer chaque film en utilisant son titre et son synopsis. Si un film est déjà dans l'index, on ne le réajoute pas.

.. code-block:: python

    def index_movies(movies, model, collection):
        """Indexes movies in ChromaDB only if the index doesn't exist already."""
        for movie in movies:
            doc_id = movie["imdbID"]
            title = movie["Title"]
            plot = movie["Plot"]
            content = f"{title}: {plot}"

            # Check if the document already exists
            existing_document = collection.get(ids=[doc_id])

            # If the document exists, skip it
            if existing_document["documents"]:
                print(
                    f"The document with ID {doc_id} already exists. It will not be added."
                )
                continue

            # Generate the embedding
            embedding = generate_embeddings(model, content)

            # Add to the collection
            collection.add(
                ids=[doc_id],
                metadatas=[{"title": title, "year": movie["Year"]}],
                documents=[content],
                embeddings=[embedding],
            )
        print("Data indexed in ChromaDB.")

Rechercher dans ChromaDB
------------------------

Maintenant, on va créer une fonction qui va effectuer la recherche dans ChromaDB en fonction de la requête de l'utilisateur. On va utiliser les embeddings de la requête pour chercher les films les plus pertinents dans la base de données.

.. code-block:: python

    def perform_query(collection, model, query):
        """Performs a search in ChromaDB and returns the results."""
        query_embedding = generate_embeddings(model, query)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3,  # Return 3 results
        )
        return results

Générer un Prompt pour Ollama
-----------------------------

Une fois que nous avons trouvé les films pertinents, on va générer un prompt pour **Ollama** afin qu’il nous recommande des films à partir des résultats de la recherche.

.. code-block:: python

    def generate_prompt(context, query):
        """Generates a prompt for Ollama where the model acts as a DVD salesperson."""
        return f"""
    You are a knowledgeable DVD salesperson with expertise in movies. Your task is to recommend movies to customers, but you can only suggest films that are available in the store's inventory. Make sure your recommendations are based solely on the list of movies provided.

    Context: Below is a list of movies currently available in the store:
    {context}

    Customer's Question: Ask for a movie about {query}

    Your Movie Recommendations (only from the available list):
    """

Interroger Ollama
-----------------

Ensuite, on va utiliser **Ollama** pour obtenir les recommandations basées sur notre prompt. Ollama va générer une réponse en fonction des films que nous avons indexés.

.. code-block:: python

    def query_ollama(prompt, model_name="myllama"):
        """Queries Ollama with the given prompt."""
        client = ollama.Client()
        response = client.chat(model_name, messages=[{"role": "user", "content": prompt}])
        return response["message"]["content"]

Créer une Interface Utilisateur avec Streamlit
----------------------------------------------

Enfin, on va utiliser **Streamlit** pour créer une interface utilisateur simple. L'utilisateur peut entrer une requête, et l'application va afficher les films pertinents ainsi que la réponse générée par Ollama.

.. code-block:: python

    def main():
        # Load the movies
        movies = load_movies()

        # Initialize SentenceTransformer to generate embeddings
        model = SentenceTransformer("all-MiniLM-L6-v2")

        # Initialize ChromaDB
        client = initialize_chromadb()

        # Check if the collection exists already
        collection = client.get_or_create_collection(name="movies")

        # If the collection is empty (does not exist), index the movies
        if not collection.count():
            print("Indexing movies in ChromaDB...")
            index_movies(movies, model, collection)
        else:
            print("The movie index already exists. It was not regenerated.")

        # Streamlit user interface
        st.title("Movie Recommendations")
        query = st.text_input("Ask for a movie about...", "a wormhole in space")

        if st.button("Ask"):
            if query:
                # Perform the search
                results = perform_query(collection, model, query)

                # Prepare the prompt for Ollama as the DVD salesperson
                documents = results.get("documents", [])
                if documents is None:
                    documents = []

                # Display the results in the UI
                st.subheader("Movies Found")
                for doc in documents:
                    st.write(doc)

                context = "\n".join(
                    [f"- {doc}" for result in documents if result for doc in result]
                )
                prompt = generate_prompt(context, query)

                # Display the prompt in the UI
                st.subheader("Prompt Sent to Ollama")
                st.text_area("Here is the prompt sent to Ollama", prompt, height=200)

                # Show the loading spinner while the request is being processed
                with st.spinner("Searching..."):
                    # Query Ollama
                    response = query_ollama(prompt, model_name="llama3.2")

                st.subheader("Ollama's Recommendation")
                st.write(response)

    if __name__ == "__main__":
        main()

Dans cet article, nous avons construit une application de recommandation de films en utilisant **RAG**, **ChromaDB**, **Sentence-Transformers** et **Ollama**. Cette approche permet de tirer parti des embeddings pour effectuer des recherches plus intelligentes, basées sur le contenu plutôt que sur des mots-clés exacts. Avec **Streamlit**, nous avons également créé une interface simple et interactive pour l'utilisateur, lui permettant d'obtenir des recommandations personnalisées sur la base de sa requête.

Cela démontre comment ces technologies peuvent être combinées pour offrir des solutions puissantes et efficaces en matière de recherche et de recommandation de contenu, tout en facilitant l'intégration et l'utilisation grâce à des outils comme **ChromaDB** et **Streamlit**.