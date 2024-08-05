Shuttle.rs : Déploiement d'un frontend
######################################

:date: 2024-08-01
:tags: shuttle, shuttle.rs, rust, devops, server, deploy, deployment, ci, cd, integration
:category: Rust
:slug: shuttle-rs-frontend
:authors: Morgan
:summary: Shuttle.rs : Déploiement d'un frontend

.. image:: ./images/shuttle.png
    :alt: Shuttle
    :align: right

Petit article rapide qui fait suite au `déploiement d'un backend <https://dotmobo.xyz/shuttle-rs.html>`_ en Rust avec `Shuttle <https://www.shuttle.rs/>`_.

Après avoir créé ton API pour ton application de TODOs avec Axum, tu vas pouvoir y ajouter un petit frontend sympa également déployé sous Shuttle pour tester tout ça.

J'hésitais entre partir sur une solution de création de frontend en Rust type `Leptos <https://leptos.dev/>`_ ou `Yew <https://yew.rs/>`_, mais ces outils feront l'objet d'articles futurs.
Pour rester ultra simple, tu peux partir sur `AlpineJS <https://alpinejs.dev/>`_ pour la gestion des composants JS et sur `Picocss <https://picocss.com/>`_ pour styliser un peu tout ça.

Tu reprends ton code Axum, et on commence par y ajouter notre page html.

Tu peux créer un fichier **templates/index.html** de cette manière :


.. code-block:: html

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>TODO App</title>
        <link rel="stylesheet" href="https://unpkg.com/@picocss/pico@1.4.0/css/pico.min.css">
        <script src="https://unpkg.com/alpinejs" defer></script>
    </head>
    <body>
        <main class="container" x-data="todoApp()">
            <h1>TODO App</h1>

            <form @submit.prevent="addTodo">
                <input type="text" x-model="newTodo" placeholder="Add a new todo" required>
                <button type="submit">Add</button>
            </form>

            <ul>
                <template x-for="todo in todos" :key="todo.id">
                    <li>
                        <span x-text="todo.note"></span>
                        <button @click="removeTodo(todo.id)" class="secondary">Delete</button>
                    </li>
                </template>
            </ul>
        </main>

        <script>
            function todoApp() {
                return {
                    todos: [],
                    newTodo: '',

                    async fetchTodos() {
                        const response = await fetch('/todos');
                        this.todos = await response.json();
                    },

                    async addTodo() {
                        const response = await fetch('/todos', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ note: this.newTodo })
                        });
                        const todo = await response.json();
                        this.todos.push(todo);
                        this.newTodo = '';
                    },

                    async removeTodo(id) {
                        await fetch(`/todos/${id}`, {
                            method: 'DELETE'
                        });
                        this.todos = this.todos.filter(todo => todo.id !== id);
                    },

                    async init() {
                        await this.fetchTodos();
                    }
                };
            }
        </script>
    </body>
    </html>

Tu as donc AlpineJS qui va se charger de lister les TODOs et de mettre à jour l'UI lorsque tu en ajoutes ou que tu en effaces. Les appels HTTP sont directement gérés avec **fetch**.

Picocss stylise automatiquement ton formulaire et tes boutons.

Ensuite, on va modifier le fichier **src/main.rs** pour que Axum expose notre **index.html** lors de l'appel de la racine du site.


.. code-block:: rust

    use axum::{
        extract::{Path, State},
        http::StatusCode,
        response::{Html, IntoResponse},
        routing::{delete, get, post},
        Json, Router,
    };
    use sqlx::PgPool;
    use tokio::fs::read_to_string;

    mod models;
    use models::{Todo, TodoNew, MyState};

    ...

    async fn serve_index() -> impl IntoResponse {
        match read_to_string("templates/index.html").await {
            Ok(html) => Html(html).into_response(),
            Err(_) => (StatusCode::INTERNAL_SERVER_ERROR, "Failed to load HTML file").into_response(),
        }
    }

Et voilà ! Tu peux redéployer ton application en prod avec **cargo shuttle deploy** et profiter de ta petite interface graphique !

Le résultat complet est disponible sur `mon dépôt github <https://github.com/dotmobo/todos-shuttle>`_.
