taxi_trips
==============================

This helps to predict the nyc taxi fare amount

Project Organization
------------

    ├── LICENSE
    ├── Makefile                <- Makefile with commands like `make data` or `make train`
    ├── README.md               <- The top-level README for developers using this project.
    ├── data
    │   ├── external            <- Data from third party sources.
    │   ├── interim             <- Intermediate data that has been transformed.
    │   ├── processed           <- The final, canonical data sets for modeling.
    │   └── raw                 <- The original, immutable data dump.
    │
    ├── docs                    <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models                  <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks               <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                              the creator's initials, and a short `-` delimited description, e.g.
    │                              `1.0-jqp-initial-data-exploration`.
    │
    ├── references              <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports                 <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures             <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt        <- The requirements file for reproducing the analysis environment, e.g.
    │                              generated with `pip freeze > requirements.txt`
    │
    ├── Dockerfile.flask        <- Dockerfile for flask container
    │
    ├── Dockerfile.ngnix        <- Dockerfile for ngnix container
    │
    ├── docker-compose.yaml     <- Creates Docker container
    │
    ├── run_docker.sh           <- Remove old docker container and create new container
    │
    ├── setup.py                <- makes project pip installable (pip install -e .) so src can be imported
    │
    ├── test                     <- Scripts for testing
    │   ├── __init__.py          <- Makes src a Python module
    |   ├──
    |
    ├── src                     <- Source code for use in this project.
    │   ├── __init__.py         <- Makes src a Python module
    |   |
    │   ├── flask_app           <- Scripts to run flask application
    │   │   ├── templates       <- contains html pages
    │   │   │     └── index.html
    |   |   ├── app.py
    |   |   ├── wsgi.py
    │   │   └── ngnix           <- contains ngnix config files
    │   │        ├── nginx.conf
    │   │        └── project.conf
    │   ├── models              <- Scripts to train models and then use trained models to make
    │   │   │                      predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization       <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini                 <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
