import pandas as pd
import numpy as np
import os

def daily_mortality():

    if not os.path.exists(f"processed_data/mortality_county"):
            os.makedirs(f"processed_data/mortality_county")

    df1 = pd.read_csv(r'covid-19-data/us-counties.csv',parse_dates=True, index_col='date')
    df1 = df1.rename(columns={'deaths':'mortality'})

    # Generate by county
    states = df1['state'].unique()

    for state in states:
        if not os.path.exists(f"processed_data/mortality_county/{state}"):
            os.makedirs(f"processed_data/mortality_county/{state}")

        df2 = df1[ (df1['state'] == state) & (df1['mortality'] > 0 )]
        
        counties = df2['county'].unique()
        
        df = []
        

        for county in counties:
            df3 = df2[ (df2['county'] == county)]
            df3['new_mortality']  = df3['mortality'].sub(df3['mortality'].shift())
            
            if not df3.empty:
                df3['new_mortality'].iloc[0] = df3['mortality'].iloc[0]
                df3['new_mortality'] = df3['new_mortality'].astype(int)

                df3.to_csv(f'processed_data/mortality_county/{state}/mortality_{county}_{state}.csv',index_label = 'date', header=True)
            df.append(df3)
        
        if len(df)>0:
            df2 = pd.concat(df)
            df2.to_csv(f'processed_data/mortality_county/{state}/{state}.csv',index_label = 'date', header=True)
        


if __name__ == "__main__":
    daily_mortality()