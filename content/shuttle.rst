Shuttle.rs
#############

:date: 2024-07-28
:tags: shuttle, shuttle.rs, rust, devops, server, deploy, deployment, ci, cd, integration
:category: Rust
:slug: shuttle-rs
:authors: Morgan
:summary: Shuttle.rs

.. image:: ./images/shuttle.png
    :alt: Shuttle
    :align: right


Aujourd'hui, je vais te parler d'un service que je viens de découvrir et qui mérite le coup d'oeil.

Si comme moi, tu as quelques projets perso que tu veux héberger mais que tu n'as pas forcément envie de débourser un abonnement pour un hébergeur,
tu es au bon endroit.

Pour héberger du front-end, c'est facile. On a au choix `Netlify <https://www.netlify.com/>`_ ou `Vercel <https://vercel.com/>`_ qui font très bien
l'affaire. 

Mais si c'est pour un back-end avec une base de données, c'est tout de suite une autre affaire si tu ne veux pas utiliser de méthode **serverless**.

Jusqu'à présent, j'utilisais `Pythonanywhere <https://www.pythonanywhere.com/>`_ qui est vraiment un super service pour déployer du Python, et de
temps en temps `Render <https://render.com/>`_, mais qui a de grosses latences pour son service gratuit.

En cherchant une solution pour héberger du `Rust <https://www.rust-lang.org/fr>`_, je suis alors tombé sur `Shuttle <https://www.shuttle.rs/>`_.
Shuttle se veut être le Vercel du backend en gros.

Non seulement la version Community de l'outil est gratuite, mais elle permet d'avoir directement une base de données Postgres et n'a pas de grosses limitations
de performances comme chez Render.

De plus, le mot d'ordre de l'outil se veut la simplicité. Exit la complexité de déploiement
d'une application. Pour ce faire, il utilise une méthode d'intégration de l'infrastructure
dans le code.

Alors certes, ça peut poser polémique dans le sens où le code source est alors fortement lié
au service d'hébergement. Mais dans le cas de Shuttle, le lien entre code et infra se fait 
avec de simples annotations facilement remplaçables dans le cadre d'une migration.

Ici, pas besoin de fichier de configuration pour Postgres ou Nginx, tout est automatiquement géré par le service.

Installation
============

L'installation de l'environnement de Shuttle se fait directement avec Cargo.
Après t'être connecté au site et avoir récupéré ta clé d'API, il te suffit d'exécuter
les 3 commandes suivantes pour avoir un hello-world déployé en Rust.


.. code-block:: bash

    cargo install cargo-shuttle
    cargo shuttle init --create-env
    cargo shuttle deploy

Tu peux alors choisir ton framework Rust préféré via le prompt, ici on va partir sur `Axum <https://github.com/tokio-rs/axum>`_.

Ultra simple !


Todos
=====

On va passer à un exemple un peu plus poussé avec une API pour une gestion d'une **TODO list**
avec une base de données **Postgres**.

Cargo.toml
----------

À partir du hello-world de base, on va ajouter la prise en charge de **Postgres** et de **Sqlx**
dans **Shuttle** via le package **shuttle-shared-db**.

.. code-block:: toml

    [package]
    name = "mon-app"
    version = "0.1.0"
    edition = "2021"

    [dependencies]
    axum = "0.7.3"
    serde = { version = "1.0.188", features = ["derive"] }
    shuttle-axum = "0.47.0"
    shuttle-runtime = "0.47.0"
    shuttle-shared-db = { version = "0.47.0", features = ["postgres", "sqlx"] }
    sqlx = "0.7.1"
    tokio = "1.28.2"


migrations/0001_init.sql
------------------------

On ajoute également un script de migration pour créer notre table dans la base de données :


.. code-block:: sql

    CREATE TABLE IF NOT EXISTS todos (
        id serial PRIMARY KEY,
        note TEXT NOT NULL
    );


src/models.rs
--------------

Tu peux désormais créer tes structures pour gérer ta table de Todo.
**Todo** correspond à l'objet de notre table, **TodoNew** sera utilisé pour la création d'un nouvel
item et **MyState** est utilisé pour gérer le pool Postgres.


.. code-block:: rust

    use serde::{Deserialize, Serialize};
    use sqlx::{FromRow, PgPool};

    #[derive(Deserialize)]
    pub struct TodoNew {
        pub note: String,
    }

    #[derive(Serialize, FromRow)]
    pub struct Todo {
        pub id: i32,
        pub note: String,
    }

    #[derive(Clone)]
    pub struct MyState {
        pub pool: PgPool,
    }

