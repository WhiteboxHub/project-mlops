import numpy as np
import pandas as pd

def ready_data_for_training(dataframe):
    df = dataframe
    target = 'Weekly_Sales'
    features = [i for i in df.columns if i not in [target]]
    nu = df[features].nunique().sort_values()
    nf = [] ; cf = [] ; nnf = 0 ; ncf = 0;
    for i in range(df[features].shape[1]):
        if nu.values[i] <= 45:cf.append(nu.index[i])
        else: nf.append(nu.index[i])
    df.drop_duplicates(inplace=True)
    #Check for empty elements

    nvc = pd.DataFrame(df.isnull().sum().sort_values(), columns=['Total Null Values'])
    nvc['Percentage'] = round(nvc['Total Null Values']/df.shape[0],3)*100
    df3 = df.copy()
        
        
    ecc = nvc[nvc['Percentage']!=0].index.values
    fcc = [i for i in cf if i not in ecc]
    #One-Hot Binay Encoding
    oh=True
    dm=True
    for i in fcc:
        #print(i)
        if df3[i].nunique()==2:
            if oh==True: print("\033[1mOne-Hot Encoding on features:\033[0m")
            print(i);oh=False
            df3[i]=pd.get_dummies(df3[i], drop_first=True, prefix=str(i))
        if (df3[i].nunique()>2):
            if dm==True: print("\n\033[1mDummy Encoding on features:\033[0m")
            print(i);dm=False
            df3 = pd.concat([df3.drop([i], axis=1), pd.DataFrame(pd.get_dummies(df3[i], drop_first=True, prefix=str(i)))],axis=1)
    

    df1 = df3.copy()

    #features1 = [i for i in features if i not in ['CHAS','RAD']]
    features1 = nf

    for i in features1:
        Q1 = df1[i].quantile(0.25)
        Q3 = df1[i].quantile(0.75)
        IQR = Q3 - Q1
        df1 = df1[df1[i] <= (Q3+(1.5*IQR))]
        df1 = df1[df1[i] >= (Q1-(1.5*IQR))]
        df1 = df1.reset_index(drop=True)
    df = df1.copy()
    df.columns=[i.replace('-','') for i in df.columns]

    return df
