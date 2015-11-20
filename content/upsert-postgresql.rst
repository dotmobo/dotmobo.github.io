Upsert avec Postgresql
======================

:date: 2015-11-22
:tags: base de données,postgres,psql,postgresql
:category: Postgresql
:slug: upsert-postgresql
:authors: Morgan
:summary: Upsert avec Postgresql

.. image:: ./images/postgresql.png
    :alt: Postgresql
    :align: right

Lorsque l'on commence à `s'amuser avec asyncio <http://dotmobo.github.io/introduction-asyncio.html>`_
pour faire des traitements asynchrones sur une base `postgresql <http://www.postgresqlfr.org/>`_
avec `aiopg <https://github.com/aio-libs/aiopg>`_, on rencontre assez vite le problème des accès concurrents
à une ressource partagée.

Et notamment lorsqu'il s'agit d'appliquer de multiples *insert* ou *update*, appelés *upsert* dans le monde de *mongodb*.

Sous *mongodb* avec `pymongo <https://api.mongodb.org/python/current/>`_ c'est facile,
il suffit de passer le paramètre *upsert=True* à la méthode *update_one* :

.. code-block:: python

    >> from pymongo import MongoClient
    >> client = MongoClient()
    >> db = client.test_database
    >> db.test.update_one({'x': 1}, {'$inc': {'x': 3}}, upsert=True)

Mais sous *posgresql*, il n'existe pas de mot-clé *upsert*. Et c'est là que tu te demandes:

*"Comment faire un upsert en postgresql, tout en évitant les problèmes d'accès concurrents ?"*

Si tu n'es pas pressé, attends la sortie de postgresql 9.5 qui va inclure `la syntaxe du upsert <https://wiki.postgresql.org/wiki/What's_new_in_PostgreSQL_9.5#INSERT_..._ON_CONFLICT_DO_NOTHING.2FUPDATE_.28.22UPSERT.22.29>`_.

En imaginant une table qui ressemble à ça:

.. code-block:: sql

	SELECT username, logins FROM user_logins;

  	username | logins
 	----------+--------
  	James    |      4
  	Lois     |      2
 	(2 rows)

Et que tu veuilles ajouter deux nouveaux *logins*:

.. code-block:: sql

    INSERT INTO user_logins (username, logins)
    VALUES ('Naomi',1),('James',1);

En temps normal, tu auras cette erreur si le *username* existe déjà en base:

.. code-block:: sql

    ERROR:  duplicate key value violates unique constraint "users_pkey"
    DETAIL:  Key (username)=(James) already exists.

Et bien en 9.5, tu pourras gérer ça de cette manière:

.. code-block:: sql

	INSERT INTO user_logins (username, logins)
 	VALUES ('Naomi',1),('James',1)
	ON CONFLICT (username)
 	DO UPDATE SET logins = user_logins.logins + EXCLUDED.logins;

Génial non ?

*"Oui mais bon, de mon côté, en production, j'ai du postgresql 9.4 et c'est pas près de changer."*

Dans ce cas-là, je t'invite à lire `ce très bon article <http://www.depesz.com/2012/06/10/why-is-upsert-so-complicated/>`_
qui date un peu, mais qui résume très bien la situation.

Pour rester simple, l'idée est d'effectuer un *update* si l'entrée existe déjà ou un *insert* sinon.
Mais lors d'accès concurrents, il se peut très bien que l'entrée ait été ajoutée par un autre processus entre
ta tentative ratée d'*update* et ton *insert* qui suit. Et là, ça plante lamentablement.

Alors oui, il existe les *locks* et les transactions, mais çe n'est pas suffisant et ça peut poser certains problèmes.
Par exemple, *postgresql* stoppe une transaction en cours lorsqu'il rencontre une erreur.
Pour plus de détail, lis l'article que j'ai cité précédemment.

Du coup, la `solution admise par la communauté stackoverflow <http://stackoverflow.com/questions/1109061/insert-on-duplicate-update-in-postgresql?answertab=votes#tab-top>`_
est la suivante. Tu écris une fonction `pl/sql <https://fr.wikipedia.org/wiki/PL/SQL>`_ qui boucle sur le *update* ou *insert*, en utilisant l'exception *unique_violation*.
Du coup, cette fonction s'appelle à l'aide d'un seul *select*, donc pas besoin de *lock* ou de transaction:

.. code-block:: sql


    CREATE TABLE db (a INT PRIMARY KEY, b TEXT);

    CREATE FUNCTION merge_db(key INT, data TEXT) RETURNS VOID AS
    $$
    BEGIN
        LOOP
            -- first try to update the key
            -- note that "a" must be unique
            UPDATE db SET b = data WHERE a = key;
            IF found THEN
                RETURN;
            END IF;
            -- not there, so try to insert the key
            -- if someone else inserts the same key concurrently,
            -- we could get a unique-key failure
            BEGIN
                INSERT INTO db(a,b) VALUES (key, data);
                RETURN;
            EXCEPTION WHEN unique_violation THEN
                -- do nothing, and loop to try the UPDATE again
            END;
        END LOOP;
    END;
    $$
    LANGUAGE plpgsql;

    SELECT merge_db(1, 'david');
    SELECT merge_db(1, 'dennis');
