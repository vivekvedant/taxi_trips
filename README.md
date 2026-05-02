# Taxi Trips Fare Prediction

Flask + PySpark project for predicting NYC taxi fare from trip details, with Docker-based deployment and optional MLflow tracking.

## What this project includes

- Fare prediction web UI built with Flask (`src/flask_app`)
- PySpark model training and inference code (`src/models`)
- Docker Compose stack with Spark master/worker + Flask + Nginx (`docker-compose.yml`)
- Monitoring configs (Loki / Prometheus / Grafana) under `monitoring/`
- Basic tests with `pytest`

## Repository Structure

```text
.
├── conf/                    # Data and location configuration JSON files
├── Docker_Files/            # Dockerfiles for Flask, Spark, and Nginx services
├── docs/                    # Sphinx docs scaffold
├── monitoring/              # Monitoring configs and dashboards
├── notebooks/               # Exploration notebooks
├── src/
│   ├── flask_app/           # Flask app, templates, static files
│   ├── models/              # Training, preprocessing, inference, pipeline scripts
│   └── ngnix/               # Nginx config files used by container
├── tests/                   # Pytest suite
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.8+
- `pip`
- Docker + Docker Compose (for containerized run)

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the App (Docker)

Recommended path for full stack execution:

```bash
bash run_docker.sh
```

What it does:

- Installs Loki Docker logging plugin
- Stops old containers/volumes
- Rebuilds images with no cache
- Starts containers in detached mode
- Runs tests inside `flask_app` container

After startup:

- App is exposed via Nginx on `http://localhost:80`
- Spark master UI is available on `http://localhost:8080`
- Spark worker UI is available on `http://localhost:8081`

## Run Model Pipeline + MLflow (local script)

`start.sh` executes the model pipeline and then starts MLflow server.

Required environment variables:

- `DB_URI` (MLflow backend store URI)
- `MLFLOW_ARTIFACT_ROOT` (artifact storage location)

Example:

```bash
export DB_URI=sqlite:///mlflow.db
export MLFLOW_ARTIFACT_ROOT=./artifacts
bash start.sh
```

## Run MLflow UI only

```bash
export DB_URI=sqlite:///mlflow.db
export MLFLOW_ARTIFACT_ROOT=./artifacts
bash start_ui.sh
```

## Testing

Run tests locally:

```bash
pytest -q
```

Run tests in containers (already included in `run_docker.sh`):

```bash
docker-compose exec flask_app pytest tests
```

## Main Code Paths

- Flask entrypoint: `src/flask_app/app.py`
- Prediction logic: `src/models/predict.py`
- Training logic: `src/models/train_model.py`
- End-to-end pipeline: `src/models/pipeline.py`

## Notes

- Some paths in Flask/inference code are absolute container-style paths (for example `/taxi_trips/...`), so Docker is the most reliable way to run the app as-is.
- Model artifacts are mounted into the Spark worker container from `trained_models/`.
