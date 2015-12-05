Ajouter un captcha dans un formulaire django
############################################

:date: 2015-11-28
:tags: python,django,django-simple-captcha,captcha,crispy,django-crispy,recaptcha
:category: Django
:slug: django-simple-captcha
:authors: Morgan
:summary: Ajouter un captcha dans un formulaire django

.. image:: ./images/djangopony.png
    :alt: Django
    :align: right

Suite à `l'article sur django-countries <http://dotmobo.github.io/django-countries.html>`_,
on va continuer notre parcours des petits outils simples et efficaces pour améliorer nos formulaires django.

Avant d'aborder le gros morceau qu'est `django-cryspy <http://django-crispy-forms.readthedocs.org/en/latest/>`_
(tu peux déjà y jeter un oeil si tu es curieux), on va parler de l'intégration de captchas sous django.

L'api de captcha la plus connue est sûrement `reCAPTCHA <https://www.google.com/recaptcha>`_ de google,
et il en existe une implémentation sous django baptisée `django-recaptcha <https://github.com/praekelt/django-recaptcha>`_.

Mais tu ne veux peut-être pas dépendre d'un service google pour diverses raisons, en préférant
une solution autonome, simple, légère, efficace et maintenue.

`Django-simple-captcha <https://github.com/mbi/django-simple-captcha>`_ remplit haut la main toutes ces conditions
et est même compatible python 3. Elle est customisable, s'intègre dans les formulaires django et sous
*django-crispy*. Différents types de captcha sont disponibles comme des caractères aléatoires,
des calculs mathématiques, des dictionnaires de mots.

Captcha utilise *PIL* et *Pillow* qui nécessitent certaines librairies systèmes.
Par exemple sous Ubuntu, tu fais:

.. code-block:: bash

    apt-get -y install libz-dev libjpeg-dev libfreetype6-dev

Tu l'installes comme d'habitude avec pip:

.. code-block:: bash

    pip install django-simple-captcha

Et tu ajoutes **captcha** dans la liste de tes **INSTALLED_APPS**
dans le fichier *settings.py* de django:

.. code-block:: python

    INSTALLED_APPS = (...,
                      captcha
    )

Tu synchronises ta base de données:

.. code-block:: bash

    python manage.py migrate

Et tu ajoutes l'entrée suivante dans ton fichier **urls.py**:

.. code-block:: python

    urlpatterns += patterns('',
        url(r'^captcha/', include('captcha.urls')),
    )

Il ne reste plus qu'à l'intégrer dans ton formulaire.

* Soit dans un **Form**:

.. code-block:: python

    from django import forms
    from captcha.fields import CaptchaField

    class CaptchaTestForm(forms.Form):
        myfield = AnyOtherField()
        captcha = CaptchaField()

* Soit dans un **ModelForm**:

.. code-block:: python

    from django import forms
    from captcha.fields import CaptchaField

    class CaptchaTestModelForm(forms.ModelForm):
        captcha = CaptchaField()
        class Meta:
            model = MyModel

Et sous *django-crispy*, tu peux utiliser **captcha** comme un **Field** à déclarer dans le **Layout**:

.. code-block:: python

    from django import forms
    from captcha.fields import CaptchaField
    from crispy_forms.helper import FormHelper
    from crispy_forms.layout import Layout, Field, Submit

    class CaptchaTestModelForm(forms.ModelForm):
        captcha = CaptchaField()

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()

            self.helper.layout = Layout(
                Field('name', placeholder="Enter Full Name"),
                Field('captcha ', placeholder="Enter captcha"),
                Submit('valid', 'Valid')
                )

        class Meta:
            model = MyModel

La validation du formulaire se fait comme d'habitude. Si la réponse au captcha
est mauvaise, une exception **ValidationError** sera levée:

.. code-block:: python

    def some_view(request):
        if request.POST:
            form = CaptchaTestForm(request.POST)

            # Validate the form: the captcha field will automatically
            # check the input
            if form.is_valid():
                human = True
        else:
            form = CaptchaTestForm()

        return render_to_response('template.html',locals())

Il est également possible de faire une validation
`via ajax <http://django-simple-captcha.readthedocs.org/en/latest/usage.html#example-usage-for-ajax-form>`_.

Il y a toute `une série de paramètres <http://django-simple-captcha.readthedocs.org/en/latest/advanced.html>`_
permettant la customisation du captcha, mais il y en a surtout deux à retenir.

Le premier permet de choisir le type de captcha que tu veux utiliser.
Dans ton **settings.py**, tu peux mettre au choix:

.. code-block:: python

    # Random chars
    CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge'
    # Simple Math
    CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'
    # Dictionary Word
    CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.word_challenge'

Tu peux même créer `ta propre fonction de captcha <http://django-simple-captcha.readthedocs.org/en/latest/advanced.html#roll-your-own>`_
si celles proposées ne te conviennent pas.

Le second permet d'utiliser le captcha dans les tests unitaires. Si la chaîne de caractères **PASSED**
est renseignée comme valeur de réponse au captcha, le formulaire sera valide.
À mettre dans ton fichier de configuration de tes tests unitaires:

.. code-block:: python

    CAPTCHA_TEST_MODE = True

Le résultat final ressemble à ça :

.. image:: http://django-simple-captcha.readthedocs.org/en/latest/_images/captcha3.png
    :alt: Django
    :align: left
