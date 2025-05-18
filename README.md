
# 📰 News ETL Pipeline Project

This is an end-to-end ETL (Extract, Transform, Load) data pipeline that:
- **Fetches news data** from the News API
- **Stores raw data** in AWS S3 (or local storage)
- **Cleans/transforms the data** using Databricks
- **Loads cleaned data** into PostgreSQL
- **Orchestrates** all steps using Apache Airflow

---

## 🚀 Tech Stack

| Layer          | Technology Used             |
|----------------|-----------------------------|
| Orchestration  | Apache Airflow (Dockerized) |
| Ingestion      | News API + Python           |
| Storage        | AWS S3                      |
| Processing     | Databricks (PySpark)        |
| Load           | PostgreSQL                  |
| Logging        | Python `logging` module     |
| Containerization | Docker + Docker Compose   |

---

## 📁 Folder Structure

```
news_etl_pipeline/
├── dags/
│   └── news_ingestion_dag.py        # Airflow DAG
├── data/
│   └── cleaned_data/                # Output from Databricks
├── scripts/
│   ├── fetch_news.py                # News API data fetcher
│   ├── upload_to_s3.py              # Uploads raw JSON to S3
│   ├── download_from_s3.py          # Downloads for cleaning
│   └── load_news_to_postgres.py     # Loads cleaned CSV to Postgres
├── requirements.txt
├── docker-compose.yaml
├── .env.example
└── README.md
```

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/news_etl_pipeline.git
cd news_etl_pipeline
```

### 2. Setup Environment Variables

Rename `.env.example` to `.env` and set your credentials:

```env
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_db
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_S3_BUCKET=news-data-bucket
```

### 3. Start Dockerized Services

```bash
docker compose up --build
```

This starts:
- Postgres
- pgAdmin (http://localhost:5050)
- Airflow Web UI (http://localhost:8080)

---

## 🔁 Airflow Pipeline

The DAG runs the following steps:

1. **fetch_news** – Fetches JSON data from News API
2. **upload_to_s3** – Uploads raw data to S3
3. **download_from_s3** – Downloads data for processing
4. **clean_and_save (Databricks)** – Spark job cleans and saves as CSV
5. **load_to_postgres** – Loads cleaned data into PostgreSQL

You can trigger the DAG from the Airflow UI or manually for testing.

---

## 🧪 Sample Test Run

After starting all services:
- Place a CSV into `data/cleaned_data/` or use Databricks output
- Run the DAG
- Check `news_cleaned` table in PostgreSQL using pgAdmin

---

## 📊 Reporting Ideas (Optional)

You can add:
- Power BI / Tableau dashboards reading from PostgreSQL
- Email summary reports using Airflow email operator

