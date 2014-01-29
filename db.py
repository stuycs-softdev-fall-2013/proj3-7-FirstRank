import sys
from numpy import matrix
import powerRatings as prs
import api
import pymongo as pm
import dbbuilder

def set_stats_events(event_key_list):
    stats = calc_stats_events(event_key_list)
    c = pymongo.MongoClient()
    db = c.frc_data
    tree = {'seed' : event_key_list,
             'tree' : stats}
    forest = db.events
    tree_id = forest.insert(tree)

def get_stats_events(event_key_list):
    c = pymongo.MongoClient()
    db = c.frc_data
    forest = db.events
    return forest.find_one({'seed' : event_key_list})

def set_stats_year(year_list):
    stats = calc_stats_year(year_list)
    c = pymongo.MongoClient()
    db = c.frc_data
    tree = {'seed' : year_list,
             'tree' : stats}
    forest = db.years
    tree_id = forest.insert(tree)

def get_stats_years(year_list):
    c = pymongo.MongoClient()
    db = c.frc_data
    forest = db.years
    return forest.find_one({'seed' : year_list})

def check_name(team_id_list):
    entry = ''
    for team in team_id_list:
        entry+=team
        entry+=','
    #remove last extra comma
    entry = entry[:-1]
    info = api.teams_show(entry)
    final = []
    for team in info:
        final.append(team['nickname'])
    return final

def rearrange(tree):
    team_names = check_name(tree['teams'])
    final = []
    i = 0
    while i<len(team_names):
        temp = {}
        temp['opr'] = tree['opr'][i]
        temp['dpr'] = tree['dpr'][i]
        temp['diffpr'] = tree['diffpr'][i]
        temp['team_id'] = tree['teams'][i]
        temp['teamname'] = team_names[i]
        final.append(temp)
    return final

def rearrange_team(tree,team_id):
    team_names = check_name([team_id])
    final = []
    i = 0
    while i<len(team_names):
        temp = {}
        temp['opr'] = tree['opr'][i]
        temp['dpr'] = tree['dpr'][i]
        temp['diffpr'] = tree['diffpr'][i]
        temp['team_id'] = tree['teams'][i]
        temp['teamname'] = team_names[i]
        final.append(temp)
    return final


#returns stats for most recent event
def get_current_stats(year):
    c = pymongo.MongoClient()
    db = c.frc_data
    forest = db.events
    events = api.event_list(year)
    #returns list sorted alphabetically by event key
    dates = []
    keys = []
    for event in events:
        for key in event.keys():
            if key=='start_date':
                dates.append(event[key])
            if key=='key':
                keys.append(event[key])
    #dates is unordered
    dates_ordered = dates[:]
    dates_ordered.sort()
    k = 1
    while k<=len(dates_ordered):
        i = dates.index(dates_ordered[len(dates_ordered)-k])
        key = keys[i]
        if forest.find_one({'seed':[key]})!=None:
            return rearrange(forest.find_one({'seed':[key]}))
        k+=1

def get_event_stats(event_id):
    return rearrange(get_stats_events([event_id]))

def get_teamlist(year,page):
    final = rearrange(get_stats_years([year]))
    return final[(page-1)*100:page*100-1]

def get_team_overall_stats_year(team_id,year):
    c = pymongo.MongoClient()
    db = c.frc_data
    forest = db.events
    events = api.event_list(year)
    for event in events:
        if event['teams'].count(team_id)==0:
            events.remove(event)
    event_keys = []
    for event in events:
        event_keys.append(event['key'])
    final = []
    for key in event_keys:
        final.append(rearrange_team(get_stats_events([key]),team_id))
    return final

def get_team_overall_stats(team_id):
    return get_team_overall_stats_year(team_id,2013)
