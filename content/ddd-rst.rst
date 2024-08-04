Domain Driven Design en Rust
############################

:date: 2022-12-04
:tags: rust,ddd,domain,driven,design
:category: Rust
:slug: ddd-rust
:authors: Morgan
:summary: Domain Driven Design en Rust

.. image:: ./images/rust.png
    :alt: Rust
    :align: right


Domain Driven Design, quésaco ?
-------------------------------

Le Domain Driven Design, communément appelé DDD, est un paradigme de développement qui met l'accent sur la compréhension approfondie du domaine dans lequel ton application sera utilisée.

Tu peux donc imaginer des modèles de données et des algorithmes qui reflètent précisément les concepts et les relations qui existent dans ton domaine d'application.

Cela te permet, en théorie, de créer des logiciels plus clairs et plus faciles à comprendre pour les personnes du projet non techniques.

L'accent est alors mis sur la collaboration avec les experts du domaine pour obtenir leur avis et leur feedback, et permet donc de parler le même langage.

DDD en Rust
-----------

Tu dois d'abord comprendre toute la partie métier de ton appli pour pouvoir définir le domaine. Cette phase d'analyse et de compréhension est la plus importante et peut t'aider à résoudre les problèmes de manière plus efficace pour maintenir et faire évoluer ton application.

Ensuite, tu peux utiliser des structures en `Rust <https://rust-lang.org/>`_ pour représenter les concepts du domaine, ainsi que des fonctions pour manipuler ces structures.


Exemple d'application de gestion de compte bancaire.
-----------------------------------------------------

Voici un exemple de code en Rust qui utilise le DDD pour gérer un compte bancaire :

.. code-block:: rust

    use chrono::{DateTime, Utc};

    struct Account {
        balance: u64,
        transactions: Vec<Transaction>,
    }

    struct Transaction {
        amount: u64,
        date: DateTime<Utc>,
    }

    struct Client {
        name: String,
        accounts: Vec<Account>,
    }

    impl Account {
        fn deposit(&mut self, amount: u64) {
            self.balance += amount;
            self.transactions.push(Transaction {
                amount,
                date: Utc::now(),
            });
        }

        fn withdraw(&mut self, amount: u64) -> Result<(), &'static str> {
            if self.balance >= amount {
                self.balance -= amount;
                self.transactions.push(Transaction {
                    amount,
                    date: Utc::now(),
                });
                Ok(())
            } else {
                Err("Insufficient funds")
            }
        }
    }

    fn main() {
        let mut client = Client {
            name: "John Doe".to_string(),
            accounts: vec![Account {
                balance: 0,
                transactions: vec![],
            }],
        };

        client.accounts[0].deposit(100);
        client.accounts[0].withdraw(50).unwrap();
        client.accounts[0].withdraw(50).unwrap();
    }

Ce code utilise des structures pour représenter les concepts du domaine (compte bancaire, transaction et client), ainsi que des fonctions pour manipuler ces structures (dépôt, retrait, etc.).


Exemple plus avancé : un système de gestion de stock.
-----------------------------------------------------

Voici un exemple de code Rust plus avancé qui utilise le DDD pour gérer un système de gestion de stock :

