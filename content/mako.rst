Templating avec Mako
####################

:date: 2015-12-23
:tags: template,templating,python,mako,jinja,django
:category: Python
:slug: mako
:authors: Morgan
:summary: Templating avec mako

.. image:: ./images/mako.png
    :alt: Mako
    :align: right

*Python is a great scripting language. Don't reinvent the wheel...
your templates can handle it !*

Je suis tombé sur `mako <http://www.makotemplates.org/>`_ suite à une discussion
mouvementée au sujet de `django <https://www.djangoproject.com/>`_ et de
`jinja <http://jinja.pocoo.org/>`_ avec un de mes collègues pro
`groovy <http://www.groovy-lang.org/>`_/`grails <https://grails.org/>`_.

Ça devait ressembler à quelque-chose comme ça:

| *- Rhhaaa je déteste jinja, j'suis obligé d'me taper la doc pour apprendre toute la syntaxe! En plus c'est grave limité! Y a pas moyen d'y écrire directement du python ?*
| *- Bah ça va, c'est pas trop compliqué, et si t'as besoin d'utiliser des méthodes python, tu peux utiliser les custom filters et custom tags!*
| *- Uai mais c'est pas super pratique, avec grails tu peux directement mettre du groovy dans tes templates, c'est génial blablabla*
| *- Ok ok j'ai compris, jinja te convient pas, mais j'suis sûr que ce que tu cherches existe dans la communauté python! Voyons voir ... regardes, y a un truc là, ça s'appelle mako!*
| *- *Yeux qui brillent**
|

Mako est un moteur de template utilisé dans le framework
`pyramid <http://www.pylonsproject.org/>`_, à l'instar de jinja utilisé dans django.
Il est réputé pour sa performance, et est même utilisé pour l'affichage des pages
de `reddit <https://www.reddit.com/>`_!

Mais son principal atout est de pouvoir utiliser directement du python à l'aide
des balises **<% %>** dans les templates.

Certains diront que c'est pas génial, car on peut vite obtenir des templates
assez crades avec tout et n'importe quoi dedans.
D'autres diront que ça ne sert à rien d'inventer une nouvelle syntaxe spécifique
aux templates, alors que python est disponible et peut faire ça très bien.

Pour te faire ton propre avis, installes-le via pip:

.. code-block:: bash

    pip install mako

En résumé, tes templates ressembleront à ça:

.. code-block:: python

    <%inherit file="base.html"/>
    <%
        rows = [[v for v in range(0,10)] for row in range(0,10)]
    %>
    <table>
        % for row in rows:
            ${makerow(row)}
        % endfor
    </table>

    <%def name="makerow(row)">
        <tr>
        % for name in row:
            <td>${name}</td>\
        % endfor
        </tr>
    </%def>


La syntaxe de mako est très bien expliquée dans la
`doc officielle <http://docs.makotemplates.org/en/latest/syntax.html>`_,
mais pour faire simple :

* La substitution d'expressions utilise le symbole **${}**, à la manière de perl.
* Tu disposes de `filtres <http://docs.makotemplates.org/en/latest/filtering.html>`_ comme sous jinja, via une syntaxe type **${"this is some text" | u}**
* Il y a les structures de contrôle classiques **% if** et **% else** et les boucles avec **% for**.
* Divers tags sont disponibles comme **<%inhérit/>**, **<%page/>**, **<%include/>**, etc ...
* Tu peux rajouter des commentaires avec **##**.
* Enfin, tout ce qui se trouve entre **<% %>** est du python. Tu peux profiter de toute la syntaxe de python et même importer des libs. C'est la fête !

Et pour l'utiliser, rien de plus simple, tu utilises la classe **Template** :

.. code-block:: python

    from mako.template import Template

    mytemplate = Template("hello, ${name}!")
    print(mytemplate.render(name="jack"))


Tu peux désormais utiliser mako pour gérer tes pages html! Et si tu es un
utilisateur de django, il t'es même possible de remplacer jinja par mako via
`django-mako-plus <https://github.com/doconix/django-mako-plus>`_.

En dehors des pages html, tu peux également l'utiliser `pour générer d'énormes
fichiers XML simples <http://stackoverflow.com/questions/3049188/generating-very-large-xml-files-in-python>`_,
comme une liste d'utilisateurs par exemple.
Ça évite de manipuler le DOM en mémoire comme avec `lxml <http://lxml.de/>`_,
c'est plus facile d'accès que `SAX <https://docs.python.org/3/library/xml.sax.html>`_,
et c'est très performant :

.. code-block:: python

    from mako.template import Template
    from mako.runtime import Context

    tpl_xml = '''
    <doc>
    % for i in data:
    <p>${i}</p>
    % endfor
    </doc>
    '''

    tpl = Template(tpl_xml)

    with open('output.xml', 'w') as f:
        ctx = Context(f, data=xrange(10000000))
        tpl.render_context(ctx)