src/main.rs
-----------

Place à notre API.

Tu remarqueras que l'intégration avec Shuttle se fait simplement via les annotations **#[shuttle_runtime::main]** pour déclarer notre application principale,
**#[shuttle_shared_db::Postgres] pool: PgPool** pour la connexion à notre base de données Postgresql et **shuttle_axum::ShuttleAxum** pour indiquer qu'on utilise le framework Axum. 

.. code-block:: rust

    #[shuttle_runtime::main]
    async fn main(#[shuttle_shared_db::Postgres] pool: PgPool) -> shuttle_axum::ShuttleAxum {
    ...
    }

Tu vois, quand je te disais que l'intégration à l'infrastructure était ultra simple !

Et voilà, on passe enfin sur l'écriture de nos routes. On va pouvoir ajouter, lire, lister
et supprimer nos TODOs.

.. code-block:: rust

    use axum::{
        extract::{Path, State},
        http::StatusCode,
        response::IntoResponse,
        routing::{delete, get, post},
        Json, Router,
    };
    use sqlx::PgPool;

    mod models;
    use models::{Todo, TodoNew, MyState};

    // Add a function to retrieve all todos
    async fn retrieve_all(
        State(state): State<MyState>,
    ) -> Result<impl IntoResponse, impl IntoResponse> {
        match sqlx::query_as::<_, Todo>("SELECT * FROM todos")
            .fetch_all(&state.pool)
            .await
        {
            Ok(todos) => Ok((StatusCode::OK, Json(todos))),
            Err(e) => Err((StatusCode::BAD_REQUEST, e.toString())),
        }
    }

    async fn retrieve(
        Path(id): Path<i32>,
        State(state): State<MyState>,
    ) -> Result<impl IntoResponse, impl IntoResponse> {
        match sqlx::query_as::<_, Todo>("SELECT * FROM todos WHERE id = $1")
            .bind(id)
            .fetch_one(&state.pool)
            .await
        {
            Ok(todo) => Ok((StatusCode::OK, Json(todo))),
            Err(e) => Err((StatusCode::BAD_REQUEST, e.toString())),
        }
    }

    async fn add(
        State(state): State<MyState>,
        Json(data): Json<TodoNew>,
    ) -> Result<impl IntoResponse, impl IntoResponse> {
        match sqlx::query_as::<_, Todo>("INSERT INTO todos (note) VALUES ($1) RETURNING id, note")
            .bind(&data.note)
            .fetch_one(&state.pool)
            .await
        {
            Ok(todo) => Ok((StatusCode::CREATED, Json(todo))),
            Err(e) => Err((StatusCode::BAD_REQUEST, e.toString())),
        }
    }

    // function to remove a todo
    async fn remove(
        Path(id): Path<i32>,
        State(state): State<MyState>,
    ) -> Result<impl IntoResponse, impl IntoResponse> {
        match sqlx::query("DELETE FROM todos WHERE id = $1")
            .bind(id)
            .execute(&state.pool)
            .await
        {
            Ok(_) => Ok(StatusCode::NO_CONTENT),
            Err(e) => Err((StatusCode::BAD_REQUEST, e.toString())),
        }
    }


    #[shuttle_runtime::main]
    async fn main(#[shuttle_shared_db::Postgres] pool: PgPool) -> shuttle_axum::ShuttleAxum {
        sqlx::migrate!()
            .run(&pool)
            .await
            .expect("Failed to run migrations");

        let state = MyState { pool };
        let router = Router::new()
            .route("/todos", get(retrieve_all))
            .route("/todos", post(add))
            .route("/todos/:id", get(retrieve))
            .route("/todos/:id", delete(remove))
            .with_state(state);

        Ok(router.into())
    }

Tu relances alors ta commande **cargo shuttle deploy** pour avoir ton service en ligne !

Et si tu veux d'abord tester localement, tu lances **cargo shuttle run** et tu peux tester ton service avec **curl** directement :

.. code-block:: bash

    curl -X POST -H 'content-type: application/json' localhost:8000/todos --data '{"note":"My todo"}'
    # {"id":1,"note":"My todo"}

    curl localhost:8000/todos/1
    # {"id":1,"note":"My todo"}

    curl localhost:8000/todos
    # [{"id":1,"note":"My todo"}]

    curl -X DELETE localhost:8000/todos/1
    # []

Tu peux alors appeler ton backend Shuttle depuis ton frontend hébergé sur Netlify ou Vercel sans aucun problème.