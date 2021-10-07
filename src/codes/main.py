import pandas as pd
import subprocess
from io import BytesIO
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))#親ディレクトリをパスに追加
from datetime import datetime as dt
import plotly.graph_objs as go
from functions import *
from pytube import YouTube
import streamlit as st
import firebase_admin
from firebase_admin import credentials, initialize_app, storage
from secret.secret import key,bucket_name

import warnings
warnings.simplefilter('ignore')


url = st.text_input(label='URLを入力してね')
url=url.strip()

if len(url) < 5:
        st.warning('URLが入力されていません')
        # 条件を満たないときは処理を停止する
        st.stop()
else:
    # video_id=url.split("https://www.youtube.com/watch?v=")[1]
    url='https://www.youtube.com/watch?v=IhiievWaZMI'
    video_id='IhiievWaZMI'

    # firebaseにチャットデータのcsvファイルをアップロード
    # subprocess.run(['python','continuation_livechat_crawler/run.py',url])

    # firebaseからcsvファイルを取ってくる
    cred = credentials.Certificate(key)

    if not firebase_admin._apps:
            # 初期済みでない場合は初期化処理を行う
            initialize_app(cred, {'storageBucket': bucket_name})
    bucket = storage.bucket()
    blob = bucket.blob(video_id+'.csv')

    #何秒ごとに集計するか
    number=1
    df = pd.read_csv(BytesIO(blob.download_as_string()),index_col=False)
    df=df.rename(columns={'time':'timestamp'})
    df=df[['timestamp']]
    df_new=process_df(df,number)
    ts=df_new['num']
    outlier=make_outlier(ts)
    print(df)


    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['timestamp'], y=df["num"], name='コメント数'))
    fig.add_trace(go.Scatter(x=outlier['timestamp'], y=outlier["num"],name="盛り上がり",mode = 'markers'))

    st.write()
    st.dataframe(outlier)
    st.plotly_chart(fig)


    
