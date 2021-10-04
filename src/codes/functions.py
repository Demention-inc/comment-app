
import numpy as np
import pandas as pd
import os
from matplotlib import pyplot as plt
import seaborn as sns
from datetime import datetime as dt
from datetime import timedelta

def process_csv(csv):
    df=pd.read_csv(csv).drop('id',axis=1)
    df['num']=1
    for n in range(len(df['timestamp'])):
        if df['timestamp'][n][0]=='-':
            df= df.drop(index=n)
    df=df.reset_index(drop=True)
    for n in range(len(df['timestamp'])):
        if len(df['timestamp'][n])==4:
            df['timestamp'][n]='0:'+'0'+df['timestamp'][n]
        elif len(df['timestamp'][n])==5:
            df['timestamp'][n]='0:'+df['timestamp'][n]
        elif len(df['timestamp'][n])==8:
            df['timestamp'][n]='0:'+df['timestamp'][n][0:5]
    df1=df.groupby('timestamp',as_index=False).sum()
    df1['timestamp']= pd.to_datetime(df1['timestamp']) #datetime型にする
    df1=df1.groupby(pd.Grouper(key='timestamp', freq='30s')).sum().reset_index()
    df1['timestamp'] = df1['timestamp'].dt.strftime('%H:%M:%S')
    df=df1.set_index('timestamp')
    return df

def make_outlier(ts, ewm_span=30, threshold=1.5):
    assert type(ts) == pd.Series
    ewm_mean = ts.ewm(span=ewm_span).mean()  # 指数加重移動平均
    ewm_std = ts.ewm(span=ewm_span).std()  # 指数加重移動標準偏差
    outlier = ts[(ts - ewm_mean)> ewm_std * threshold]
    outlier=outlier.reset_index().sort_values('num',ascending=False)
    return outlier
