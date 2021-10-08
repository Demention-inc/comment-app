import pandas as pd
import subprocess
from io import BytesIO
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))#親ディレクトリをパスに追加
from datetime import datetime as dt
import plotly.graph_objs as go
from functions import *
from pytube import YouTube
from google.cloud import storage as gcs
from google.oauth2 import service_account
import json
import streamlit as st
import firebase_admin
from firebase_admin import credentials, initialize_app, storage
from secret.secret import key,bucket_name,project_id

import warnings
warnings.simplefilter('ignore')


url = st.text_input(label='URLを入力してね')
url=url.strip()

if  url.split("=")[0] != 'https://www.youtube.com/watch?v':

    st.warning('youtubeのURLを入力してください')
    # 条件を満たないときは処理を停止する
    st.stop()
else:
    video_id=url.split("https://www.youtube.com/watch?v=")[1]
    # url='https://www.youtube.com/watch?v=oPDqWGXwoPA'
    # video_id='oPDqWGXwoPA'
    csv_name=video_id+'.csv'
    # firebaseにチャットデータのcsvファイルがなければ取得してアップロード
    credential = service_account.Credentials.from_service_account_info(key)
    client = gcs.Client(project_id, credentials=credential)
    bucket = client.get_bucket(bucket_name)
    box=[]
    for file in client.list_blobs(bucket_name):
        box.append(file.name)
    if csv_name in box:
        pass
    else:
        subprocess.run(['python','continuation_livechat_crawler/run.py',url])

    # firebaseからcsvファイルを取ってくる
    cred = credentials.Certificate(key)

    if not firebase_admin._apps:
            # 初期済みでない場合は初期化処理を行う
            initialize_app(cred, {'storageBucket': bucket_name})
    bucket = storage.bucket()
    blob = bucket.blob(csv_name)

    #何秒ごとに集計するか
    number=30
    #移動平均の時間
    # 平均から標準偏差の threshold 倍以上外れているデータを外れ値としてプロットする
    ewm_span=60
    threshold=2
    # df = pd.read_csv(BytesIO(blob.download_as_string()),index_col=False)
    if 'db' not in st.session_state:
        st.session_state['db'] = pd.read_csv(BytesIO(blob.download_as_string()),index_col=False)
    df_new=st.session_state['db'].rename(columns={'time':'timestamp'})
    df_new=df_new[['timestamp']]
    df_new=process_df(df_new,number)
    ts=df_new['num']
    outlier=make_outlier(ts,ewm_span, threshold)
    print(df_new)
    print(outlier)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_new.index, y=df_new["num"], name='コメント数'))
    fig.add_trace(go.Scatter(x=outlier['timestamp'], y=outlier["num"],name="盛り上がり",mode = 'markers'))

    st.write()
    st.dataframe(outlier)
    st.plotly_chart(fig)


    
