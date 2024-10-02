import pandas as pd
if True:
    dfs = pd.read_excel('input/online_retail_II.xlsx', sheet_name= None)
    df = pd.concat(dfs)
    for col in ['Invoice', 'StockCode', 'Description']:
        df[col] = df[col].astype('str')
    df['Customer ID'] = df['Customer ID'].astype('Int64')
    df.to_parquet('output/transaction_df.parquet')
else:
    df = pd.read_parquet('output/transaction_df.parquet')



customer_ids = list(df[~pd.isna(df['Customer ID'])]['Customer ID'].astype('int64').unique())

health_df = pd.read_csv('input/diabetes_prediction_dataset.csv')

customer_df = pd.DataFrame(index = range(len(customer_ids)))

customer_df['Customer ID'] = customer_ids

customer_df = pd.concat([customer_df, health_df.sample(len(customer_df)).reset_index()], axis = 1)

import numpy as np

customer_df['Education'] = np.random.randint(3, size = (len(customer_df), 1))

customer_df['Education'] = customer_df['Education'].map({0: 'High School', 1: 'Associates', 2: 'Bachelors', 3 : 'Masters', 4 : 'PhD'})

print(customer_df)

customer_df.to_csv('output/Customers.csv', index = False)