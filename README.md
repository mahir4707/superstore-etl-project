# Superstore ETL Pipeline

An end-to-end data engineering project that extracts raw retail data, cleans and transforms it using Python and Pandas, validates data quality, and loads the processed dataset into PostgreSQL.

**Tech stack:** Python · Pandas · NumPy · PostgreSQL · SQLAlchemy · pytest · Git

## Project Overview

Real-world datasets often contain duplicate records, missing values, inconsistent formatting, and data-quality issues. This project implements a structured ETL pipeline to process a Superstore retail dataset and prepare it for downstream analytics.

The pipeline is orchestrated through a single entry point, `main.py`, with separate modules for extraction, transformation, and database loading.

## Architecture

```text
Raw CSV Dataset
      |
      v
   Extract
 scripts/extract.py
      |
      v
  Transform
 scripts/transform.py
      |
      v
   Validate
     main.py
      |
      +--------------------+
      |                    |
      v                    v
 Cleaned CSV          PostgreSQL
                       superstore_v2
```

## Key Features

- **Modular ETL architecture:** Separate extraction, transformation, and loading modules.
- **Data cleaning:** Standardizes column names and trims text values.
- **Duplicate handling:** Removes exact duplicate rows.
- **Missing-value handling:** Preserves missing financial values and creates flags to identify missing Sales and Profit values.
- **Data transformation:** Derives unit price, profit margin, and shipping duration.
- **Data validation:** Checks required columns, duplicate rows, and missing order and product identifiers.
- **Database integration:** Loads processed data into PostgreSQL using SQLAlchemy.
- **Logging and exception handling:** Records pipeline stages, validation results, and failures.
- **Automated testing:** Uses pytest to test transformation behavior.
- **Credential management:** Reads database configuration from environment variables rather than hardcoding credentials.

## Project Structure

```text
superstore-etl-project/
├── data/
│   ├── Superstore_Messy.csv
│   └── Superstore_Final_Cleaned.csv
├── scripts/
│   ├── __init__.py
│   ├── extract.py
│   ├── transform.py
│   └── load.py
├── tests/
│   └── test_transform.py
├── sql/
│   └── queries.sql
├── logs/
│   └── pipeline.log
├── main.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

The `.env` file and runtime logs are excluded from Git using `.gitignore`.

## Dataset and Processing Results

Results from a successful local pipeline execution:

| Metric | Result |
|---|---:|
| Raw rows | 10,294 |
| Exact duplicate rows removed | 273 |
| Cleaned rows | 10,021 |
| Raw columns | 21 |
| Transformed columns | 27 |
| Missing Sales values | 300 |
| Missing Profit values | 300 |
| Invalid shipping records flagged | 0 |

Missing financial values are preserved rather than replaced with invented values. Additional flags identify missing Sales and Profit values for downstream analysis.

## Technologies Used

- **Python:** Pipeline orchestration and data processing
- **Pandas:** Data extraction, cleaning, and transformation
- **NumPy:** Handling non-finite derived numerical values
- **PostgreSQL:** Relational storage for processed data
- **SQLAlchemy:** Database connectivity and data loading
- **python-dotenv:** Loading local environment configuration
- **pytest:** Automated tests for transformation logic

## Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/mahir4707/superstore-etl-project.git
cd superstore-etl-project
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```dotenv
DB_HOST=localhost
DB_PORT=5433
DB_NAME=superstore_db
DB_USER=postgres
DB_PASSWORD=your_local_database_password
```

Replace the example password with your local PostgreSQL password. Never commit real credentials to GitHub.

Ensure PostgreSQL is running and the configured database already exists.

### 4. Run the ETL pipeline

```bash
python main.py
```

The pipeline extracts the raw data, transforms and validates it, writes the cleaned CSV, and loads the data into the PostgreSQL table `public.superstore_v2`.

The loader intentionally fails if the target table already exists. It does not automatically overwrite an existing table.

### 5. Run automated tests

```bash
python -m pytest -v
```

The current test suite covers:

- Exact duplicate removal
- Unit price and profit margin calculations
- Preservation and flagging of missing financial values
- Rejection of an empty DataFrame

**Current test result:** 4 passed.

## Database Verification

The successful PostgreSQL load was verified locally:

- Table: `public.superstore_v2`
- Rows loaded: 10,021
- Columns: 27

Example SQL queries:

```sql
-- Total rows loaded
SELECT COUNT(*)
FROM public.superstore_v2;

-- Inspect the dataset
SELECT *
FROM public.superstore_v2
LIMIT 10;

-- Check missing financial values
SELECT
    COUNT(*) FILTER (WHERE sales IS NULL) AS missing_sales,
    COUNT(*) FILTER (WHERE profit IS NULL) AS missing_profit
FROM public.superstore_v2;

-- Sales and profit by category
SELECT
    category,
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit
FROM public.superstore_v2
GROUP BY category
ORDER BY total_sales DESC;
```

## Future Improvements

- Add automated tests for the complete pipeline and database loading.
- Introduce structured data-quality reports and configurable validation rules.
- Add database migrations and a controlled strategy for repeatable loads.
- Add CI automation with GitHub Actions.
- Containerize the application with Docker.
- Extend the pipeline with incremental loading and scheduling.

## Author

**Mahir Sama**

Computer Engineering student interested in Data Engineering, Data Analytics, databases, and building reliable data pipelines.

GitHub: https://github.com/mahir4707
