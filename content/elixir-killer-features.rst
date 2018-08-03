Les killer features d'Elixir
############################

:date: 2018-08-03
:tags: elixir,killer,features
:category: Elixir
:slug: elixir-killer-features
:authors: Morgan
:summary: Les killer features d'Elixir

.. image:: ./images/elixir.png
    :alt: Elixir
    :align: right


Ça fait un petit moment que j'ai dans l'idée de bosser un langage fonctionnel, histoire d'améliorer mes compétences de dev
en m'entrainant à réfléchir autrement. *Haskell* m'attirait beaucoup, car il semblait représenter la perfection du paradigme fonctionnel.
Mais bon, il faut vraiment prendre le temps de s'y investir, et il n'est pas simple de l'utiliser rapidement pour nos petits *use-cases* quotidiens.

Quand aux langages de type *Lisp*, c'est intéressant et rigolo mais utiliser des milliers de parenthèses partout, très peu pour moi (ok je sais, c'est cliché mais c'est comme ça).

C'est alors que plusieurs langages dits modernes fîrent leur apparition, comme *Go*, *Rust*, *Elixir* et *Crystal*.
Et j'ai dans mon entourage des devs qui ont fait le cheminement suivant : 

*Python -> Go -> Elixir*

Après avoir entendu beaucoup de bien d'`Elixir <https://elixir-lang.org/>`_, j'ai décidé de m'y mettre et je ne suis pour l'instant pas déçu !

Du coup, j'avais envie de te montrer les quelques *killer features* d'*Elixir* pour un dev qui vient principalement du monde *Python* à la base.

Pour la petite histoire, c'est un langage inventé par un ancien dev de *Ruby on Rails*, donc on a droit une syntaxe toute mimi.
Et ça tourne sur la VM *Erlang*, qui est réputée comme étant très performante en programmation concurrente.

Compréhension
-------------

Alléluia, on a les listes et dictionnaires compréhensions. Comme tout *pythoneux* qui se respecte, ça fait plaisir de voir ça ici !

En *Python*, on écrirait par exemple une petite liste compréhension de cette manière :

.. code-block:: python

    >>> myList = [x * x for x in [1, 2, 3, 4] if x > 2]
    >>> myList
    [9, 16]

En *Elixir*, ça donne ça :

.. code-block:: elixir

    iex> myList = for x <- 1..4, x > 2, do: x * x
    [9, 16]


Et pour faire un dictionnaire compréhension à partir d'une liste, en *Python* on ferait ça :

.. code-block:: python

    >>> myDict = {x: x**2 for x in [1, 2, 3, 4] if x % 2 == 0}
    >>> myDict
    {2: 4, 4: 16}


En *Elixir*, ça donne ça :

.. code-block:: elixir

    iex> myDict = for x <- 1..4, rem(x, 2) == 0, into: %{}, do: {x, x * x}
    %{2 => 4, 4 => 16}


Tu remarqueras qu'*Elixir* utilise le typage dynamique comme en *Python*, du coup on peut avoir un syntaxe assez concise.


Fonction anonyme
----------------

Dans *Elixir*, on a droit aux fonctions anonymes, qui sont beaucoup plus poussées que les lambdas de *Python*.

En *Python*: 

.. code-block:: python

    >>> add = lambda a, b: a + b
    >>> add(3, 4)
    7

En *Elixir* :


.. code-block:: elixir

    iex> add = fn a, b -> a + b end     
    iex> add.(3, 4)
    7

Ici on a un exemple relativement simple, mais sache que tu n'as pas de limitation de syntaxe dans les fonctions anonymes d'*Elixir*.

Il s'agit également de *closures*, donc elles ont accès aux variables du *scope*. Tu remarqueras la syntaxe **.(** pour l'appel de la fonction.
C'est une volonté d'*Elixir* de différencier les appels des fonctions anonymes par rapport au appels des fonctions normales.



Pattern matching
----------------

Sûrement le plus gros point fort de ce langage, ce qui le rend unique. Le symbole **=** ne sert non pas à assigner une variable, mais à faire du *pattern matching*.

En effet, pour faire simple, en *Elixir* lorsque tu fais **x = 1**, le langage essaye de *matcher* l'expression de droite avec celle de gauche.
On pourra voir l'assignation de la variable x comme une conséquence de ce *pattern matching*.

