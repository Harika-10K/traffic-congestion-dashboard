import pandas as pd

def load_data():
    df = pd.read_csv("data.csv")
    return df

def process_data(df):
    df['traffic_level'] = pd.cut(df['vehicle_count'],
                                bins=[0,300,700,1000],
                                labels=['Low','Medium','High'])
    return df
