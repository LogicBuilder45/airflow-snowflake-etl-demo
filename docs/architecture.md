# 🏗 Airflow → Snowflake ETL Architecture (Reference Implementation)

This document explains the high-level design of the **Airflow + Snowflake ETL pipeline** implemented in this repository.  
It uses simple, production-friendly patterns suitable for modern data engineering teams.

---

## 📐 1. High-Level Architecture

        +-----------------------+
        |     Source System     |
        |  (API, CSV, S3, etc.) |
        +----------+------------+
                   |
                   | Extract (PythonOperator)
                   v
        +-----------------------+
        |        Airflow        |
        |   DAG Orchestration   |
        +----+------------+-----+
             |            |
             |            |
             v            v
    Create Tables     Load Raw Data
     (SnowflakeOp)   (PythonOperator)
             \            /
              \          /
               \        /
                v      v
        +-----------------------+
        |       Snowflake       |
        |  RAW → ANALYTICS      |
        +-----------+-----------+
                    |
                    | Transform (SQL)
                    v
            ANALYTICS Tables



Airflow handles:

- **Scheduling**
- **Retry logic**
- **Dependency sequencing**
- **Parameterization**

Snowflake handles:

- **Storage**
- **ELT SQL**
- **Warehouse compute**

---

## 🧠 2. Logical Flow of the DAG

1. **Create Tables**  
   Ensures the RAW and ANALYTICS tables exist.  
   Implemented using `SnowflakeOperator` with `snowflake_ddl.sql`.

2. **Load Raw Data**  
   Runs a Python function (`load_demo_data_to_snowflake`) that connects to Snowflake and inserts sample rows.

3. **Transform Data**  
   Executes the transformation SQL (`snowflake_transform.sql`) to produce analytics-ready tables.

---

## 🧩 3. Detailed Component Breakdown

### **Airflow**

- Runs inside Docker via `docker-compose.yaml` (added next).
- Uses:
  - `PythonOperator` → for extraction/loading
  - `SnowflakeOperator` → for DDL and ELT SQL
- Uses an `.env` file for Snowflake credentials.

### **Snowflake**

- Objects involved:
  - `DEMO_RAW`
  - `DEMO_ANALYTICS`
- RAW layer receives data from extraction step.
- ANALYTICS layer receives structured data via SQL transform.

---

## 🔐 4. Configuration & Credentials

Airflow uses one of these connection methods:

### **Option A — Airflow Connection UI**
You create a connection named `snowflake_default`.

### **Option B — Environment Variables**
The repo includes a `.env.example` file with:
SNOWFLAKE_ACCOUNT=
SNOWFLAKE_USER=
SNOWFLAKE_PASSWORD=
SNOWFLAKE_ROLE=
SNOWFLAKE_WAREHOUSE=
SNOWFLAKE_DATABASE=
SNOWFLAKE_SCHEMA=



Docker Compose will load these into the Airflow container.

---

## ⚙️ 5. Why This Design is Production-Friendly

This architecture follows patterns used in real data engineering teams:

- **Separation of concerns**  
  Airflow controls orchestration; Snowflake controls compute.

- **Idempotent table creation**  
  Safe to rerun DAGs without creating duplicates.

- **Environment-driven config**  
  No hard-coded credentials.

- **Extensible structure**  
  RAW → STAGE → ANALYTICS can be scaled to more domains.

- **Operator clarity**  
  Work is split:
  - PythonOperator → extract/load  
  - SnowflakeOperator → transform  

This structure is familiar and credible to hiring managers, architects, and EB-1A reviewers.

---

## 📁 6. Repository Structure (for reference)

airflow-snowflake-etl-demo/
├── dags/
│ └── snowflake_etl_demo_dag.py
├── src/
│ ├── load/
│ │ └── snowflake_load.py
│ └── init.py
├── sql/
│ ├── snowflake_ddl.sql
│ └── snowflake_transform.sql
├── docs/
│ └── architecture.md
├── .env.example
├── requirements.txt
└── README.md





---

## 🚀 7. Next Steps

- Add more DAGs (e.g., CSV download → stage → transform)
- Add S3 extraction or API extraction examples
- Add a proper `docker-compose.yaml` to run Airflow locally  
  *(We will build this next per your request.)*

---