Ça permet de faire tout un tas de choses, par exemple :

.. code-block:: elixir

    iex> {a, b, c} = {:hello, "world", 42}
    {:hello, "world", 42}
    iex> a
    :hello
    iex> b
    "world"   

Tu remarqueras le **:hello**, qui est en réalité un *atom*. C'est en gros une constante qui porte comme nom de variable sa valeur. les **true** et **false** du langage
sont des *atoms* par exemple.

Pour récupérer le *head* et le *tail* d'une liste via le *pattern matching* :

.. code-block:: elixir

    iex> [head | tail] = [1, 2, 3]
    [1, 2, 3]
    iex> head
    1
    iex> tail
    [2, 3]

Mais là où c'est vraiment fort, c'est que ce *pattern matching* fonctionne également pour les arguments des fonctions.
Et on va alors pouvoir écrire une fonction qui va se comporter différemment en fonction des arguments d'entrée.
Ça peut faire penser à *Java*, mais via le *pattern matching*, c'est vraiment plus puissant.

On imagine ici une fonction que se comporterait différemment en fonction du *JSON* qu'elle a reçu par exemple.
Ici, on effectue des répartions différentes selon le véhicule passé en entrée.


.. code-block:: elixir

    iex> defmodule Garage do
             def repair(%{"voitures" => %{ "marque" => "peugeot"}}) do
                 IO.puts("on traite les voitures peugeots")
             end
             def repair(%{"motos" => %{ "couleur" => "rouge"}}) do
                 IO.puts("on traite les motos rouges")
             end
             def repair(_) do
                 IO.puts("on traite le reste")
             end
         end

    iex> Garage.repair(%{
             "voitures" => %{
                "marque" => "peugeot",
                "roues" => 4,
                "couleur" => "rouge"
             }
         })
    on traite les voitures peugeots

    iex> Garage.repair(%{
             "motos" => %{
                 "marque" => "ducati",
                 "roues" => 2,
                 "couleur" => "rouge"
             }
         })
    on traite les motos rouges

    iex> Garage.repair(%{
             "motos" => %{
                 "marque" => "derbi",
                 "roues" => 2,
                 "couleur" => "noir"
             }
         })
    on traite le reste


Plutôt sympa nan ? Ça peut nous éviter pas mal de bloc type *if ... else* ce genre de syntaxe !

Pipe
-------

L'opérateur unix ultime, qui manque cruellement à *Python*, est bien présent dans Elixir !

Tu peux du coup faire ce genre de truc :


.. code-block:: elixir

    iex> "i love elixir" |> String.split |> Enum.take(-1) |> Enum.join(" ") |> String.capitalize
    "Elixir"


Processus
---------


On en vient à ce qui permet à Elixir d'avoir des performances de malade. Elixir gère la concurrence à travers des processus internes.
Alors attention, ça n'a rien à voir avec les processus systèmes. C'est un fonctionnement interne à la VM *Erlang*, on peut donc en avoir des millions 
sans que ça pose problème au niveau de la machine.

Pour ce faire, on a juste 3 mots clés à retenir : **spawn**, **send** et **receive**.

Avec **spawn**, on lance un nouveau processus, tandis que **send** et **receive** vont servir à envoyer et reçevoir des 
messages à travers les processus.


Ça ressemble un peu au système de *goroutines* de *Go*. On pourrait voir le mot clé **spawn** équivalent au mot clé **go** de *Go*,
et le système **send**/**receive** comme le système de channel de *Go*.


.. code-block:: elixir

    iex> parent = self()
    #PID<0.41.0>
    iex> spawn fn -> send(parent, {:hello, self()}) end
    #PID<0.48.0>
    iex> receive do
    ...>   {:hello, pid} -> "Got hello from #{inspect pid}"
    ...> end
    "Got hello from #PID<0.48.0>"

Dans cet exemple, on a notre processus parent qui reçoit un message du processus 48 qui a été *spawné*.



Bonus
-----

En bonus, on a également droit à tout ce qui vient du monde des langages fonctionnels, à savoir l'immutabilité, les *closures*,
les fonctions d'ordre supérieur, la récursivité à la place des boucles *for*, les fonctions pures etc ...

Voilà, j'espère t'avoir donné envie de t'intéresser à cet excellent langage ! Et ce n'est qu'un bref aperçu de toutes ses possibilités !