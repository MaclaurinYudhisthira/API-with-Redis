import pandas as pd

df = pd.read_csv('./data.csv')

df_sorted = df.sort_values(by='sts')

print(df_sorted.head())