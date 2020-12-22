import pandas as pd
import numpy as np

from scipy.stats import linregress

import os

def _slope_and_intercept_calc(df,first_date):
    df['days'] = (df.index - first_date).days + 1
    df['log10_days'] = np.log10(df['days'])
    df['log10_mortality'] = np.log10(df['mortality'])

    df = df.drop(['fips','cases'],axis=1)
    X = df.loc[:,'log10_days']
    Y = df.loc[:,'log10_mortality']

    # Building the model
    slope, intercept, r_value, p_value, std_err = linregress(df['log10_days'],df['log10_mortality'])

    df['slope'] = slope
    df['intercept'] = intercept
    df['r_value'] = r_value
    df['p_value'] = p_value
    df['std_err'] = std_err

    return df

def county_slope_and_intercept(days,n,filter):
    if not os.path.exists(f"processed_data/slope_intercept"):
        os.makedirs(f"processed_data/slope_intercept")

    df1 = pd.read_csv(f'processed_data/state_mortality_ratio_1st_trigger/mortality_ratio_1st_trigger_{n}n_{filter}filter.csv',parse_dates=True, index_col='date')

    if not os.path.exists(f'processed_data/slope_intercept/days_{days}'):
        os.makedirs(f'processed_data/slope_intercept/days_{days}')
    
    if not os.path.exists(f'processed_data/slope_intercept/days_{days}/{n}n_{filter}filter'):
        os.makedirs(f'processed_data/slope_intercept/days_{days}/{n}n_{filter}filter')

    ls_calc = []

    for index, row in df1.iterrows():
        trigger_mortality_date = index
        county = row['county']
        state = row['state']

        df2 = pd.read_csv(f'processed_data/mortality_county/{state}/mortality_{county}_{state}.csv',parse_dates=True, index_col='date')
        
        first_mortality_date = df2.index[0]
        latest_data_date = df2.index[-1]
        
        df2 = df2[df2.index> trigger_mortality_date]

        if df2.shape[0]>(days-1):
            # Takes the data from last <days>
            df2 = df2.iloc[-days:]
            df = _slope_and_intercept_calc(df2,first_mortality_date)
            df['trigger_mortality'] = trigger_mortality_date
            df['first_mortality'] = first_mortality_date

            df.to_csv(f'processed_data/slope_intercept/days_{days}/{n}n_{filter}filter/slope_intercept_{days}days_{n}n_{filter}filter_{county}_{state}.csv',index_label='date', header=True)
            
            slope = df['slope'].values[0]
            intercept = df['intercept'].values[0]
            r_value = df['r_value'].values[0]
            p_value = df['p_value'].values[0]
            std_err = df['std_err'].values[0]

            ls_calc.append([county,state,first_mortality_date,trigger_mortality_date,latest_data_date,slope,intercept,r_value,p_value,std_err])


    df_calc = pd.DataFrame(ls_calc,columns=['county','state','first_mortality','trigger_mortality','latest_data_date','slope','intercept','r_value','p_value','std_err'])
    df_calc.to_csv(f'processed_data/slope_intercept/days_{days}/{n}n_{filter}filter/slope_intercept_{days}days_{n}n_{filter}filter_all.csv',index=False, header=True)

if __name__ == "__main__":
    filters = [1.5,2.1,2.5]
    for days in range(3,9):
        for filter in filters:
            for n in range(1,8):
                county_slope_and_intercept(days,n,filter)