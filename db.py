import api
from pymongo import MongoClient

db = MongoClient().database

def addTeams():
    i = 1
    while i < 5382:
        key = "frc" + str(i)
        team = api.team_info(key)
        if 'key' in team and team['name'] != None:
            db.teams.insert({key:team})
        i = i + 1

def team_compiler(page_num):
    cursor = db.teams.find(fields={'_id':False})
    teams = [x for x in cursor]
    return teams[(page_num - 1) * 100: page_num * 100]

if __name__ == "__main__":
    #addTeams()
    teams = team_compiler(1)
    for team in teams:
        for x in team:
            print team[x]
