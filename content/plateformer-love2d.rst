Créer un petit jeu de plateforme avec Löve
##########################################

:date: 2021-03-19
:tags: jeux,video,lua,love2d,plateformer,itch
:category: Lua
:slug: plateformer-love2d
:authors: Morgan
:summary: Créer un petit jeu de plateforme avec Löve

.. image:: ./images/love.png
    :alt: Löve
    :align: right

On fait suite au précédent post du blog qui introduisait le développement de jeu vidéo en Lua avec Löve.
Tu vas voir comment créer un petit jeu de plateforme inspiré de Super Meat Boy et de Disc Room uniquement avec Löve.

Disc Room Escape
-----------------

Le jeu s'appelle Disc Room Escape et `est jouable sur itch.io <https://dotmobo.itch.io/disc-room-escape>`_.
Le but est simplement de traverser les différents niveaux, sans mourir, dans la limite de temps disponible.
Il faudra sauter sur des plateformes et éviter des scies.

Ici, pas besoin de librairies et outils annexes. Tout sera fait uniquement avec Löve.

.. image:: ./images/discroom.gif
    :alt: Disc Room

Code source
------------

Le code source est `intégralement disponible sur Github <https://github.com/dotmobo/disc-room-escape>`_.
N'hésite pas à le récupérer, à jour avec, à le modifier et à te l'approprier.

Je vais t'expliquer dans les grandes lignes son fonctionnement. Suis les liens vers les fichiers sources pour les comprendre.
Sur ce post, je ne mettrais en exemple que certains bout de code intéressant pour éviter de trop surcharger d'information.

Etat du jeu
-----------

On va commencer par créer un système qui gère l'état de notre jeu. 

Tu voudras avoir `un écran d'accueil <https://github.com/dotmobo/disc-room-escape/blob/master/StartState.lua>`_ où tu lances le jeu,
`un écran avec le jeu en cours <https://github.com/dotmobo/disc-room-escape/blob/master/PlayState.lua>`_,
`un écran de fin lors de la victoire <https://github.com/dotmobo/disc-room-escape/blob/master/WinState.lua>`_ et
`un écran de fin lors de la défaite <https://github.com/dotmobo/disc-room-escape/blob/master/DeadState.lua>`_. 

Tout ces écrans vont être manipulable grâce à `une classe GameState <https://github.com/dotmobo/disc-room-escape/blob/master/GameState.lua>`_
qui va se charger de gérer la transition des états. Il suffit par exemple, d'utiliser la commande suivante pour changer de niveau :

.. code-block:: lua
    
    GameState.setCurrent('Play', self.level_num + 1)

Le `fichier principal de Löve <https://github.com/dotmobo/disc-room-escape/blob/master/main.lua>`__ va juste se charger de démarrer le jeu sur
l'écran d'accueil et d'initier le Joystick, `le fichier de configuration <https://github.com/dotmobo/disc-room-escape/blob/master/conf.lua>`_ et
`les constantes du jeu <https://github.com/dotmobo/disc-room-escape/blob/master/const.lua>`_.

Animation et assets
-------------------

Tous les assets du jeu, sons et images, sont disponibles `ici <https://github.com/dotmobo/disc-room-escape/tree/master/assets>`_.
Tu peux les modifier selon tes propres envies. Tu auras besoin de deux petits helpers,
`un pour gérer les animations <https://github.com/dotmobo/disc-room-escape/blob/master/Animation.lua>`_ et
`un autre pour gérer les assets <https://github.com/dotmobo/disc-room-escape/blob/master/assets.lua>`_.

Le monde
--------

Chaque élément du jeu sera ajouter à `un monde <https://github.com/dotmobo/disc-room-escape/blob/master/World.lua>`_, qui va se charger de
vérifier en continuer la position des éléments et leurs collisions. 

On vérifie la collision de nos éléments à l'aide d'une fonction toute simple :

.. code-block:: lua

    local function checkCollision(a, b)
        return a.x < b.x + b.w and
            a.x + a.w > b.x and
            a.y < b.y + b.h and
            a.h + a.y > b.y
    end

Les niveaux
-----------

Les niveaux seront représentés par des tableaux de la manière suivante :

.. code-block:: lua

    return {
        6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,
        10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10,
        10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10,
        10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10,
        10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10,
        10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10,
        10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10,
        10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10,
        10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10,
        10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10,
        10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10,
        10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,10,
        10,0,0,0,0,0,0,0,0,3,3,0,0,0,3,3,0,0,0,0,0,0,0,0,10,
        10,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,10,
        2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,
        1,1,1,1,1,1,1,5,5,5,5,5,5,5,5,5,5,5,1,1,1,1,1,1,1,
    }

Chaque chiffre va représenter un élément sur notre écran. 

