import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from logger_config import get_logger
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize logger
logger = get_logger(__name__)

def load_data_to_postgres():
    try:
        # Path should be valid inside Airflow Docker container
        csv_path = "/opt/airflow/data/cleaned_data/part-00000-tid-1122251859516882938-e850a3c6-8fca-4e84-ae0b-4e1621caebda-8-1-c000.csv"

        # Check if CSV file exists
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found at: {csv_path}")

        logger.info(f"Found CSV file at: {csv_path}")

        # Load CSV into DataFrame
        df = pd.read_csv(csv_path)
        logger.info(f"Loaded CSV with {len(df)} rows and {len(df.columns)} columns.")

        if df.empty:
            raise ValueError("CSV is empty. Aborting.")

        # Get environment variables
        pg_user = os.getenv("POSTGRES_USER")
        pg_password = os.getenv("POSTGRES_PASSWORD")
        pg_port = os.getenv("POSTGRES_PORT")
        pg_host = os.getenv("POSTGRES_HOST")
        pg_db = os.getenv("POSTGRES_DB")

        # Construct database URL
        db_url = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"
        engine = create_engine(db_url)

        # Load DataFrame into PostgreSQL
        df.to_sql("news_cleaned", engine, if_exists="replace", index=False)
        logger.info("Data successfully loaded into PostgreSQL table: news_cleaned")

    except FileNotFoundError as fe:
        logger.error(f"FileNotFoundError: {fe}")
        raise
    except ValueError as ve:
        logger.error(f"ValueError: {ve}")
        raise
    except SQLAlchemyError as se:
        logger.error(f"SQLAlchemyError: {se}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise

if __name__ == "__main__":
    load_data_to_postgres()
