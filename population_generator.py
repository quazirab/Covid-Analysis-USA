import pandas as pd

df1 = pd.read_csv(f'population-data/co-est2019-annres.csv')

df1['county'], df1['state'] = df1['Geographic Area'].str.split(' ', 1).str
df1 = df1.replace(to_replace=r'County, ', value='', regex=True)
df1 = df1.replace(to_replace='\.', value='', regex=True)
df1 = df1.replace(to_replace='\,', value='', regex=True)

df1['population'] = df1['2019'].astype(int)

df1 = df1[['county','state','population']]

df1.to_csv(f'population-data/population_county.csv',index=False, header=True)
