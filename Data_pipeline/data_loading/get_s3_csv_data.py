import boto3
import pandas as pd
from io import StringIO
from dotenv import load_dotenv
import os
def get_s3_csv_data():
    load_dotenv()
    try:
        aws_access_key = os.getenv('aws_access_key_id')
        aws_region_name = os.getenv('region_name')
        aws_secret_access_key = os.getenv('aws_secret_access_key')
        bucket_name = os.getenv('bucket_name')

        s3_client = boto3.client('s3',
                                aws_access_key_id = aws_access_key,
                                aws_secret_access_key = aws_secret_access_key,
                                region_name=aws_region_name
                                )


        response = s3_client.list_objects_v2(Bucket = bucket_name)
        dfs = []
        for obj in response.get('Contents',[]):
            file_key = obj['Key']
            if file_key.endswith('.csv'):
                file_obj = s3_client.get_object(Bucket = bucket_name,Key = file_key)
                csv_data = file_obj['Body'].read().decode('utf-8')
                csv_buffer = StringIO(csv_data)
                df = pd.read_csv(csv_buffer)
                dfs.append(df)
        if len(dfs) > 1:
            columns = [set(df.columns) for df in dfs]
            if all(columns[0] == col_set for col_set in columns):
                # Merge the DataFrames if columns match
                merged_df = pd.concat(dfs, ignore_index=True)
                return merged_df
            else:
                raise ValueError("Columns do not match across all CSV files!")
        return df[0]
    except Exception as e:
        return "unknown Exception {e} occured"
    
