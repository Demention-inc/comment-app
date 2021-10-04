import subprocess
import os
import shutil
import numpy as np
import pandas as pd
import os
from matplotlib import pyplot as plt
import seaborn as sns
from datetime import datetime as dt
from datetime import timedelta
import plotly.graph_objs as go
from functions import *
from pytube import YouTube
import streamlit as st


import warnings
warnings.simplefilter('ignore')


url = st.text_input(label='URLを入力してね')
url=url.strip()

if len(url) < 5:
        st.warning('URLを入力して')
        # 条件を満たないときは処理を停止する
        st.stop()
else:

    # コメントスクレイピング
    # subprocess.run(['videochatget',url]) 
    name=url.split("https://www.youtube.com/watch?v=")[1]
    # shutil.move(name+".txt","../../txt/"+name+".txt")

    # csvファイル作成
    # subprocess.run(['ruby','get_data.rb',name])



    df=process_csv('../../csv/'+name+'.csv')
    ts=df['num']
    outlier=make_outlier(ts)

    df=df.reset_index()
    print(df)


    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df["num"], name='コメント数'))
    fig.add_trace(go.Scatter(x=outlier['timestamp'], y=outlier["num"],name="盛り上がり",mode = 'markers'))


    st.dataframe(outlier)
    st.plotly_chart(fig)


    #動画ダウンロード
    yt = YouTube(url)
    st.subheader(yt.title )
    stream = yt.streams.filter(file_extension='mp4').first()
    next_title=name

    # stream.download("../../mp4/")
    # os.rename("../../mp4/" + yt.title + ".mp4","../../mp4/" + next_title + ".mp4")

    file_path = "../../mp4/"+next_title+'.mp4'
    for i,t in enumerate(outlier['timestamp']):
        time=t
        short_time=60
        sec=int(time[0:1])*60*60+int(time[3:5])*60+int(time[6:8])
        start = str(sec-(short_time/2))
        save_path ='../../short/'+next_title+str(i)+'.mp4'
        short_time=str(short_time)
        subprocess.run(['ffmpeg','-i',file_path,'-ss',start,'-t',short_time,save_path])

        video_file = open(save_path, 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)
