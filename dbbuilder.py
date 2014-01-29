import sys
from numpy import matrix
import powerRatings as prs
import api

#live-updating percent value
def progressBar(message,iterator,maximum):
    sys.stdout.write("\r"+message+": %d%%" %(iterator*100/maximum))
    sys.stdout.flush()

#live-updating message
def update(base_message,rolling_message):
    sys.stdout.write("\r"+base_message+rolling_message)
    sys.stdout.flush()

#removes 'B's which are sometimes suffixed to team names during matches
#but not for the full event roster. not fixing this causes issues
def removeBs(l):
    final = [x if (x[-1]=='0' or
                   x[-1]=='1' or
                   x[-1]=='2' or
                   x[-1]=='3' or
                   x[-1]=='4' or
                   x[-1]=='5' or
                   x[-1]=='6' or
                   x[-1]=='7' or
                   x[-1]=='8' or
                   x[-1]=='9' )
                   else x[:-1] for x in l]
    return final

#to copy 1-D lists etc use new = old[:]
#but to copy 2-D lists...
def doubleCopy(l):
    final = []
    for element in l:
        final.append([])
    i = 0
    while i<len(final):
        final[i] = l[i][:]
        i+=1
    return final

#removes redundancies and orders list
#better used at start on input, but sometimes cannot be
def clean(l):
    final = set(l)
    final = list(final)
    final.sort()
    return final



#takes a list of years. must be list. can be only 1 long.
def collect_event_keys(year_list):
    year_list = clean(year_list)
    final = []
    for year in year_list:
        progressBar("Collecting Event Keys",year_list.index(year)+1,len(year_list))
        a = api.event_list(year)
        for b in a:
            final.append(b['key'])
    print "\nEvent Key List Complete!"
    return final
    
#takes list of event keys. can be only 1 long.
def collect_events(event_key_list):
    event_key_list = clean(event_key_list)
    final = []
    for event_key in event_key_list:
        update("Collecting Event Infos",
               "... collecting for event %d/%d"
               %(event_key_list.index(event_key)+1,len(event_key_list)))
        a = api.event_info(event_key)
        final.append(a)
    print "\nEvent Infos Collected!"
    return final

#takes list of full dictionaries returned by an api.event_info(key) call
def collect_teams(event_list):
    final = []
    for event in event_list:
        progressBar("Populating Teams List",event_list.index(event)+1,len(event_list))
        for t in event['teams']:
            final.append(t)    
    final = clean(final)
    print "\nTeams List Complete!"
    return final
    
#takes list of full dictionaries returned by an api.event_info(key) call
def collect_match_keys(event_list):
    final = []
    for event in event_list:
        progressBar("Populating Match Key List",event_list.index(event)+1,len(event_list))
        for m in event['matches']:
            final.append(m)    
    final = clean(final)
    print "\nMatch Key List Complete!"
    return final

def collect_matches(match_key_list):
    match_key_list = clean(match_key_list)
    final = []
    for match_key in match_key_list:
        update("Collecting Match Infos",
               "... collecting for match %d/%d"
               %(match_key_list.index(match_key)+1,len(match_key_list)))
        a = api.match_info(match_key)[0]
        final.append(a)
    print "\nMatch Infos Collected!"
    return final

#creates appropriate M, Mprime, S, and Sprime empty structures to be filled
def create_mould(team_list):
    mtrix = []
    scorecard = []
    for t in team_list:
        mtrix.append([])
        scorecard.append(0)
    i = 0
    while i<len(team_list):
        for t in team_list:
            mtrix[i].append(0)
        i+=1
    M = doubleCopy(mtrix)
    Mprime = doubleCopy(mtrix)
    S = scorecard[:]
    Sprime = scorecard[:]
    final = {'M':M,'Mprime':Mprime,'S':S,'Sprime':Sprime,'teams':team_list}
    return final

def fill_mould(mould,match):
    team_list = mould['teams']
    blue = match['alliances']['blue']
    red = match['alliances']['red']
    #remove modifications to match-specific team designations
    blue['teams'] = removeBs(blue['teams'])
    red['teams'] = removeBs(red['teams'])
    #for each member of the blue team
    for team in blue['teams']:
        #fill M
        temp = blue['teams'][:]
        temp.remove(team)
        for u in temp:
            mould['M'][team_list.index(team)][team_list.index(u)]+=1
        #fill Mprime
        temp = red['teams'][:]
        for u in temp:
            mould['Mprime'][team_list.index(team)][team_list.index(u)]+=1
        #fill S
        mould['S'][team_list.index(team)]+=blue['score']
        #fill Sprime
        mould['Sprime'][team_list.index(team)]+=red['score']
    #for each member of the red team
    for team in red['teams']:
        #fill M
        temp = red['teams'][:]
        temp.remove(team)
        for u in temp:
            mould['M'][team_list.index(team)][team_list.index(u)]+=1
        #fill Mprime
        temp = blue['teams'][:]
        for u in temp:
            mould['Mprime'][team_list.index(team)][team_list.index(u)]+=1
        #fill S
        mould['S'][team_list.index(team)]+=red['score']
        #fill Sprime
        mould['Sprime'][team_list.index(team)]+blue['score']
    return mould

def pour_mould(mould,match_list):
    for match in match_list:
        update("Pouring the mould",
               "... pouring for match %d/%d"
               %(match_list.index(match)+1,len(match_list)))
        mould = fill_mould(mould, match)
    print ''
    return mould

def run_mould(mould):
    M = matrix(mould['M'])
    Mprime = matrix(mould['Mprime'])
    S = matrix(mould['S']).getT()
    Sprime = matrix(mould['Sprime']).getT()
    final = prs.getAllRatings(M,Mprime,S,Sprime)
    final['teams'] = mould['teams'][:]
    return final

def uncase(sculpture):
    i=0
    while i<len(sculpture['teams']):
        sculpture['diffpr'][i] = sculpture['diffpr'][i].tolist()[0][0]
        sculpture['opr'][i] = sculpture['opr'][i].tolist()[0][0]
        sculpture['dpr'][i] = sculpture['dpr'][i].tolist()[0][0]
        i+=1
    return sculpture
        

#def calc_stats_event(event_id):
#    x = []
#    x.append(event_id)
#    x = collect_events(x)
#    x = collect_match_keys(x)
#    x = collect_matches(x)
    

####==================== TESTS =====================####
#x = []
#x.append(2012)
#print collect_events(collect_event_keys(x))
#WORKS!

#x = []
#x.append('2012ct')
#print create_mold(collect_teams(collect_events(x)))
#WORKS!

#x = []
#x.append('2012ct')
#print collect_matches(collect_match_keys(collect_events(x)))
#WORKS!

def calc_stats_events(event_key_list):
    x = event_key_list
    mould = create_mould(collect_teams(collect_events(x)))
    matches = collect_matches(collect_match_keys(collect_events(x)))
    mould = pour_mould(mould,matches)
    return uncase(run_mould(mould))

def calc_stats_year(year_list):
    x = collect_event_keys(year_list)
    return calc_stats_events(x)




#print calc_stats_year([2013])
#a = calc_stats_events(['2012ww'])
#b = calc_stats_events(['2012ww','2012ww','2012ww'])
#print a
#print b


#EVERYTHING WORKS! YISS!!!! SUCCESS!!!!
