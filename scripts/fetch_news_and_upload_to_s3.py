import requests
import json
from datetime import datetime
import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import ClientError
from logger_config import get_logger

logger = get_logger(__name__)
load_dotenv()

def fetch_news():
    try:
        api_key = os.getenv("NEWS_API_KEY")
        if not api_key:
            raise ValueError("NEWS_API_KEY not found in environment.")

        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
        response = requests.get(url)
        response.raise_for_status()

        news_data = response.json()
        logger.info(f"Fetched {len(news_data.get('articles', []))} articles from API.")
        return news_data
    except Exception as e:
        logger.exception("Error fetching news from API.")
        raise

def upload_json_to_s3(data, s3_key):
    try:
        bucket_name = os.getenv("AWS_S3_BUCKET")
        aws_region = os.getenv("AWS_REGION")

        s3 = boto3.client(
            's3',
            region_name=aws_region,
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
        )

        s3.put_object(Bucket=bucket_name, Key=s3_key, Body=json.dumps(data))
        logger.info(f"Uploaded news JSON to s3://{bucket_name}/{s3_key}")
    except ClientError as e:
        logger.error(f"S3 upload failed: {e}")
        raise
    except Exception as e:
        logger.exception("Unexpected error during S3 upload.")
        raise

def fetch_and_upload_to_s3():
    """Main function used by Airflow to fetch news and upload to S3."""
    try:
        news_data = fetch_news()
        timestamp = datetime.utcnow().strftime('%Y_%m_%dT%H_%M_%S')
        s3_key = f"raw/news_{timestamp}.json"
        upload_json_to_s3(news_data, s3_key)
    except Exception as e:
        logger.error("Failed to fetch and upload news data.")
        raise

if __name__ == "__main__":
    fetch_and_upload_to_s3()
