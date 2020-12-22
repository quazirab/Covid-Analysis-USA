import pandas as pd
import numpy as np
from datetime import timedelta
import os

import matplotlib.pyplot as plt
plt.style.use('classic')
import matplotlib.dates as mdates

def projection(days,n,filter,proection_days):

    if not os.path.exists(f"processed_data/mortality_projection"):
            os.makedirs(f"processed_data/mortality_projection")

    df1 = pd.read_csv(f'processed_data/slope_intercept/days_{days}/{n}n_{filter}filter/slope_intercept_{days}days_{n}n_{filter}filter_all.csv')
    
    df1['trigger_mortality'] = pd.to_datetime(df1['trigger_mortality'])
    df1['first_mortality'] = pd.to_datetime(df1['first_mortality'])
    df1['latest_data_date'] = pd.to_datetime(df1['latest_data_date'])


    for index, row in df1.iterrows():

        if not os.path.exists(f"processed_data/mortality_projection/{row['state']}/{row['county']}"):
            os.makedirs(f"processed_data/mortality_projection/{row['state']}/{row['county']}")
        

        starting_day = (row['latest_data_date'])
        end_day = starting_day+timedelta(days=21)

        df2 = pd.DataFrame(columns=['projected_mortality','days_since_first_mortality','log_days','log_mortality'],index = pd.date_range(start=starting_day,end=end_day))       
        import matplotlib.dates as mdates
        df2['days_since_first_mortality'] = (df2.index - row['first_mortality']).days + 1
        df2['log_days']  = np.log10(df2['days_since_first_mortality'])
        df2['log_mortality'] = row['slope']*df2['log_days'] + row['intercept']
        df2['projected_mortality'] = np.power(10,df2['log_mortality'])

        df2.to_csv(f"processed_data/mortality_projection/{row['state']}/{row['county']}/mortality_projection_{row['county']}_{row['state']}_{days}days_{n}n_{filter}filter.csv",index_label='date', header=True)

def graph_projection_all():

    states = os.listdir('processed_data/mortality_projection/')
    
    fig, ax = plt.subplots()
    for state in states:
        counties = os.listdir(f'processed_data/mortality_projection/{state}')
        for county in counties:
            files = os.listdir(f'processed_data/mortality_projection/{state}/{county}')
            plt.xlabel('Date', fontsize=18)
            plt.ylabel('mortality', fontsize=16)
            fig.suptitle(f'{county}, {state} - Projection', fontsize=22)
            

            df1 = pd.read_csv(f'processed_data/mortality_county/{state}/mortality_{county}_{state}.csv',parse_dates=True, index_col='date')
            ax.plot(df1.index,df1['mortality'],label='real_mortality')
            
            for file in files:
                if file.endswith('.csv'):
                    df1 = pd.read_csv(f'processed_data/mortality_projection/{state}/{county}/{file}',parse_dates=True, index_col='date')
                    label = 'projection_'+file[-22:-4]
                    
                    ax.plot(df1.index,df1['projected_mortality'],label=label)
            
            ax.legend(fontsize=10,bbox_to_anchor=(1, 1),loc='upper left',ncol=2)
            ax.set_ylim(ymin=0)
            ax.xaxis.set_major_locator(mdates.DayLocator(interval = 7))
            ax.xaxis.set_minor_locator(mdates.DayLocator(interval = 1))
            plt.grid(which='major')
            fig.set_size_inches(25, 15)
            fig.tight_layout()
            fig.savefig(f'processed_data/mortality_projection/{state}/{county}/{county}_{state}_projection_graph.png',pad_inches=0)
            plt.cla()
            

if __name__ == "__main__":
    filters = [1.5,2.1,2.5]

    for days in range(3,9):
        for filter in filters:
            for n in range(1,8):
                projection(days,n,filter,21)

    # graph_projection_all()