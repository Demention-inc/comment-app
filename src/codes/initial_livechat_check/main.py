import platform
import json
import sys
import os
from retry import retry
from bs4 import BeautifulSoup
import requests



class ContinuationURLNotFound(Exception):
    pass

class LiveChatReplayDisabled(Exception):
    pass

class RestrictedFromYoutube(Exception):
    pass



def get_ytInitialData(target_url, session):
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    html = session.get(target_url, headers=headers)
    soup = BeautifulSoup(html.text, 'html.parser')
    for script in soup.find_all('script'):
        script_text = str(script)
        if 'ytInitialData' in script_text:
            for line in script_text.splitlines():
                if 'ytInitialData' in line:
                    if 'var ytInitialData =' in line:
                        st = line.strip().find('var ytInitialData =') + 19
                        return(json.loads(line.strip()[st:-10]))
                    if 'window["ytInitialData"] =' in line:
                        return(json.loads(line.strip()[len('window["ytInitialData"] = '):-1]))
#                    return(json.loads(line.strip()[len('window["ytInitialData"] = '):-1]))

    if 'Sorry for the interruption. We have been receiving a large volume of requests from your network.' in str(soup):
        print("restricted from Youtube (Rate limit)")
        raise RestrictedFromYoutube

    return(None)

def check_livechat_replay_disable(ytInitialData):
    conversationBar = ytInitialData['contents'].get('twoColumnWatchNextResults',{}).get('conversationBar', {})
    if conversationBar:
        conversationBarRenderer = conversationBar.get('conversationBarRenderer', {})
        if conversationBarRenderer:
            text = conversationBarRenderer.get('availabilityMessage',{}).get('messageRenderer',{}).get('text',{}).get('runs',[{}])[0].get('text')
            print(text)
            if text == 'この動画ではチャットのリプレイを利用できません。':
                return(True)
    else:
        return(True)

    return(False)

@retry(ContinuationURLNotFound, tries=2, delay=1)
def get_initial_continuation(target_url):
    print(target_url)
    session = requests.session()
    try:
        ytInitialData = get_ytInitialData(target_url, session)
    except RestrictedFromYoutube:
        return(None)


    if not ytInitialData:
        print("Cannot get ytInitialData")
        raise ContinuationURLNotFound

    if check_livechat_replay_disable(ytInitialData):
        print("LiveChat Replay is disable")
        raise LiveChatReplayDisabled

    continue_dict = {}
    try:
        continuations = ytInitialData['contents']['twoColumnWatchNextResults']['conversationBar']['liveChatRenderer']['header']['liveChatHeaderRenderer']['viewSelector']['sortFilterSubMenuRenderer']['subMenuItems']
        for continuation in continuations:
            continue_dict[continuation['title']] = continuation['continuation']['reloadContinuationData']['continuation']
    except KeyError:
        print("Cannot find continuation")

    continue_url = None
    if not continue_url:
        if continue_dict.get('上位のチャットのリプレイ'):
            continue_url = continue_dict.get('上位のチャットのリプレイ')
        if continue_dict.get('Top chat replay'):
            continue_url = continue_dict.get('Top chat replay')

    if not continue_url:
        if continue_dict.get('チャットのリプレイ'):
            continue_url = continue_dict.get('チャットのリプレイ')
        if continue_dict.get('Live chat replay'):
            continue_url = continue_dict.get('Live chat replay')

    if not continue_url:
        continue_url = ytInitialData["contents"]["twoColumnWatchNextResults"].get("conversationBar", {}).get("liveChatRenderer",{}).get("continuations",[{}])[0].get("reloadContinuationData", {}).get("continuation")

    if not continue_url:
        raise ContinuationURLNotFound

    return(continue_url)




