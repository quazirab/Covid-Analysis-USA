import pandas as pd
import numpy as np

def state_seperator():
    df1 = pd.read_csv(r'covid-19-data/us-counties.csv')

    # Generate by county
    states = df1['state'].unique()

    for state in states:
        df2 = df1[ (df1['state'] == state) & (df1['deaths'] > 0 )]
        if not df2.empty:
            df2.to_csv(f'processed_data/deaths_state/{state}.csv',index = False, header=True)


def county_seperator():
    df1 = pd.read_csv(r'covid-19-data/us-counties.csv')

    # Generate by county
    states = df1['state'].unique()
    for state in states:
        df2 = df1[ (df1['state'] == state) & (df1['deaths'] > 0 )]
            
        if not df2.empty:
            # Generate by county
            counties = df2['county'].unique()

            for county in counties:
                df3 = df2[(df2['county'] == county) & (df2['deaths'] > 0 )]
                if not df3.empty:
                    df3.to_csv(f'processed_data/deaths_county/deaths_{county}_{state}.csv',index = False, header=True)

if __name__ == "__main__":
    county_seperator()