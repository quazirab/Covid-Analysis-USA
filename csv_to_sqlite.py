import pandas as pd
from sqlalchemy import create_engine
import datetime
import os

engine = create_engine(f'sqlite:///bin/{datetime.date.today()}.db')

def raw_data():
    df = pd.read_csv(f'covid-19-data/us-states.csv',index_col='date',parse_dates=True)
    df.to_sql('covid_us_states', index=True,con=engine)
    df = pd.read_csv(f'covid-19-data/us-counties.csv',index_col='date',parse_dates=True)
    df.to_sql('covid_us_counties', index=True,con=engine)

def deaths_county():
    for state in os.listdir("processed_data/deaths_county"):
        if os.path.exists(f'processed_data/deaths_county/{state}/{state}.csv'):
            df = pd.read_csv(f'processed_data/deaths_county/{state}/{state}.csv',index_col='date',parse_dates=True)
            df.to_sql(f'deaths_county',if_exists='append', index=True,con=engine)

def deaths_ratio():
    files = os.listdir("processed_data/deaths_ratio")
    files = [file for file in files if 'all' in file]
    
    first = 1

    df = None

    for file in os.listdir("processed_data/deaths_ratio"):
        if 'all' in file:
            if first:
                df = pd.read_csv(f'processed_data/deaths_ratio/{file}',index_col='date',parse_dates=True)
                first = 0
            else:
                df_new = pd.read_csv(f'processed_data/deaths_ratio/{file}',index_col='date',parse_dates=True)
                df[df_new.columns.tolist()[-1]] = df_new[df_new.columns.tolist()[-1]]
    df.to_sql(f'deaths_ratio', index=True,con=engine)

if __name__ == "__main__":
    deaths_ratio()