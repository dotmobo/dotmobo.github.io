
Man vs. Wild: Angular
##############################

:date: 2020-05-21
:tags: frontend,angular,rxjs
:category: Frontend
:slug: man-vs-wild-angular
:authors: Morgan
:summary: Angular

Ah Angular, sujet de débat éternel pour tous les trolls des technos front. Ce framework est soit détesté, soit adulé, mais on est rarement dans la nuance. Pour le coup je botte un peu en touche, car mes sentiments à l'égard d'Angular font office de montagnes russes. Après m'être battu pendant 2 ans avec ce framework pour un projet pro, j'avais envie de te faire un petit retour des choses que j'aurai aimé savoir dès le début et sur comment s'en sortir avec cette stack et ses concepts.

Editeur
=======
De ce que j'ai pu tester, l'éditeur le plus simple à prendre en main pour angular est VS Code (https://code.visualstudio.com/).
Au niveau des plugins, j'ai bien aimé les suivants :
- Angular 8 Snippets (https://marketplace.visualstudio.com/items?itemName=Mikael.Angular-BeastCode) : Snippets pour angular, material, ngrx
- Prettier (https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode) : pour le formatage du code
- Tsint (https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-typescript-tslint-plugin) : le linter typescript
- Bracket Pair Colorizer (https://marketplace.visualstudio.com/items?itemName=CoenraadS.bracket-pair-colorizer) : pour s'en sortir avec les parenthèses
J'ai un peu testé Intellij, Atom et Vim, mais je suis vite retourné sur VS Code.

Rxjs
====

On attaque directement avec le plus important. Rxjs est une libraire de reactive programming permettant de travailler avec des fluxs de données asynchrones. Il faut savoir que Angular repose complètement sur cette librairie et qu'il est absolument vital de la maitriser. Toute la technicité du code va en grande partie dépendre de Rxjs.

Opérateurs
----------
Il faut absolument en maitriser les principaux opérateurs comment switchMap, combineLatest, filter, debounce et autres.
Si ce n'est pas déjà fait, commence par aller ici (https://www.learnrxjs.io) et fait le tour des opérateurs, joue avec, essaye de les comprendre et de les garder en tête.

Subscribe/unsubscribe
---------------------
Un des premières grosses sources de bugs est d'oublier de se désabonner d'un flux. Ca fait des fuites de mémoires et ça a des effets de bord en cascade. Tu risque de te retrouver abonné à certains fluxs plusieurs fois inutilement et d'avoir des comportements étranges sans comprendre facilement d'où ça vient car c'est difficilement débuggable.

Si possible, évite d'utiliser le unsubscribe à la main et privilégie plutôt le déclenchement d'un signal de fin de flux, avec first() par exemple.

.. code-block:: javascript

    source.pipe(first()).subscribe(val => console.log(`First value: ${val}`));

Ici on récupère la première valeur de source et un signal de fin de flux est alors émis grace au first, ce qui nous désabonne sans le unsubscribe.

En second lieu, tu peux aussi privilégier l'abonnement directement dans le template via "monflux$ | async" car le désabonnement est géré par angular lorsque l'on quitte le composant :

.. code-block:: html
    
    <span>Wait for it... {{ greeting$ | async }}</span>
    

Enfin, si tu es obligé de rester abonné dans ton fichier typescript à un flux pour x raisons, n'oublie surtout pas de te désabonné dans l'event ngOnDestroy.

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

Dernier point, il faut également éviter de faire des subscribe dans des subscribe pour éviter des comportements non voulus.

Marble tests
------------
Il est possible de faire des tests unitaires plutôt poussés de tes fluxs avec des "marble tests". La doc (https://rxjs-dev.firebaseapp.com/guide/testing/marble-testing) est pas trop mal faite mais il faut savoir que c'est pas forcément évident.
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
En angular, les resolvers sont des fonctions qui permette de récupérer des données d'une api avant d'afficher une page. Il est intéressant de savoir qu'il est possible de gérer facilement du cache avec l'opérateur shareReplay de rxjs.

.. code-block:: javascript

TODO mettre exemple avec sharereplay de 1h

Ici, le resolver récupère la première requête et la met en cache pendant 1h. Pratique pour éviter de faire des appels systématiques !


Store
=====
L'utilisation d'un store type redux pour Angular est très intéressant pour les gros projets. Ca permet de débugger plus facilement l'application et ça facilite l'intéraction entre plusieurs pages en partageant les données. Le store le plus utilisé par la communauté est Ngrx (https://ngrx.io/), donc je t'invite à partir sur celui-là si tu n'a pas de préférence particulière. Potasse un peu la doc officielle pour comprendre le fonctionnement (https://ngrx.io/guide/store). Après rxjs, c'est le deuxième indispensable.

Debug
-----
L'outil de debug indispensable est le Redux Devtools (https://chrome.google.com/webstore/detail/redux-devtools/lmhkpmbekcpmknklioeibfkpmmfibljd?hl=fr). Ca va te pemettre de visualiser ton store en direct et de lancer des actions manuellement.

Facade
------
Plutôt que de manipuler directement le store dans les composants, je te conseille d'utiliser un service angular qui va s'en charger. Dans ce service, tu vas mettre tes appels aux selectors, les dispatchs de tes actions et autres. C'est une manière d'utiliser le design pattern facade. Tu peux jeter un oeil à cette article où c'est bien expliqué (https://medium.com/@thomasburlesonIA/ngrx-facades-better-state-management-82a04b9a1e39). Concretement ta facade va ressembler à ça :


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
        
Et c'est donc ce service que tu vas injecter dans tes composants plutot que le store directement ! Ca permet de garder des composants plus lisible, et d'isoler la partie store. Si un jour tu migres de technos de store, il te suffira de modifier les facades.

Forms
-----
Il est possible de gérer nos formulaires angular directement dans le store ngrx. C'est vraiment très pratique si tu dois faire une application avec beaucoup de formulaire complexe. Ca facilite grandement le debug des formulaires et on a une manière propre de les utiliser. Cette librairie s'appelle ngrx-forms (https://ngrx-forms.readthedocs.io/) et est vraiment au top !

Error thrown
-------------
j'en ai fait des cauchemars de celle-là. Si tu fais des tests unitaires pour ton application angular, tu risques de la rencontrer souvent. Elle peut survenir aléatoirement, c'est dur à débugguer, un horreur. Mais en gros, après s'être arraché les cheveux, si tu as une erreur de ce type qui survient à l'exécution des tests unitaires, c'est qu'il te manque dans 99% des cas l'importation et l'initialisation de ton store quelques part dans un des tests.

UI
==

Niveau UI, tu peux partir sur la librairie de composants Angular Material (https://material.angular.io/). Elle a l'avantage d'être open source et d'être officiellement suppoorté par Angular.

Material
--------
Quand tu as des doutes sur l'utilisation de tes composants material, n'hésite pas à te référer à la documentation officielle de google sur material, c'est une mine d'or : https://material.io/

Theme
-----
Il est possible de faire son propre theme, voir ici (https://material.angular.io/guide/theming#defining-a-custom-theme).
Et de la même manière, tu peux également thémer tes propres composants customisés voir ici (https://material.angular.io/guide/theming-your-components)

Angular
=======
On finit sur les tips internes à Angular.

i18n
----
Avec le module i18n de Angular, il est possible d'internationaliser les templates. Oui. Mais il faut savoir qu'il ne permet pas d'internationaliser les chaines de caractères en dehors de ces templates ! C'est une demande qui est ouverte depuis 4 ans (cf: https://github.com/angular/angular/issues/11405) et qui n'a toujours pas été résolu. Donc il faut soit prendre son mal en patience, soit utiliser une librairie externe pour l'internationalisation, ou alors gérer ça dans le code à la main. Franchement, en comparaison d'autres framework, l'internationalisation dans Angular n'est franchement pas terrible. Et en plus il faut se taper des fichiers xml ...

Schematics
----------
Les schematics sont les templates utilisés par le angular cli pour généré les composants, les modules et autres. C'est pratique à utiliser, par contre c'est une horreur à écrire. Franchement, ne pert pas de temps à en créer des customs, ça ne te servira pas à grand chose au final ...

Lazy loading
-------------
Pour gagner en performance, il faut savoir qu'il est possible de découper son application en plusieurs sous modules lazy loadé (https://angular.io/guide/lazy-loading-ngmodules). Ca permet à l'application de répondre rapidement lorsque l'on va sur la page d'accueil, et ne charger les modules nécessaires que lorsqu'ils sont vraiment utiles. Il suffit de déclarer nos modules à lazy loader de cette manière dans le fichier de routing :


.. code-block:: javascript

        const routes: Routes = [
          {
            path: 'items',
            loadChildren: () => import('./items/items.module').then(m => m.ItemsModule)
          }
        ];





