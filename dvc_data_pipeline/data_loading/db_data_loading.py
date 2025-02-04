import pandas as pd
from sqlalchemy import create_engine,inspect
from dotenv import load_dotenv
import os

def table_exists(engine,table_name):
    inspector = inspect(engine)
    return table_name in inspector.get_table_names()

def get_next_vesion(engine,base_table_name):
    version = 0
    while True:
        version += 1
        table_name = f"{base_table_name}V{version}"
        if not table_exists(engine,table_name):
            return table_name
def main(dataframe):
    load_dotenv()    

    df = dataframe

    # Database connection details
    rds_host = os.getenv('rds_host')
    username = os.getenv('rds_username') 
    password = os.getenv('password')  
    database_name = os.getenv('database_name') 
    port = os.getenv('port') 
    base_table_name = os.getenv('base_table_name')
    # Establish a connection to your RDS instance (PostgreSQL example, change accordingly for MySQL)
    connection_string = f'postgresql+psycopg2://{username}:{password}@{rds_host}:{port}/{database_name}'
    # Create a database engine using SQLAlchemy
    engine = create_engine(connection_string)
    table_name = get_next_vesion(engine,base_table_name)

    # Push DataFrame to a table in the database (replace 'your_table' with your actual table name)
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)

    print(f"Data has been successfully pushed to the RDS instance. with table name {table_name}")
    return f"Data has been successfully pushed to the RDS instance. with table name {table_name}"

# df = pd.read_csv('./CSV_data/Walmart_split_subset_1.csv')
# main('test',df)
# df = pd.read_csv('./CSV_data/Walmart_split_subset_1.csv')
# main('test',df)
