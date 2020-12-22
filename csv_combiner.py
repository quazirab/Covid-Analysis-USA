import os
import pandas as pd

def mortality_combined():
    state_dataframe_list = []
    
    for state in os.listdir("processed_data/mortality_county"):
        
        if os.path.exists(f'processed_data/mortality_county/{state}/{state}.csv'):
            df_state = pd.read_csv(f'processed_data/mortality_county/{state}/{state}.csv',index_col='date',parse_dates=True)
            
            if os.path.exists(f'processed_data/mortality_projection/{state}'):
                for county in os.listdir(f"processed_data/mortality_projection/{state}"):
                    if county != 'Unknown':
                        for file in os.listdir(f"processed_data/mortality_projection/{state}/{county}"):
                            if file.endswith('.csv'):
                                df_county = pd.read_csv(f'processed_data/mortality_projection/{state}/{county}/{file}',index_col='date',parse_dates=True)
                                
                                filter_days = int(file[file.find('days')-1:file.find('days')])
                                filter_shift = int(file[file.rfind('n_')-1:file.rfind('n_')])
                                filter_trigger = float(file[file.rfind('filter')-3:file.rfind('filter')])
                                
                                # Drop columns
                                # df_county= df_county.drop(['days_since_first_death','log_days','log_mortality'],axis=1)

                                df_county['filter_days'] = filter_days
                                df_county['filter_shift'] = filter_shift
                                df_county['filter_trigger'] = filter_trigger
                                df_county['county'] = county
                                df_county['state'] = state
                                df_county['fips'] = df_state.loc[ (df_state['state'] == state) & (df_state['county'] == county) ]['fips'][0]
                                df_state = df_state.append(df_county)

            state_dataframe_list.append(df_state)

    df = pd.concat(state_dataframe_list)
    df.to_csv(f'processed_data/mortality_projection_all_state.csv',index_label = 'date', header=True)

if __name__ == "__main__":
    mortality_combined()