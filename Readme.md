# CS2 Esports Data Engineering Pipeline

An end-to-end **Data Engineering pet project** for collecting, processing, storing, transforming, and validating Counter-Strike 2 esports data.

The project demonstrates a production-like data pipeline built with **Python, Apache Airflow, MinIO, PostgreSQL, ClickHouse, Docker, Alembic, SQLAlchemy, and Sentry**.

The pipeline collects tournament and match data from Cybersport.ru, stores raw data in MinIO, processes it into PostgreSQL, builds analytical marts in ClickHouse, and performs data quality checks.

---

## Architecture

```text
                    ┌─────────────────────┐
                    │   Cybersport.ru     │
                    │      CS2 data        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Scrapers       │
                    │       Python        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       MinIO         │
                    │     Raw Storage     │
                    │       S3 API        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      PostgreSQL     │
                    │   Normalized Data   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     ClickHouse      │
                    │   Analytical Marts  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Data Quality     │
                    │       Checks        │
                    └─────────────────────┘


                 Apache Airflow
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      Scraping    PostgreSQL    ClickHouse
       tasks        tasks          tasks
                       │
                       ▼
                     Sentry
                 Error monitoring
```

---

## What the project does

The pipeline performs the following steps:

1. Scrapes CS2 tournament data.
2. Scrapes match information.
3. Scrapes player statistics.
4. Stores the raw scraped data in MinIO.
5. Loads normalized entities into PostgreSQL.
6. Builds analytical datasets in ClickHouse.
7. Runs data quality checks.
8. Orchestrates the entire workflow with Apache Airflow.
9. Sends application errors and warnings to Sentry.
10. Stores Airflow task logs in MinIO.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Scraping and data processing |
| BeautifulSoup | HTML parsing |
| SQLAlchemy | PostgreSQL ORM |
| Alembic | Database migrations |
| PostgreSQL | Operational/normalized storage |
| MinIO | S3-compatible raw data storage |
| ClickHouse | Analytical storage |
| Apache Airflow | Pipeline orchestration |
| Docker | Application infrastructure |
| Sentry | Error monitoring |
| Psycopg | PostgreSQL driver |
| ClickHouse Python Client | ClickHouse access |

---

## Project Structure

```text
.
├── app/
│   ├── config.py
│   ├── pipeline/
│   │   ├── main.py
│   │   ├── scraper/
│   │   ├── postgres/
│   │   ├── clickhouse/
│   │   └── data_quality/
│   └── store/
│
├── airflow/
│   └── dags/
│       └── cybersport_etl.py
│
├── docker/
│   ├── airflow/
│   ├── minio/
│   ├── postgres/
│   └── clickhouse/
│
├── migrations/
│   └── versions/
│
├── models/
│   ├── event.py
│   ├── match.py
│   ├── match_map.py
│   ├── player.py
│   └── statistic.py
│
├── scraper/
│   ├── events.py
│   ├── matches.py
│   └── statistics.py
│
├── services/
│   ├── db.py
│   ├── clickhouse.py
│   ├── minio_client.py
│   ├── crawler.py
│   ├── logger.py
│   └── sentry.py
│
├── minio/
│   └── data/
│
├── .env.example
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# Data Flow

## 1. Scraping

The scraper collects CS2 esports data from Cybersport.ru.

The main scraping pipelines are:

```text
scraper.events
scraper.matches
scraper.statistics
```

The scraper extracts information such as:

- tournaments
- matches
- teams
- maps
- players
- player statistics
- match scores

The scraped data is stored as JSON in MinIO.

---

## 2. MinIO Raw Storage

MinIO is used as the **raw data layer**.

The data is intentionally stored by date and tournament:

```text
<date>/
└── <tournament>/
    ├── event.json
    ├── match_team_data.json
    └── match_statistics.json
```

This allows raw data from different scraping runs to remain separated.

MinIO provides an S3-compatible API and is also used for storing Airflow remote logs.

---

## 3. PostgreSQL

PostgreSQL is used as the normalized storage layer.

The main entities include:

```text
events
matches
match_maps
players
statistics
```

The application uses:

- SQLAlchemy
- Psycopg
- Alembic

Database schema changes are managed through Alembic migrations.

The loading process is designed to be **idempotent** where possible, using insert/upsert operations and unique keys.

---

## 4. ClickHouse

ClickHouse is used as the analytical storage layer.

The PostgreSQL data is transformed into analytical marts.

Current marts include:

```text
mart_player_performance
mart_match_summary
```

These tables are designed for analytical queries rather than transactional operations.

---

## 5. Data Quality

After the ClickHouse marts are generated, the pipeline runs data quality checks.

The Data Quality stage validates the resulting analytical data and detects problems before the pipeline is considered successful.

```text
PostgreSQL
     │
     ▼