.. code-block:: rust

    use chrono::{DateTime, Utc};
    use std::collections::HashMap;

    // Représente un produit dans le stock
    #[derive(Clone, Debug)]
    struct Product {
        // Nom du produit
        name: String,
        // Quantité en stock
        quantity: u32,
        // Prix de vente
        price: f32,
    }

    // Représente un client dans le système
    #[derive(Clone, Debug)]
    struct Customer {
        // Nom du client
        name: String,
        // Adresse email du client
        email: String,
    }

    // Représente une commande dans le système
    #[derive(Clone, Debug)]
    struct Order {
        // Identifiant unique de la commande
        id: u32,
        // Produits commandés
        products: Vec<Product>,
        // Client qui a passé la commande
        customer: Customer,
        // Date de la commande
        date: DateTime<Utc>,
    }

    // Représente un système de gestion de stock
    #[derive(Debug)]
    struct StockSystem {
        // Produits en stock
        products: HashMap<String, Product>,
        // Clients enregistrés dans le système
        customers: HashMap<String, Customer>,
        // Commandes enregistrées dans le système
        orders: Vec<Order>,
    }

    impl StockSystem {
        // Ajoute un produit au stock
        fn add_product(&mut self, product: Product) {
            self.products.insert(product.name.clone(), product);
        }

        // Ajoute un client au système
        fn add_customer(&mut self, customer: Customer) {
            self.customers.insert(customer.email.clone(), customer);
        }

        // Passe une commande pour un client donné
        fn place_order(&mut self, products: Vec<Product>, customer_email: &str) -> Result<Order, &'static str> {
            // Vérifie si les produits demandés sont en stock
            for product in &products {
                let stock_product = self.products.get(&product.name);
                if stock_product.is_none() || stock_product.unwrap().quantity < product.quantity {
                    return Err("Product out of stock");
                }
            }

            // Vérifie si le client existe dans le système
            let customer = self.customers.get(customer_email);
            if customer.is_none() {
                return Err("Customer not found");
            } else {
                // Réduit la quantité en stock pour les produits commandés
                for product in &products {
                    let mut stock_product = self.products.get_mut(&product.name).unwrap();
                    stock_product.quantity -= product.quantity;
                }

                // Crée la commande
                let order = Order {
                    id: self.orders.len() as u32 + 1,
                    products,
                    customer: customer.unwrap().clone(),
                    date: Utc::now(),
                };

                // Ajoute la commande au système
                self.orders.push(order.clone());

                Ok(order)
            }
        }
    }


Pour utiliser ce code, tu peux créer une instance de la structure StockSystem et ajouter des produits, des clients et passer des commandes :


.. code-block:: rust

    fn main() {
        // Crée une instance du système de stock
        let mut stock_system = StockSystem {
            products: HashMap::new(),
            customers: HashMap::new(),
            orders: Vec::new(),
        };

        // Ajoute des produits au stock
        stock_system.add_product(Product {
            name: "Table".to_string(),
            quantity: 10,
            price: 100.0,
        });
        stock_system.add_product(Product {
            name: "Chair".to_string(),
            quantity: 20,
            price: 50.0,
        });

        // Ajoute des clients au système
        stock_system.add_customer(Customer {
            name: "John Doe".to_string(),
            email: "john.doe@example.com".to_string(),
        });
        stock_system.add_customer(Customer {
            name: "Jane Doe".to_string(),
            email: "jane.doe@example.com".to_string(),
        });


        // Passe une commande pour un client
        let order = stock_system.place_order(vec![
            Product {
                name: "Table".to_string(),
                quantity: 1,
                price: 100.0,
            },
            Product {
                name: "Chair".to_string(),
                quantity: 2,
                price: 50.0,
            },
        ], "jane.doe@example.com").unwrap();

        println!("Order placed: {:?}", order);

        // Affiche les informations du système
        println!("Stock system: {:?}", stock_system);
    }


Avantages et défis 
------------------

En utilisant le DDD dans tes projets, tu peux bénéficier de nombreux avantages, tels que :

* Des logiciels plus clairs et plus faciles à comprendre, ce qui peut améliorer la collaboration avec les autres développeurs et les experts du domaine.
* Des modèles de données et des algorithmes qui reflètent les concepts et les relations du domaine d'application, ce qui peut améliorer la qualité de ton code et la précision de tes résultats.
* Un code plus facile à maintenir et à évoluer, ce qui peut réduire les coûts de développement et accélérer les délais de mise sur le marché.

Cependant, le DDD peut également présenter des défis, tels que :

* La nécessité de comprendre en profondeur le domaine d'application, ce qui peut être difficile et prendre du temps pour les développeurs qui ne sont pas des experts du domaine.
* L'intégration du DDD dans un projet existant peut être complexe et perturbante pour le fonctionnement de l'application.
* La mise en place d'un processus de développement orienté domaine peut nécessiter des changements importants dans la façon dont les équipes de développement travaillent, ce qui peut être difficile à gérer.