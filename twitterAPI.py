import requests #request library @ http://docs.python-requests.org/en/latest/
#import oauth <--- Wrote this all by myself... for no reason whatsoever
#because there's already code for it... Damn it...

from requests_oauthlib import OAuth1

api_url = 'https://api.twitter.com/1.1/'
screen_name = 'frcfms'
global last_update
last_update = ''

def get_n_most_recent_tweets(n):
    a = _api_call('statuses/user_timeline.json',screen_name=screen_name,count=n)
    texts = []
    for b in a:
        texts.append(b['text'])
    return texts    

def get_new_tweets():
    if last_update=='':
        return get_n_most_recent_tweets(20)
    count = 1
    while True:
        a = _api_call('statuses/user_timeline.json',screen_name=screen_name,count=count)
        if a[len(a)-1]['id_str']==last_update:
            a.pop()
            break
        count=count+1
    if a==[]:
        return 'No new updates'
    global last_update
    last_update = a[0]['id_str']
    texts = []
    for b in a:
        texts.append(b['text'])
    return texts    

def _api_call(address, **params):
    auth = OAuth1('4GbaQbqcqJ1kFEHt5z5Uxg','yaew7yf9fi20vRtEJy0csArMvrsjaNNeSew5DbHUI','2312426281-UWf6zpbHXEwUWVKvBcZJDPmh8xEMWCSTLki5EL6','RiDm7oN5Cybf9QHZxcwkiJnBrG0tWDkYcGvBkCn9ovfLA')
    return requests.get(api_url+address, params=params, auth=auth).json()


