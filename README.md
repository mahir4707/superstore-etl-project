# Superstore ETL Pipeline Project

## Overview

This project demonstrates an end-to-end ETL (Extract, Transform, Load) pipeline using a messy retail dataset.

The pipeline takes raw Superstore sales data, performs data cleaning and transformation using Python, and loads the cleaned data into PostgreSQL for analysis.

This project was built to practice real-world data engineering concepts such as:

* Data extraction
* Data cleaning
* Handling missing values
* Feature engineering
* PostgreSQL integration
* SQL analysis queries
* Project structuring

---

## Project Objective

The main objective of this project is to simulate a real-world data engineering workflow where raw and messy business data is cleaned, standardized, validated, and loaded into a database for reporting and analytics.

---

## Dataset Used

Dataset: Superstore Sales Dataset

The dataset contains information related to:

* Orders
* Customers
* Products
* Cities and regions
* Sales
* Profit
* Shipping details

The original dataset was intentionally made messy by adding:

* Missing values
* Duplicate rows
* Inconsistent text formatting
* Missing city and postal code values
* Missing sales and profit values
* Incorrect ship modes

---

## Project Architecture

```text
Raw CSV File
      ↓
Extract Phase
      ↓
Transform Phase
      ↓
Cleaned CSV File
      ↓
Load Phase
      ↓
PostgreSQL Database
      ↓
SQL Analysis Queries
```

---

## Folder Structure

```text
superstore-etl-project/
│
├── data/
│   ├── Superstore_Messy.csv
│   └── Superstore_Final_Cleaned.csv
│
├── scripts/
│   ├── extract.py
│   ├── transform.py
│   └── load.py
│
├── sql/
│   └── queries.sql
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Technologies Used

* Python
* Pandas
* NumPy
* PostgreSQL
* SQLAlchemy
* Psycopg2
* SQL
* Git
* GitHub

---

## Extract Phase

In the extract phase:

* Raw CSV file is read using Pandas
* Dataset shape is checked
* Column names are inspected
* Missing values are identified
* Data types are reviewed

---

## Transform Phase

The transform phase contains the main data cleaning logic.

### Cleaning Steps Performed

* Removed duplicate rows
* Standardized column names
* Removed unnecessary columns
* Filled missing customer names
* Filled missing city values using postal code
* Filled missing postal codes using city
* Replaced remaining missing city values with 'Unknown City'
* Replaced remaining postal code values with -1
* Calculated unit price using sales and quantity
* Estimated missing sales using:

  * Product-level average unit price
  * Sub-category average unit price
* Ensured sales values were not lower than profit values
* Calculated profit margin
* Estimated missing profit values using:

  * Product-level profit margin
  * Sub-category profit margin
* Converted order and ship dates into datetime format
* Calculated shipping days
* Removed invalid shipping records
* Standardized ship mode values

---

## Load Phase

In the load phase:

* Cleaned CSV file is read
* Connection is established with PostgreSQL
* Cleaned data is loaded into PostgreSQL table
* Table is created automatically using Pandas and SQLAlchemy

---

## PostgreSQL Connection

The project uses SQLAlchemy to connect Python with PostgreSQL.

Example connection string:

```python
engine = create_engine(
    "postgresql://postgres:your_password@localhost:5433/superstore_db"
)
```

---

## SQL Analysis Queries

Some example SQL queries used after loading data:

### Total Sales

```sql
SELECT SUM(sales)
FROM superstore;
```

### Top 10 Products by Sales

```sql
SELECT product_name, SUM(sales) AS total_sales
FROM superstore
GROUP BY product_name
ORDER BY total_sales DESC
LIMIT 10;
```

### Monthly Sales Trend

```sql
SELECT 
    DATE_TRUNC('month', order_date::date) AS month,
    SUM(sales) AS total_sales
FROM superstore
GROUP BY month
ORDER BY month;
```

### Top Cities by Profit

```sql
SELECT city, SUM(profit) AS total_profit
FROM superstore
GROUP BY city
ORDER BY total_profit DESC
LIMIT 10;
```

### Average Shipping Days by Ship Mode

```sql
SELECT ship_mode, AVG(shipping_days) AS avg_shipping_days
FROM superstore
GROUP BY ship_mode;
```

---

## Key Business Insights

* Standard Class is the most commonly used shipping mode
* Some products generate negative profit despite having high sales
* Certain cities contribute significantly more profit than others
* High discounts often lead to negative profit
* Shipping times vary significantly across ship modes

---

## How to Run the Project

### Step 1

Clone the repository

```bash
git clone https://github.com/yourusername/superstore-etl-project.git
```

### Step 2

Install required libraries

```bash
pip install -r requirements.txt
```

### Step 3

Run extract script

```bash
python scripts/extract.py
```

### Step 4

Run transform script

```bash
python scripts/transform.py
```

### Step 5

Run load script

```bash
python scripts/load.py
```

---

## Future Improvements

* Add Apache Airflow for orchestration
* Add logging and error handling
* Add Docker support
* Add cloud storage integration
* Add automated testing
* Add dashboard using Power BI or Tableau
* Add Spark for large-scale processing

---

## Author

Mahir Sama

Aspiring Data Engineer
