
Man vs. Wild: Angular
##############################

:date: 2020-05-21
:tags: frontend,angular,rxjs,typescript,javascript,framework,material,ngrx
:category: Frontend
:slug: man-vs-wild-angular
:authors: Morgan
:summary: Man vs. Wild: Angular

.. image:: ./images/angular.png
    :alt: Angular
    :align: right

Ah `Angular <https://angular.io/>`_... Sujet de débat éternel pour tous les trolls des technos front. Ce framework est soit détesté, soit adulé,
mais on est rarement dans la nuance. Pour le coup je botte un peu en touche, car mes sentiments à l'égard d'Angular font office de montagnes russes.
Et après m'être battu pendant 2 ans avec ce framework pour un projet pro, j'avais envie de te faire un petit retour des choses que j'aurai aimé savoir dès le début
pour m'en sortir avec cette stack et ses concepts.

Editeur
=======
De ce que j'ai pu tester, l'éditeur le plus simple à prendre en main pour Angular (et de loin) est `VS Code <https://code.visualstudio.com/>`_.
J'ai un peu testé Intellij, Atom et Vim, mais je suis très vite retourné sur VS Code.

Plugins
-------
Au niveau des plugins, mes quelques indispensables sont:

* `Angular 8 Snippets <https://marketplace.visualstudio.com/items?itemName=Mikael.Angular-BeastCode>`_: Snippets pour angular, material et ngrx.
* `Prettier <https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode>`_: Formatage automatique du code.
* `Tsint <https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-typescript-tslint-plugin>`_: Linter typescript.
* `Bracket Pair Colorizer <https://marketplace.visualstudio.com/items?itemName=CoenraadS.bracket-pair-colorizer>`_ : Pour s'en sortir avec les parenthèses !


Rxjs
====

On attaque directement avec le plus important. `Rxjs <https://rxjs-dev.firebaseapp.com/>`_ est une libraire de **reactive programming** permettant de travailler avec des
flux de données asynchrones. Il faut savoir que Angular repose complètement sur cette librairie et qu'il est absolument vital de la maîtriser. 
Toute la technicité du code va en grande partie dépendre de Rxjs.

Opérateurs
----------
Il faut absolument en **maitriser les principaux opérateurs** comme *switchMap*, *combineLatest*, *filter*, *debounce* et autres.
Si ce n'est pas déjà fait, commence par aller sur `learnrxjs.io <https://www.learnrxjs.io>`_ et fait le tour des opérateurs, joue avec, essaye de les comprendre et de les garder en tête.

Subscribe/unsubscribe
---------------------
Une des premières grosses sources de bugs est **d'oublier de se désabonner d'un flux**. Ça entraine des fuites de mémoires et ça produit des effets de bord en cascade. 
Tu risques de te retrouver abonné à certains flux plusieurs fois inutilement et d'avoir des comportements étranges sans comprendre facilement d'où ça vient.

Si possible, évite d'utiliser le *unsubscribe* à la main et privilégie plutôt le déclenchement d'un signal de fin de flux, avec **first()** par exemple.
Ici on récupère la première valeur du flux *source* et un signal de fin de flux est alors émis grace au *first()*, ce qui nous désabonne directement sans utiliser *unsubscribe*:

.. code-block:: javascript

    source.pipe(first()).subscribe(val => console.log(`First value: ${val}`));


En second lieu, tu peux aussi privilégier l'abonnement directement dans le template via **monflux$ | async**, car le désabonnement est alors géré automatiquement
par Angular lorsque l'on quitte le composant:

.. code-block:: html
    
    <span>Hello {{ myName$ | async }}</span>
    

Enfin, si tu es obligé de rester abonné à un flux dans ton fichier typescript pour x raisons, n'oublie surtout pas de te désabonner dans l'événement **ngOnDestroy**:

.. code-block:: javascript

    @Component({...})
    export class AppComponent implements OnInit, OnDestroy {
        subscription: Subscription 
        ngOnInit () {
            const timer$ = Rx.Observable.interval(500);
            this.subscription = timer$.subscribe(x => console.log(x));
        }
        ngOnDestroy() {
            this.subscription.unsubscribe()
        }
    }

Dernier point, il faut également **éviter de faire des subscribe dans des subscribe** car c'est pas très propre et ça peut entrainer des comportements non voulus.

Marble tests
------------
Il est possible de faire des tests unitaires plutôt poussés de tes flux avec des **marble tests**.
`La documentation officielle <https://rxjs-dev.firebaseapp.com/guide/testing/marble-testing>`_ est pas trop mal faite,
mais il faut savoir que c'est pas forcément évident à appréhender.

Pour info ca ressemble à ça:

