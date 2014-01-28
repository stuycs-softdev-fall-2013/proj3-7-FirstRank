# will contain functions that pull info from api
# and will convert the info to a form specifically
# suited for the front end and database purposes
import sys
from numpy import matrix
import powerRatings as prs
#import pymongo
#client = MongoClient('localhost':8000)

#db = client.first
#stats = db.stats #stats table, stores and gets updated from AP

import api

def copy(lst):
    copy = []
    for i in lst:
        copy.append(i)
    return copy

def collect_event_keys(year):
    a = api.event_list(year)
    final = []
    for b in a:
        final.append(b['key'])
    print "collected all event keys"
    return final

def collect_match_keys(key):
    a = api.event_info(key)
    return a['matches']

def build_event(key):
    base = api.event_info(key)
    
#    print 'checkpoint 0'

    teams = base['teams']
#    print len(teams)
    matches = collect_match_keys(key)
#    print len(matches)
#    print 'checkpoint 1'
    
    i = 0
    while True:
        matches[i]=api.match_info(matches[i])
        sys.stdout.write("\rpulling match # %d/%d" %((i+1),len(matches)))
        sys.stdout.flush()
        i+=1
        if i==len(matches):
            break
    print ''
#    print 'checkpoint 2'

    M=[]
    Mprime=[]
    S = []
    Sprime = []
    for t in teams:
        M.append([])
        Mprime.append([])
        S.append(0)
        Sprime.append(0)
    i = 0
    while i<len(teams):
        for t in teams:
            M[i].append(0)
            Mprime[i].append(0)
        i+=1                 
#    print 'checkpoint 3'
    i=1
    for match in matches:
        sys.stdout.write("\rmatch: %s" %(match[0]['key']))
        sys.stdout.flush()
        blue = match[0]['alliances']['blue']
        red = match[0]['alliances']['red']
        for t in blue['teams']:
            #temp must be created separately from new literal
            temp = copy(blue['teams'])
            temp.remove(t)
            for u in temp:
                M[teams.index(t)][teams.index(u)]+=1

            temp = copy(red['teams'])
            for u in temp:
                Mprime[teams.index(t)][teams.index(u)]+=1
            S[teams.index(t)]+=blue['score']
            Sprime[teams.index(t)]+=red['score']
        for t in red['teams']:
            temp = copy(red['teams'])
            temp.remove(t)
            for u in temp:
                M[teams.index(t)][teams.index(u)]+=1
            temp = copy(blue['teams'])
            for u in temp:
                Mprime[teams.index(t)][teams.index(u)]+=1
            S[teams.index(t)]+=red['score']
            Sprime[teams.index(t)]+=blue['score']
    print ''

    M = matrix(M)
    Mprime = matrix(Mprime)
    S = matrix(S).getT()
    Sprime = matrix(Sprime).getT()
    return {'teams':teams,'M':M,'Mprime':Mprime,'S':S,'Sprime':S}


def event_prs(key):
    b = build_event(key)
    final = prs.getAllRatings(b['M'],b['Mprime'],b['S'],b['Sprime'])
    final['teams']=b['teams']
    return final


def build_year(year):
    event_keys = collect_event_keys(year)
    matches = []
    temp1 = []
    temp2 = []
    teams = []
    i=0
    for k in event_keys:
        sys.stdout.write("\rpulling match keys and teams for event # %d/%d" %((i+1),len(event_keys)))
        sys.stdout.flush()
        i+=1
        event = api.event_info(k)
        temp1.append(event['matches'])
        temp2.append(event['teams'])
    for a in temp1:
        for b in a:
            matches.append(b)
    for a in temp2:
        for b in a:
            teams.append(b)
    print ''
#now we have all the match keys for the entire year
    i = 0
    while True:
        matches[i]=api.match_info(matches[i])
        sys.stdout.write("\rpulling match info for match # %d/%d" %((i+1),len(matches)))
        sys.stdout.flush()
        i+=1
        if i==len(matches):
            break
    print ''
#now we have all the match infos and teams for the entire year
    
    M=[]
    Mprime=[]
    S = []
    Sprime = []
    for t in teams:
        M.append([])
        Mprime.append([])
        S.append(0)
        Sprime.append(0)
    i = 0
    while i<len(teams):
        for t in teams:
            M[i].append(0)
            Mprime[i].append(0)
        i+=1                 

#now we've created slots for M,Mprime,S,Sprime

    for match in matches:
        sys.stdout.write("\rmatch: %s" %(match[0]['key']))
        sys.stdout.flush()
        blue = match[0]['alliances']['blue']
        red = match[0]['alliances']['red']
        i=0
        while i<len(blue['teams']):
            t = blue['teams'][i]
            if t[len(t)-1]=='B':
                t=t[:len(t)-1]
            i+=1
        i=0
        while i<len(red['teams']):
            t = red['teams'][i]
            if t[len(t)-1]=='B':
                t=t[:len(t)-1]
            i+=1
        for t in blue['teams']:
            #temp must be created separately from new literal
            temp = copy(blue['teams'])
            temp.remove(t)
            for u in temp:
                M[teams.index(t)][teams.index(u)]+=1

            temp = copy(red['teams'])
            for u in temp:
                Mprime[teams.index(t)][teams.index(u)]+=1
            S[teams.index(t)]+=blue['score']
            Sprime[teams.index(t)]+=red['score']
        for t in red['teams']:
            temp = copy(red['teams'])
            temp.remove(t)
            for u in temp:
                M[teams.index(t)][teams.index(u)]+=1
            temp = copy(blue['teams'])
            for u in temp:
                Mprime[teams.index(t)][teams.index(u)]+=1
            S[teams.index(t)]+=red['score']
            Sprime[teams.index(t)]+=blue['score']
    print ''

#now we've successfully created all values for M, Mprime, S, Sprime
    
    M = matrix(M)
    Mprime = matrix(Mprime)
    S = matrix(S).getT()
    Sprime = matrix(Sprime).getT()
    return {'teams':teams,'M':M,'Mprime':Mprime,'S':S,'Sprime':S}


def year_prs(year):
    b = build_year(year)
    final = prs.getAllRatings(b['M'],b['Mprime'],b['S'],b['Sprime'])
    final['teams']=b['teams']
    return final




x = year_prs(2012)
print x


