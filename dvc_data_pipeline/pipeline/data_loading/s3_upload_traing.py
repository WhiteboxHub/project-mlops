import pandas as pd
from dotenv import load_dotenv
import os
import boto3
import io

def main(df):
    load_dotenv()
    # try:
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_region_name = os.getenv('AWS_REGION')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    bucket_name = os.getenv('BUCKET_NAME')
    Training_data_prefix = 'training_data/v'

    s3_client = boto3.client('s3',
                                aws_access_key_id = aws_access_key,
                                aws_secret_access_key = aws_secret_access_key,
                                region_name=aws_region_name
                                )
    
    existing_files = s3_client.list_objects_v2(Bucket = bucket_name,Prefix = "training_data/")
    existing_versions = []

    if 'Contents' in existing_files:
        for obj in existing_files['Contents']:
            key = obj['Key']
            if key.startswith(Training_data_prefix) and key.endswith('.csv'):
                version_number = key.replace(Training_data_prefix,"").replace(".csv","")
                if version_number.isdigit():
                    existing_versions.append(int(version_number))

    next_version = max(existing_versions,default=0) + 1

    Cleaned_file_key = f"{Training_data_prefix}{next_version}.csv"

    # using buffer to store cleaned csv without saving the file.
    csv_buffer = io.StringIO()

    df.to_csv(csv_buffer,index=False)
    s3_client.put_object(Bucket=bucket_name,Key=Cleaned_file_key,Body =csv_buffer.getvalue())

    print(f"Data cleaned and uploaded to S3 as {Cleaned_file_key}")
