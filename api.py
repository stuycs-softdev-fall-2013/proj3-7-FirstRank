"""API Documentation @ https://github.com/gregmarra/the-blue-alliance/wiki/API-v1-Documentation"""

import requests #request library @ http://docs.python-requests.org/en/latest/

api_url = 'http://www.thebluealliance.com/api/v1/'

def event_list(year):
    return _api_call('events/list',year=year)

def event_info(key):
    return _api_call('event/details',event=key)

def match_info(key):
    return _api_call('match/details',match=key)

def team_info(key):
    return _api_call('teams/details',team=key)

def _api_call(address, **params):
    "Private Function"
    return requests.get(api_url+address, params=params).json()
