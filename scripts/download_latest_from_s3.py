import os
import logging
import boto3
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError, ClientError

logger = logging.getLogger(__name__)
load_dotenv()


def download_latest_from_s3(prefix="raw/", local_dir="/opt/airflow/data"):
    try:
        s3 = boto3.client('s3')
        bucket_name = os.getenv("AWS_S3_BUCKET")

        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        all_files = response.get("Contents")

        if not all_files:
            logger.warning("No files found in S3 with prefix %s", prefix)
            return

        latest_file = max(all_files, key=lambda x: x['LastModified'])
        s3_key = latest_file['Key']

        filename = os.path.basename(s3_key)
        local_file_path = os.path.join(local_dir, filename)

        s3.download_file(bucket_name, s3_key, local_file_path)

        logger.info("Downloaded latest file: %s to %s", s3_key, local_file_path)

    except (NoCredentialsError, ClientError) as e:
        logger.error("AWS error: %s", e)
    except Exception as e:
        logger.error("Unexpected error during latest file download.", exc_info=True)
