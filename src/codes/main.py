import subprocess
import os
import shutil
import numpy as np
import pandas as pd
import os
from datetime import datetime as dt
import plotly.graph_objs as go
from functions import *
from pytube import YouTube
import streamlit as st


import warnings
warnings.simplefilter('ignore')


url = st.text_input(label='URLを入力してね')
url=url.strip()

if len(url) < 5:
        st.warning('URLが入力されていません')
        # 条件を満たないときは処理を停止する
        st.stop()
else:
    name=url.split("https://www.youtube.com/watch?v=")[1]

    # コメントスクレイピング
    is_file = os.path.isfile("../txt/"+name+".txt")
    if is_file:
        pass
    else:
        subprocess.run(['videochatget',url]) 
    
    

    is_file = os.path.isfile(name+".txt")
    if is_file:
        shutil.move(name+".txt","../txt/"+name+".txt")
    else:
        pass 
        
    is_file = os.path.isfile('../csv/'+name+'.csv')
    if is_file:
        pass
    else:
        # csvファイル作成
        subprocess.run(['ruby','get_data.rb',name]) 


    df=process_csv('../csv/'+name+'.csv')
    ts=df['num']
    outlier=make_outlier(ts)

    df=df.reset_index()
    print(df)


    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df["num"], name='コメント数'))
    fig.add_trace(go.Scatter(x=outlier['timestamp'], y=outlier["num"],name="盛り上がり",mode = 'markers'))

    st.write()
    st.dataframe(outlier)
    st.plotly_chart(fig)


    
