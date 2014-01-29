from random import randint
from time import mktime, localtime
from urllib import quote

from hashlib import sha1
import hmac
import binascii

lowers = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
uppers = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def consumer_key():
    return '4GbaQbqcqJ1kFEHt5z5Uxg'

def nonce():
    final = ''
    i = randint(32,42)
    while True:
        j = randint(0,2)
        if j==0:
            final=final+str(randint(0,9))
        if j==1:
            final=final+lowers[randint(0,25)]
        else:
            final=final+uppers[randint(0,25)]
        i=i-1
        if i==0:
            return final

def signature_method():
    return 'HMAC-SHA1'

def timestamp():
    return int(mktime(localtime()))

def token():
    return '2312426281-UWf6zpbHXEwUWVKvBcZJDPmh8xEMWCSTLki5EL6'

def version():
    return '1.0'

def parameter_string(count):
    oauth_consumer_key = ['oauth_consumer_key',quote(consumer_key(),'')]
    oauth_nonce = ['oauth_nonce',quote(nonce(),'')]
    oauth_signature_method = ['oauth_signature_method',quote(signature_method(),'')]
    oauth_timestamp = ['oauth_timestamp',quote(str(timestamp()),'')]
    oauth_token = ['oauth_token',quote(token(),'')]
    oauth_version = ['oauth_version',quote(version(),'')]
    screen_name = ['screen_name',quote('frcfms','')]
    count = ['count',quote(str(count),'')]

    a = [oauth_consumer_key,oauth_nonce,oauth_signature_method,oauth_timestamp,
         oauth_token,oauth_version,screen_name,count]
    a.sort()
    final = ''
    for b in a:
        final = final + b[0] + '=' + b[1] + '&'
    final = final[:len(final)-1]
    return final

def signature_base_string(count):
    final = 'GET&'
    final = final + quote('https://api.twitter.com/1.1/statuses/user_timeline.json','') + '&'
    final = final + quote(parameter_string(count))
    return final

def signing_key(consumer_secret,oauth_token_secret):
    return ''+quote(consumer_secret,'')+'&'+quote(oauth_token_secret,'')

def signature(count,consumer_secret,oauth_token_secret):
    key = signing_key(consumer_secret,oauth_token_secret)
    base = signature_base_string(count)
    hashed = hmac.new(key,base,sha1)
    return binascii.b2a_base64(hashed.digest())[:-1]

def header(count,consumer_secret,oauth_token_secret):
    oauth_consumer_key = ['oauth_consumer_key',quote(consumer_key(),'')]
    oauth_nonce = ['oauth_nonce',quote(nonce(),'')]
    oauth_signature=['oauth_signature',quote(signature(count,
                                                       consumer_secret,
                                                       oauth_token_secret),'')]

    oauth_signature_method = ['oauth_signature_method',quote(signature_method(),'')]
    oauth_timestamp = ['oauth_timestamp',quote(str(timestamp()),'')]
    oauth_token = ['oauth_token',quote(token(),'')]
    oauth_version = ['oauth_version',quote(version(),'')]

    a = [oauth_consumer_key,oauth_nonce,oauth_signature,
         oauth_signature_method,oauth_timestamp,
         oauth_token,oauth_version]
    a.sort()
    final = 'OAuth '
    for b in a:
        final = final + b[0] + '=' + '"' + b[1] +'"' + ', '
    final = final[:len(final)-2]
    return final