ClickHouse marts
     │
     ▼
Data Quality checks
     │
     ▼
Pipeline success / failure
```

---

# Airflow Pipeline

The complete workflow is orchestrated by Apache Airflow.

The DAG contains the following major stages:

```text
scraper.events
       │
       ▼
postgres.events
       │
       ▼
postgres.matches
       │
       ▼
postgres.matchmap
       │
       ▼
postgres.statistics
       │
       ├───────────────┐
       ▼               ▼
mart_player       mart_match
_performance       _summary
       │               │
       └───────┬───────┘
               ▼
         data_quality
```

Match and statistics scraping can run independently where their dependencies allow it.

The actual Airflow DAG manages the required task dependencies.

---

# Prerequisites

Before starting the project, install:

- Docker
- Docker Compose
- Git

Recommended resources:

```text
CPU:    4+ cores
RAM:    8 GB+
Disk:   10 GB+
```

The project is designed to run inside Docker containers, so Python does not need to be installed locally for the main pipeline.

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/vladmunj/cybersport.git
cd cybersport
```

---

## 2. Create the environment file

Copy the example environment file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and configure the required credentials.

---

# Environment Configuration

The project uses environment variables for database credentials, MinIO, ClickHouse, Airflow, and Sentry configuration.

A typical configuration contains:

```env
# MinIO
MINIO_USER=minioadmin
MINIO_PASSWORD=change_me

# PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=change_me
POSTGRES_DB=cybersport
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# ClickHouse
CLICKHOUSE_HOST=clickhouse
CLICKHOUSE_PORT=8123
CLICKHOUSE_USER=default
CLICKHOUSE_PASSWORD=
CLICKHOUSE_DB=cybersport

# Airflow PostgreSQL
AIRFLOW_POSTGRES_USER=airflow
AIRFLOW_POSTGRES_PASSWORD=change_me
AIRFLOW_POSTGRES_DB=airflow
AIRFLOW_POSTGRES_HOST=airflow-postgres
AIRFLOW_POSTGRES_PORT=5432

# Airflow
AIRFLOW_ADMIN_USERNAME=admin
AIRFLOW_ADMIN_PASSWORD=change_me

AIRFLOW_SECRET_KEY=change_me
AIRFLOW_FERNET_KEY=change_me
AIRFLOW_JWT_SECRET=change_me

# Sentry
SENTRY_DSN=your_sentry_dsn
```

Use strong passwords for non-local or shared environments.

---

# Generating Airflow Secrets

The Airflow Fernet key is used to encrypt sensitive information stored in the Airflow metadata database.

Generate a Fernet key with:

