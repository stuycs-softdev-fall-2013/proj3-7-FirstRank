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
    return _api_call('team/details',team=key)

def teams_show(key):
    return _api_call('teams/show',teams=key)

def _api_call(address, **params):
    "Private Function"
    headers = {'X-TBA-App-Id':'frc694:FRCstats:1.0'}
    return requests.get(api_url+address,
                        params=params,
                        headers=headers).json()

#print teams_show('frc694,frc1')
#print event_list(2013)
#print event_info('2013nyny')
#print team_info('frc694')
#print match_info('2013nyny_qm20')