.. code-block:: javascript
  
    import { TestScheduler } from 'rxjs/testing';

    const testScheduler = new TestScheduler((actual, expected) => {
      // asserting the two objects are equal
      // e.g. using chai.
      expect(actual).deep.equal(expected);
    });

    // This test will actually run *synchronously*
    it('generate the stream correctly', () => {
      testScheduler.run(helpers => {
        const { cold, expectObservable, expectSubscriptions } = helpers;
        const e1 =  cold('-a--b--c---|');
        const subs =     '^----------!';
        const expected = '-a-----c---|';

        expectObservable(e1.pipe(throttleTime(3, testScheduler))).toBe(expected);
        expectSubscriptions(e1.subscriptions).toBe(subs);
      });
    });
    
Resolver avec du cache
----------------------
En Angular, les *resolvers* sont des services qui permettent de récupérer des données d'une api avant d'afficher une page.
Il est intéressant de savoir qu'il est possible de gérer facilement du cache avec l'opérateur **shareReplay** de rxjs de cette manière:

.. code-block:: javascript

    import { Injectable } from '@angular/core';
    import { Resolve, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
    import { Observable } from 'rxjs';
    import { Country, NomenclatureService } from 'ins-common-lib';
    import { shareReplay } from 'rxjs/operators';

    @Injectable({
        providedIn: 'root'
    })
    export class PaysResolver implements Resolve<Country[]> {
        private pays$: Observable<Country[]>;

        constructor(private service: NomenclatureService) {}

        resolve(_route: ActivatedRouteSnapshot, _state: RouterStateSnapshot): Observable<Country[]> {
            if (!this.pays$) {
                this.pays$ = this.service.listCountries().pipe(shareReplay(1, 3600000));
            }
            return this.pays$;
        }
    }


Ici, le *resolver* récupère la première requête et la met en cache pendant 1h. Pratique pour éviter de faire des appels systématiques à l'api !


Store
=====
L'utilisation d'un **store type Redux** pour Angular est très intéressant pour les gros projets.
Ça permet de débugger plus facilement l'application et ça facilite l'intéraction entre plusieurs pages en partageant des données.
Le *store* le plus utilisé par la communauté est `Ngrx <https://ngrx.io/>`_, donc je t'invite à partir sur celui-là si tu n'a pas de préférences particulières.
Potasse un peu la `doc officielle <https://ngrx.io/guide/store>`_ pour en comprendre le fonctionnement.
Après rxjs, c'est la deuxième librairie qu'il est vital de maîtriser.

Debug
-----
L'outil de debug indispensable est le `Redux Devtools <https://chrome.google.com/webstore/detail/redux-devtools/lmhkpmbekcpmknklioeibfkpmmfibljd?hl=fr>`_.
Ça va te permettre de visualiser ton *store* en direct et de lancer des actions manuellement.

Facade
------
Plutôt que de manipuler directement le *store* dans les composants, je te conseille d'utiliser un service Angular qui va s'en charger.
Dans ce service, tu vas y mettre tes appels aux sélecteurs, l'éxecution de tes actions et autres. C'est une manière d'utiliser le **design pattern façade**.
Tu peux jeter un oeil à `cet article <https://medium.com/@thomasburlesonIA/ngrx-facades-better-state-management-82a04b9a1e39>`_ où c'est bien expliqué.
Concrètement ta façade va ressembler à ça :


.. code-block:: javascript

        @Injectable()
        export class CarsFacade {
          loaded$ = this.store.select(carsQuery.getIsLoaded);
          allCars$ = this.store.select(carsQuery.getAllCars);
          selectedCar$ = this.store.select(carsQuery.getSelectedCar);

          constructor(private store: Store<CarsState>) {}

          loadAllCars() {
            this.store.dispatch(new LoadCar());
          }

          selectCar(carId: string) {
            this.store.dispatch(new SelectCar(carId));
          }
        }
        
Et c'est donc ce service que tu vas injecter dans tes composants plutôt que le *store* directement !
Ça permet de garder des composants plus lisibles, et d'isoler la partie *store*. Si un jour tu migres de technos de *store*, il te suffira de modifier les façades.

Formulaires
-----------
Il est possible de gérer nos formulaires Angular directement dans le *store ngrx*.
C'est vraiment très pratique si tu dois faire une application avec beaucoup de **formulaires complexes**. Ça facilite grandement le debug des formulaires
et on a une manière propre de les créer. Cette librairie s'appelle `ngrx-forms <https://ngrx-forms.readthedocs.io/>`_ et est vraiment au top !

Error thrown
-------------
J'en ai fait des cauchemars de celle-là ! Si tu fais des tests unitaires pour ton application Angular, tu risques de la rencontrer souvent.
Elle peut survenir aléatoirement et c'est dur à débugguer, une horreur. Mais en gros, après m'être arraché les cheveux, si tu rencontre un **Error thrown**
à l'exécution de tes tests unitaires, c'est qu'il te manque dans 99% des cas **l'importation et l'initialisation de données de ton store** quelque part dans un des tests.

UI
==

Niveau UI, tu peux partir sur la librairie de composants `Angular Material <https://material.angular.io/>`_.
Elle a l'avantage d'être open source et d'être officiellement supportée par Angular.

Material
--------
Quand tu as des doutes sur l'utilisation de tes composants **material**, n'hésite pas à te référer à la `documentation officielle de google sur material <https://material.io/>`_, c'est une mine d'or.

Theme
-----
Il est possible de `faire ton propre theme <https://material.angular.io/guide/theming#defining-a-custom-theme>`_.
Et de la même manière, tu peux également `themer tes propres composants customisés <https://material.angular.io/guide/theming-your-components>`_.

Angular
=======
Allez on y est presque, place aux tips sur les mécaniques internes de Angular.

i18n
----
Avec le module i18n de Angular, il est possible d'internationaliser les templates.
Oui... mais il faut savoir qu'il **ne permet pas d'internationaliser les chaines de caractères en dehors des templates** !
C'est une demande qui est `ouverte depuis 4 ans <https://github.com/angular/angular/issues/11405>`_ et qui n'a toujours pas été résolue.
Donc il faut soit prendre son mal en patience, soit utiliser une librairie externe pour l'internationalisation, ou alors gérer ça dans le code à la main.

Franchement, en comparaison d'autres frameworks, l'internationalisation dans Angular n'est vraiment pas terrible. Et en plus il faut se taper des fichiers xml ...

Schematics
----------
Les *schematics* sont les templates utilisés par *angular cli* pour générer les composants, les modules et autres.
C'est pratique à utiliser, par contre c'est une horreur à écrire. Franchement, **ne perds pas de temps à en créer**, car ça ne te servira pas à grand chose au final.

Lazy loading
-------------
Pour gagner en performance, il faut savoir qu'il est possible de découper son application en plusieurs `sous-modules lazy loadés <https://angular.io/guide/lazy-loading-ngmodules>`_.
Ça permet à l'application de répondre rapidement lorsque l'on va sur la page d'accueil, et de charger les modules nécessaires que lorsqu'ils sont vraiment demandés par l'utilisateur.
Il suffit de déclarer nos modules de cette manière dans le fichier de *routing* :

.. code-block:: javascript

        const routes: Routes = [
          {
            path: 'items',
            loadChildren: () => import('./items/items.module').then(m => m.ItemsModule)
          }
        ];


Guards vs Resolvers
--------------------
La différence entre les deux concepts n'est pas toujours bien comprise, donc on va juste faire un petit point ici:

* Les *Guards* sont utilisés **pour autoriser ou non l'utilisateur à accéder à une page**. On va y faire des contrôles sur l'authentification et sur les autorisations.
* Les *Resolvers* sont utilisés pour **récupérer des données d'une api** nécessaire au bon fonctionnement d'un page, comme des nomenclatures ou autres.

Evite donc d'utiliser les *guards* pour récupérer des données qui n'ont rien à voir avec les autorisations !

Detection des changements
--------------------------

Si tu rencontre des soucis au niveau de la detection des changements, verifie que tu n'as pas une stratégie particulière type **ChangeDetectionStrategy.OnPush** sur ton composant.
Cette stratégie permet d'avoir de meilleurs performances mais risque de ne pas détecter les changements sur les variables en dehors des *inputs*.
Donc pour des petits composants qui fonctionnent uniquement à base de *input/output* c'est parfait, mais pour le reste il faut se méfier.

Librairies et workspaces
------------------------
Il y a quelques temps encore, il fallait installer et gérer *ng-packagr* à la main pour créer des libraires.
Aujourd'hui, c'est directement disponible via *angular cli*. Voici les commandes pour créer, tester, builder et publier une librairie :

.. code-block:: bash

    ng new my-workspace --create-application=false
    cd my-workspace
    ng generate library my-lib
    ng build my-lib
    ng test my-lib
    ng lint my-lib
    ng build my-lib --prod
    cd dist/my-lib
    npm publish

Il est également possible de créer un workspace qui va contenir plusieurs applications et librairies pour un même projet.

.. code-block:: bash

    ng new my-workspace --createApplication="false"
    cd my-workspace
    ng generate library my-first-lib
    ng generate library my-second-lib
    ng generate application my-first-app
    ng generate application my-second-app

C'est pratique dans le cas où tu aurais **plusieurs applications qui partagent des librairies communes**.
Par exemple, on pourrait imaginer une application pour les clients et une pour l'administration du site avec des modèles métier en commun dans une librarie partagée.


Mot de la fin
-------------
Et voilà, on a plus ou moins fait le tour de quelques tips que j'aurai bien aimé savoir en début de projet pour gagner du temps.
Si un de ces points a pu t'aider, n'hésite pas à en faire part dans les commentaires. Bon courage !