```bash
docker compose run --rm airflow-init \
  python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Copy the generated value to:

```env
AIRFLOW_FERNET_KEY=...
```

The same key must remain unchanged after Airflow has been initialized.

---

# Starting the Infrastructure

Start all services:

```bash
docker compose up -d --build
```

Check running containers:

```bash
docker compose ps
```

Follow logs:

```bash
docker compose logs -f
```

Or follow a specific service:

```bash
docker compose logs -f airflow-scheduler
```

---

# Service Ports

The main services are available at:

| Service | Port | Purpose |
|---|---:|---|
| Airflow | `8080` | Workflow management UI |
| MinIO API | `9000` | S3-compatible API |
| MinIO Console | `9001` | MinIO Web UI |
| PostgreSQL | `5432` | Application database |
| ClickHouse HTTP | `8123` | ClickHouse HTTP API |
| ClickHouse Native | `9009` | ClickHouse native protocol |

---

# MinIO

MinIO is automatically initialized when the Docker Compose stack starts.

The initialization process creates the required buckets.

The Airflow logs bucket is:

```text
airflow-logs
```

Airflow uses this bucket for remote task logging.

MinIO Console:

```text
http://localhost:9001
```

Use the credentials from `.env`.

---

# Database Migrations

PostgreSQL schema changes are managed by Alembic.

Run migrations inside the application environment:

```bash
docker compose exec airflow-scheduler alembic upgrade head
```

Or run Alembic from the appropriate project container where the project environment is available.

Check the current migration:

```bash
alembic current
```

Show migration history:

```bash
alembic history
```

---

# Airflow

After the containers have started, open:

```text
http://localhost:8080
```

Login using:

```text
Username: AIRFLOW_ADMIN_USERNAME
Password: AIRFLOW_ADMIN_PASSWORD
```

The main DAG is:

```text
cybersport_etl
```

The DAG orchestrates the complete ETL workflow from scraping to data quality validation.

---

# Running the Pipeline

The recommended way to run the complete pipeline is through Airflow.

1. Open Airflow.
2. Find `cybersport_etl`.
3. Enable the DAG.
4. Trigger a new DAG run.
5. Monitor the task graph.

A successful run should finish with all tasks in the `success` state.

---

# Pipeline Modules

The project separates the pipeline into independent modules.

### Scraping

```text
scraper.events
scraper.matches
scraper.statistics
```

### PostgreSQL

```text
postgres.events
postgres.matches
postgres.matchmap
postgres.statistics
```

### ClickHouse

```text
clickhouse.mart_player_performance
clickhouse.mart_match_summary
```

### Data Quality

```text
data_quality.clickhouse
```

The pipeline runner dynamically loads these modules and executes their corresponding pipeline functions.

---

# Error Monitoring

Sentry is integrated into the application for error monitoring.

Unexpected exceptions are reported to Sentry together with useful execution context.

The project also reports skipped duplicate records during batch upsert operations.

This allows data problems to be monitored without necessarily stopping the entire pipeline for every non-critical duplicate.

Configure Sentry using:

```env
SENTRY_DSN=your_sentry_dsn
```

---

# Idempotency

The pipeline uses idempotent loading strategies where possible.

For example, PostgreSQL batch operations use unique keys to determine whether records should be inserted or updated.

This makes it possible to safely rerun individual Airflow tasks without unnecessarily creating duplicate records.

Examples of logical keys include:

```text
events       → slug
matches      → external_id
match_maps   → match_id + map_id
statistics   → match_id + player_id + team_id
```

This is especially important for Airflow because failed tasks can be retried or manually rerun.

---

# Development

The project can also be executed outside the complete Airflow workflow for development and debugging.

Individual pipeline modules can be executed through the project's pipeline runner.

For example:

```bash
python -m app.pipeline.main scraper.events
```

The exact command depends on the pipeline runner configuration.

For debugging individual stages, it is possible to run the corresponding pipeline independently instead of executing the entire DAG.

---

# Logs

Airflow uses remote logging through MinIO.

Task logs are stored under:

```text
s3://airflow-logs/logs
```

This means Airflow task logs remain available independently of the lifecycle of individual Airflow containers.

---

# Troubleshooting

## Airflow does not start

Check:

```bash
docker compose ps
```

Then inspect the logs:

```bash
docker compose logs airflow-init
docker compose logs airflow-scheduler
docker compose logs airflow-api-server
```

---

## MinIO bucket does not exist

Check the initialization container:

```bash
docker compose logs minio-init
```

The initialization process should finish with:

```text
MinIO initialization completed.
```

---

## PostgreSQL migration fails

Check the current database revision:

```bash
alembic current
```

Then check migration history:

```bash
alembic history
```

Make sure the PostgreSQL container is running and the application is connected to the expected database.

---

## Airflow task fails

Open the failed task in Airflow and inspect its logs.

Because the pipeline is divided into independent tasks, a failed task can usually be rerun after fixing the underlying problem without executing the entire pipeline from the beginning.

---

# Learning Goals

This project was created as a practical Data Engineering project and demonstrates several concepts commonly used in real-world data platforms:

- ETL/ELT pipelines
- Web scraping
- Raw data storage
- S3-compatible object storage
- Data normalization
- Relational databases
- Analytical databases
- Data marts
- Batch processing
- Idempotent data loading
- Upserts
- Database migrations
- Workflow orchestration
- Task dependencies
- Data quality
- Error monitoring
- Remote logging
- Dockerized infrastructure

---

# Future Improvements

Possible future improvements include:

- Incremental data loading
- More advanced data quality checks
- Additional ClickHouse marts
- Performance optimization
- Partitioning and indexing improvements
- Automated tests
- CI/CD
- More detailed Airflow monitoring
- Additional CS2 data sources
- Historical data backfilling
- Analytical dashboards

---

# Project Status

The complete Airflow ETL pipeline is operational.

Current workflow:

```text
Cybersport.ru
      ↓
   Scraping
      ↓
     MinIO
      ↓
  PostgreSQL
      ↓
  ClickHouse
      ↓
 Data Quality
      ↓
   SUCCESS
```

The project is primarily intended as a **Data Engineering learning project and portfolio project**, demonstrating an end-to-end data platform rather than a production commercial system.