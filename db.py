# will contain functions that pull info from api
# and will convert the info to a form specifically
# suited for the front end and database purposes



import pymongo
client = MongoClient('localhost':8000)

db = client.first
stats = db.stats #stats table, stores and gets updated from AP

#documents in the stat table will be dictionaries structured as follows,
#the first entry in the dictionary will be 'eventID':####
#(4 digit ids used for events, 0000 indicates full season stats)
#the rest of the entries will be a set [OPR,DPR,DiffPR] mapped to a team's
#FIRST number. So, for example, if you wanted to get Stuy's
#stats for the entire season in the stats collection, you would go:
#>>>fullSeason = stats.find_one({'eventID':'0000'})
#>>>return fullSeason['0694']

#will not be storing team info and event info as the API can quickly and easily
#provide that

