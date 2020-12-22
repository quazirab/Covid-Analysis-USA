import pandas as pd
import numpy as np
import os

def state_mortality_ratio_1st_trigger(n,filter=1):

    if not os.path.exists(f"processed_data/state_mortality_ratio_1st_trigger"):
        os.makedirs(f"processed_data/state_mortality_ratio_1st_trigger")

    df1 = pd.read_csv(f'processed_data/mortality_ratio/mortality_ratio_{n}n_{filter}filter.csv',parse_dates=True, index_col='date')

    df1['date'] = df1.index

    
    df1 = df1.groupby('county').first().reset_index()
    df1.sort_values('date',axis=0,ascending = True,inplace = True)

    columns = list(df1.columns)
    columns = [columns[-1]] + columns[:-1]

    df1=df1[columns]
    df1.to_csv(f'processed_data/state_mortality_ratio_1st_trigger/mortality_ratio_1st_trigger_{n}n_{filter}filter.csv',index=False,header=True)

if __name__ == "__main__":
    for n in range(1,8):
        state_mortality_ratio_1st_trigger(n,filter=1.5)
        state_mortality_ratio_1st_trigger(n,filter=2.5)
        state_mortality_ratio_1st_trigger(n,filter=2.1)