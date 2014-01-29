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

def removeBs(l):
    final = [x if x[-1]!='B' else x[:-1] for x in l]
    return final

#to copy lists, strings, etc use new = old[:]

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
def collect_match_ids(event_list):
    final = []
    for event in event_list:
        progressBar("Populating Match IDs List",event_list.index(event)+1,len(event_list))
        for m in event['matches']:
            final.append(m)    
    final = clean(final)
    print "\nMatche ID List Complete!"
    return final



####==================== TESTS =====================####
#x = []
#x.append(2012)
#print collect_events(collect_event_keys(x))
#WORKS!

#x = []
#x.append('2012ct')
#print collect_teams(collect_events(x))
#WORKS!

