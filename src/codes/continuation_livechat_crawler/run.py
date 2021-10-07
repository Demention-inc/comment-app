import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from continuation_livechat_crawler.main import get_chat_replay_from_continuation, RestrictedFromYoutube
from initial_livechat_check.main import get_initial_continuation,  ContinuationURLNotFound, LiveChatReplayDisabled, RestrictedFromYoutube
import firebase_admin
from firebase_admin import credentials, initialize_app, storage
from secret.secret import key,bucket_name
import pandas as pd
from tqdm import tqdm

if __name__ == '__main__':
    target_url=sys.argv[1]
    video_id = target_url.split("https://www.youtube.com/watch?v=")[1]
    continuation = get_initial_continuation(target_url)
    comment_data, continuation = get_chat_replay_from_continuation(video_id, continuation, 3000, True)

    dmplist = []
    cols = ['user','timestampUsec','time authorbadge','text purchaseAmount','type','video_id','Chat_No']
    dfn = pd.DataFrame(index=[], columns=cols)

    for line in tqdm(comment_data):
        df = pd.DataFrame(line,index=['1',])
        dfn=pd.concat([df,dfn],axis=0)

    csv=dfn.to_csv(index=False)
    output_file_name = video_id + '.csv'
    print('DONE!')

    #firebase storageにアップロードする
    file_name=output_file_name

    cred = credentials.Certificate(key)
    if not firebase_admin._apps:
        # 初期済みでない場合は初期化処理を行う
        initialize_app(cred, {'storageBucket': bucket_name})

    bucket = storage.bucket()
    blob = bucket.blob(file_name)
    blob.upload_from_string(csv)

    print('DONE!')

    

