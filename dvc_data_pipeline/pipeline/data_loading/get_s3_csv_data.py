# import boto3
# import pandas as pd
# from io import StringIO
# from dotenv import load_dotenv
# import os
# def get_s3_csv_data():
#     load_dotenv()
#     try:
#         aws_access_key = os.getenv('aws_access_key_id')
#         aws_region_name = os.getenv('region_name')
#         aws_secret_access_key = os.getenv('aws_secret_access_key')
#         bucket_name = os.getenv('bucket_name')

#         s3_client = boto3.client('s3',
#                                 aws_access_key_id = aws_access_key,
#                                 aws_secret_access_key = aws_secret_access_key,
#                                 region_name=aws_region_name
#                                 )


#         response = s3_client.list_objects_v2(Bucket = bucket_name)
#         dfs = []
#         for obj in response.get('Contents',[]):
#             file_key = obj['Key']
#             if file_key.endswith('.csv'):
#                 file_obj = s3_client.get_object(Bucket = bucket_name,Key = file_key)
#                 csv_data = file_obj['Body'].read().decode('utf-8')
#                 csv_buffer = StringIO(csv_data)
#                 df = pd.read_csv(csv_buffer)
#                 dfs.append(df)
#         if len(dfs) > 1:
#             columns = [set(df.columns) for df in dfs]
#             if all(columns[0] == col_set for col_set in columns):
#                 # Merge the DataFrames if columns match
#                 merged_df = pd.concat(dfs, ignore_index=True)
#                 return merged_df
#             else:
#                 raise ValueError("Columns do not match across all CSV files!")
#         return df[0]
#     except Exception as e:
#         return "unknown Exception {e} occured"
    
import boto3
import pandas as pd
from io import StringIO
from dotenv import load_dotenv
import os

def get_s3_csv_data():
    load_dotenv()
    try:
        aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
        aws_region_name = os.getenv('AWS_REGION')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        bucket_name = os.getenv('BUCKET_NAME')

        s3_client = boto3.client('s3',
                                aws_access_key_id=aws_access_key,
                                aws_secret_access_key=aws_secret_access_key,
                                region_name=aws_region_name
                                )

        # List all objects in the /raw/ folder
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix='raw/')
        files = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].endswith('.csv')]
        print(files)
        dfs = []
        for obj in response.get('Contents', []):
            file_key = obj['Key']
            if file_key.endswith('.csv'):  # Ensure we're only processing CSV files
                file_obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
                
                csv_data = file_obj['Body'].read().decode('utf-8')
                csv_buffer = StringIO(csv_data)
                df = pd.read_csv(csv_buffer)
                dfs.append(df)

        if not dfs:
            raise ValueError("No CSV files found in the /raw/ folder!")

        if len(dfs) > 1:
            columns = [set(df.columns) for df in dfs]
            if all(columns[0] == col_set for col_set in columns):
                # Merge the DataFrames if columns match
                merged_df = pd.concat(dfs, ignore_index=True)
                print(merged_df)
                return merged_df
            else:
                raise ValueError("Columns do not match across all CSV files in /raw/!")
        print(f"aka {dfs[0]}")
        return dfs[0]  # Return the single dataframe if only one file is found

    except Exception as e:
        return f"Unknown exception occurred: {e}"
