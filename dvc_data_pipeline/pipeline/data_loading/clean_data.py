import pandas as pd

def clean_data(df):
    # def clean_data(file_path):
    print(df)
    print("Columns:", df.columns)
    df.Date = pd.to_datetime(df['Date'], format='%d-%m-%Y')
    df['weekday'] = df.Date.dt.weekday
    df['month'] = df.Date.dt.month
    df['year'] = df.Date.dt.year
    df.drop(['Date'],axis = 1,inplace = True)

    target = 'Weekly_Sales'
    original_df = df.copy(deep=True)
    return original_df