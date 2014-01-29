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

def get_stats_events(year_list):
    c = pymongo.MongoClient()
    db = c.frc_data
    forest = db.years
    return forest.find_one({'seed' : year_list})
