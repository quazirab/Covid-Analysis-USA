import pandas as pd
import numpy as np
import os

def mortality_ratio(n,filter=1,all=0):

    if not os.path.exists(f"processed_data/mortality_ratio"):
            os.makedirs(f"processed_data/mortality_ratio")

    df1 = pd.read_csv(r'covid-19-data/us-counties.csv',parse_dates=True, index_col='date')
    df1 = df1.rename(columns={'deaths':'mortality'})

    # Generate by county
    states = df1['state'].unique()

    df_states = []

    for state in states:
        df2 = df1[ (df1['state'] == state) & (df1['mortality'] > 0 )]
        
        counties = df2['county'].unique()
        
        df_counties = []
        
        for county in counties:
            df3 = df2[ (df2['county'] == county)]
            df3[f'{n}n_ratio']  = (df3['mortality'].div(df3['mortality'].shift(n)))

            df_counties.append(df3)
        
        if len(df_counties)>0:
            df2 = pd.concat(df_counties)    
            df_states.append(df2)

    df1 = pd.concat(df_states)

    if all:

        df1.to_csv(f'processed_data/mortality_ratio/mortality_ratio_{n}n_all.csv',index_label = 'date', header=True)

    df1 = df1[ (df1[f'{n}n_ratio'] > filter )]
    df1.to_csv(f'processed_data/mortality_ratio/mortality_ratio_{n}n_{filter}filter.csv',index_label = 'date', header=True)


if __name__ == "__main__":
    for n in range(1,8):
        mortality_ratio(n,filter=1.5)
        mortality_ratio(n,filter=2.1)
        mortality_ratio(n,filter=2.5,all=1)