- le 0 représente le vide.
- le 1 sera `des murs <https://github.com/dotmobo/disc-room-escape/blob/master/Wall.lua>`_.
- le 2 sera `le sol <https://github.com/dotmobo/disc-room-escape/blob/master/Floor.lua>`_.
- le 3 sera `des plateformes amovibles <https://github.com/dotmobo/disc-room-escape/blob/master/ToggleFloor.lua>`_.
- le 4 sera `les portes de sorties <https://github.com/dotmobo/disc-room-escape/blob/master/Door.lua>`_.
- le 5 sera `des scies fixes <https://github.com/dotmobo/disc-room-escape/blob/master/Disc.lua>`_.
- le 6 sera `le toît <https://github.com/dotmobo/disc-room-escape/blob/master/Roof.lua>`_.
- le 7 sera `le boss du jeu <https://github.com/dotmobo/disc-room-escape/blob/master/Boss.lua>`_.
- le 8 sera `les ennemies du jeu <https://github.com/dotmobo/disc-room-escape/blob/master/Enemy.lua>`_, des scies qui se déplacent.
- le 9 sera `notre héro <https://github.com/dotmobo/disc-room-escape/blob/master/Hero.lua>`_.
- le 10 sera un élement du décor, `l'échafaudage <https://github.com/dotmobo/disc-room-escape/blob/master/Scaffold.lua>`_.

Une `classe Level <https://github.com/dotmobo/disc-room-escape/blob/master/Level.lua>`_ va se charger de l'affichage des éléments du niveau en fonction de ces chiffres.

Il sera alors possible de déclencher des évenements dans le monde, par exemple lorsque le joueur franchit une porte :

.. code-block:: lua

    ...
    self.touches_hero = GameState.getCurrent().world:check(self, 'is_hero')
    ...
    if self.touches_hero then
        GameState.getCurrent():trigger('door:open')
    end

Le hero
-------

Notre hero va devoir se déplacer si on utilise le Joystick ou le clavier, en utilisant un système d'accélération et de décélération :

.. code-block:: lua

    local dx, dy = 0, 0

    if love.keyboard.isDown('left') or (Joystick and (Joystick:isGamepadDown('dpleft') or Joystick:getGamepadAxis('leftx') <= -0.25)) then
        self:setAnim('run')
        self.last_direction = -1
        -- acceleration system
        self.vx = self.vx + (-self.speed * self.acceleration * dt)
        if self.vx < -self.speed then self.vx = -self.speed end
        -- dx = dx - dt * self.speed
    elseif love.keyboard.isDown('right') or (Joystick and (Joystick:isGamepadDown('dpright') or Joystick:getGamepadAxis('leftx') >= 0.25)) then
        self:setAnim('run')
        self.last_direction = 1
        -- acceleration system
        self.vx = self.vx + (self.speed * self.acceleration * dt)
        if self.vx > self.speed then self.vx = self.speed end
        -- dx = dx + dt * self.speed
    else
        -- deceleration system
        if self.vx < 0 then
            self.vx = self.vx + (self.speed * self.deceleration * dt)
            if self.vx > 0 then self.vx = 0 end
        elseif self.vx > 0 then
            self.vx = self.vx + (-self.speed * self.deceleration * dt)
            if self.vx < 0 then self.vx = 0 end
        end
        -- self.vx = 0
    end
    dx = dx + self.vx * dt

Tu va devoir gérer la gravité lors du saut :

.. code-block:: lua

    if (love.keyboard.isDown('up') or (Joystick and (Joystick:isGamepadDown('a')))) then
        -- init jump
        if self:canJump() then
            self.vy = HERO_JUMP_SPEED
            self.is_jumping = true
            local jumpSound = love.audio.newSource(SOUND_JUMP, "static")
            jumpSound:play()
        -- during the jump
        elseif self.is_jumping == true then
            -- reduce the gravity for smooth jump
            if self.vy < 0 then
                self.vy = self.vy - HERO_JUMP_GRAVITY * dt
            end
        end
    end
    -- gravity
    if self:isGrounded() then
        self.vy = 0
        self.is_jumping = false
        self.ungroundedTime = 0
    else
        self:setAnim('jump')
        self.vy = math.min(self.vy + HERO_GRAVITY * dt, HERO_MAX_VELOCITY)
        self.ungroundedTime = self.ungroundedTime + dt
    end

Et bien évidemment, il faudra l'animer à l'aide de notre helper :

.. code-block:: lua

    self:setAnim('run')

et le déplacer dans notre monde via :

.. code-block:: lua

    GameState.getCurrent().world:move(self, self.x + dx, self.y + self.vy, 'is_solid')


Les particules de sang
----------------------

Enfin, à la mort, on va utiliser `un système de particules <https://github.com/dotmobo/disc-room-escape/blob/master/Particles.lua>`_ pour gérer le sang.
On va pouvoir utiliser différents paramètres pour styliser nos particules :


.. code-block:: lua

    p.psystem:setParticleLifetime(0.5, 3)
    p.psystem:setEmissionRate(128)
    p.psystem:setEmitterLifetime(0.5)
    p.psystem:setSizeVariation(1)
    p.psystem:setLinearAcceleration(-100, -100, 100, 100)
    p.psystem:setColors(1, 1, 1, 1, 1, 1, 1, 0)

Conclusion
----------

J'espère que cet aperçu va te donner envie d'essayer Löve plus en profondeur ! Have fun !