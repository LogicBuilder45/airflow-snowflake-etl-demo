# Airflow + Snowflake ETL (Reference Implementation)

This repository demonstrates an end-to-end ETL orchestration pattern using Apache Airflow and Snowflake.
It focuses on clear separation of concerns (extract, load), environment-driven configuration, and simple
patterns you can adapt for production.

## Architecture (High Level)
- Source (public dataset/API or CSV)
- Airflow (scheduled DAG)
- Staging in Snowflake (internal stage/table)
- Transformations (SQL)
- Analytics-ready tables

## Tech Stack
- Apache Airflow
- Snowflake (snowflake-connector-python, Snowflake SQL)
- Python (requests, pandas/pyarrow optional)
- Docker Compose (local orchestration)

## Getting Started
1. Copy `.env.example` to `.env` and fill in Snowflake values.
2. (Optional) Adjust `sql/snowflake_ddl.sql` for database/schema/table names.
3. Use Docker Compose to run Airflow locally (see **Local Dev**).
4. Place your DAGs in `dags/` and Python helpers in `src/`.

## Local Dev (Docker Compose)
```bash
# one-time (set AIRFLOW_UID env var on Linux/macOS; Windows users can omit)
make init

# start the stack
make up

# open Airflow Web UI (default http://localhost:8080)
# stop the stack
make down
```

## Snowflake Setup
- Create warehouse, role, database, and schema (see `sql/roles_rbac.sql` and `sql/snowflake_ddl.sql`).
- Configure a Snowflake connection in Airflow via environment variables or UI.

## Repo Layout
```
dags/                    # Airflow DAGs
src/                     # Python helpers (extract/load/utils)
  extract/               # source extraction utilities or API clients
  load/                  # Snowflake loading utilities
  utils/                 # common helpers (logging, configs)
sql/                     # DDL/DML scripts for Snowflake
docs/                    # diagrams and documentation
tests/                   # minimal tests or examples
docker-compose.yaml      # local Airflow stack
requirements.txt         # Python deps for Airflow image / DAGs
.env.example             # environment variable template
.gitignore               # standard ignores
```
