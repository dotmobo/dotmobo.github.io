Maturin : Booster Python avec du Rust
#####################################

:date: 2025-09-01
:tags: maturin, pyo3, rust, python
:category: Rust
:slug: maturin
:authors: Morgan
:summary: Maturin : Booster Python avec du Rust

.. image:: ./images/ferris.png
    :alt: Rust
    :align: right

La plupart des librairies **Python** actuelles qui sont à la mode comme **pydantic**, **ruff** ou **uv** sont écrites en
grande partie en **Rust** pour des raisons de performance. Mais comment ont-ils géré cette intégration ?

La solution se situe dans un outil ultra pratique appelé `Maturin <https://www.maturin.rs/>`_ qui permet de créer des extensions Python en Rust
de manière très simple. L'idée derrière **maturin** est de compiler le code Rust en librairie Python directement utilisable.

Un peu comme **CPython** qui fait du binding entre le code C et Python, **PyO3** (une dépendance de maturin) fait du binding entre Rust et Python.

Création d'un projet Python
===========================

Tu peux commencer par créer un projet Python classique avec un environnement virtuel.

On va utiliser `uv <https://astral.sh/uv/>`_ qu'on a vu sur l'article précédent.

.. code-block:: bash

    uv init myrustapp -p 3.13
    cd myrustapp
    uv venv -p 3.13
    source .venv/bin/activate

Installation de maturin
=======================

On va maintenant installer `maturin` dans notre environnement virtuel.

.. code-block:: bash

    uv add maturin

Et c'est tout !

Création du projet Rust
=======================

Pour créer le projet Rust, on va utiliser `maturin init` qui va nous créer notre librairie Rust avec tout ce qu'il faut
dans le **Cargo.toml** pour faire le lien avec Python.

.. code-block:: bash

    maturin init --bindings pyo3 myrustlib
    cd myrustlib
    maturin develop

Avec `maturin develop`, on compile la librairie et on l'installe directement dans notre environnement virtuel.

Une fois le développement terminé, il vaut mieux utiliser `maturin develop -r` pour créer la librairie en mode release
pour de meilleures performances.

Il est également possible de builder et de déployer sur PyPI la librairie avec `maturin build -r` et `maturin publish`.

Le code Rust
============

Ok maintenant qu'on a notre workflow opérationnel, on va jeter un oeil au code Rust dans **src/lib.rs**.

.. code-block:: rust

    use pyo3::prelude::*;

    /// Formats the sum of two numbers as string.
    #[pyfunction]
    fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
        Ok((a + b).to_string())
    }

    /// A Python module implemented in Rust.
    #[pymodule]
    fn myrustlib(m: &Bound<'_, PyModule>) -> PyResult<()> {
        m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
        Ok(())
    }

On va rapidement détailler comme ça tu pourras le modifier et l'étendre de toi-même.

Les deux macros **#[pyfunction]** et **#[pymodule]** sont fournies par PyO3 pour faire le lien entre Rust et Python.

Pour toutes les fonctions que tu veux exposer à python, tu utiliseras **#[pyfunction]**.
Si tes paramètres de fonctions sont des types natifs Python (int, str, list, dict...) tu n'as rien de plus à faire.

Il te suffit alors d'ajouter les fonctions au module python via **m.add_function** dans la macro **#[pymodule]**.

Si tu veux utiliser des types Rust plus complexes, tu peux utiliser les types fournis par PyO3 comme **PyList** ou **PyDict**.

Et voilà, tu peux maintenant utiliser n'importe quel code Rust dans ton projet Python.
N'oublie pas de recompiler avec `maturin develop -r` à chaque modification.

Accélérer numpy
===============

Pour le ML, tu peux utiliser `numpy <https://github.com/PyO3/rust-numpy/>`_ qui fait le lien entre les arrays numpy et les arrays Rust.


.. code-block:: rust

        use numpy::ndarray::{ArrayD, ArrayViewD, ArrayViewMutD};
    use numpy::{IntoPyArray, PyArrayDyn, PyReadonlyArrayDyn, PyArrayMethods};
    use pyo3::{pymodule, types::PyModule, PyResult, Python, Bound};

    #[pymodule]
    fn rust_ext<'py>(_py: Python<'py>, m: &Bound<'py, PyModule>) -> PyResult<()> {
        // example using immutable borrows producing a new array
        fn axpy(a: f64, x: ArrayViewD<'_, f64>, y: ArrayViewD<'_, f64>) -> ArrayD<f64> {
            a * &x + &y
        }

        // example using a mutable borrow to modify an array in-place
        fn mult(a: f64, mut x: ArrayViewMutD<'_, f64>) {
            x *= a;
        }

        // wrapper of `axpy`
        #[pyfn(m)]
        #[pyo3(name = "axpy")]
        fn axpy_py<'py>(
            py: Python<'py>,
            a: f64,
            x: PyReadonlyArrayDyn<'py, f64>,
            y: PyReadonlyArrayDyn<'py, f64>,
        ) -> Bound<'py, PyArrayDyn<f64>> {
            let x = x.as_array();
            let y = y.as_array();
            let z = axpy(a, x, y);
            z.into_pyarray(py)
        }

        // wrapper of `mult`
        #[pyfn(m)]
        #[pyo3(name = "mult")]
        fn mult_py<'py>(a: f64, x: &Bound<'py, PyArrayDyn<f64>>) {
            let x = unsafe { x.as_array_mut() };
            mult(a, x);
        }

        Ok(())
    }

Dans la plupart des cas, numpy est suffisamment performant. Mais tu n'es jamais à l'abri de tomber sur un cas critique
où une petite partie de l'application nécessite un boost de performance.

Avec maturin, tu t'évites de devoir réécrire tout le projet en Rust pour te concentrer uniquement sur la partie concernée.

Quand utiliser Rust dans Python ?
===============================

Dans la plupart des cas classiques, tu n'auras pas besoin de coder en Rust.

Mais dès que tu vas devoir manipuler des milliers ou millions de données, et que tu te rends compte que **pandas** ne suffit plus
niveau vitesse, tu pourras coder la partie critique en Rust.

Typiquement, toute opération de filtrage, de transformation, d'agrégation, ou de calcul sur des milliers de données
vont pouvoir être profondément accélérées. Tu vas passer de plusieurs secondes à quelques millisecondes.

À garder dans un coin de sa tête pour les projets futurs !

