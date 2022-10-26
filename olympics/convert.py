'''
    CS 257 Software Design
    Prof. Jeff Ondich
    Author: Serafin Patino Jr

    This program gets data from an olympic dataset from
    kaggkle 
    https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results
'''

import csv

#plan: make dictionaries that correspond to each table, make a linking table that connects their id
# ake the csv for each table that has all the fields from the respective table

athleteDictionary = {}
eventDictionary = {}
sportDictionary = {}
olympicgamesDictionary = {}
medalDictionary = {}
nocDictionary = {}
# linkingTable = {}

with open('athlete_events.csv') as original_data_file,\
    open ('athletes.csv', 'w') as athletes_file, open('linkingTable.csv', 'w') as linkingTable_file ,\
    open ('noc.csv', 'w') as noc_file,open('medals.csv','w') as medals_file, open('events.csv', 'w') as events_file,\
    open ('olympic_games.csv', 'w') as olympic_games_file, open ('sports.csv', 'w') as sports_file:
    reader = csv.reader(original_data_file, delimiter=',')
    athletes_writer = csv.writer(athletes_file)
    events_writer = csv.writer(events_file)
    sports_writer = csv.writer(sports_file)
    olympic_games_writer = csv.writer(olympic_games_file)
    medals_writer = csv.writer(medals_file)
    noc_writer = csv.writer(noc_file)
    linkingTable_writer = csv.writer(linkingTable_file)
    next(reader) #skips header is original file

# organizing variables to make tables / csv files later on

    for row in reader:
        athlete_id = row[0]
        athlete_name = row[1]
        athlete_sex = row[2]

        if row[3] == 'NA':
            athlete_age = 0
        else:
            athlete_age = int(row[3])
        if row[4] == 'NA':
            athlete_height = 0
        else:
            athlete_height = float(row[4])
        if row[5] == 'NA':
            athlete_weight = 0
        else:
            athlete_weight = float(row[5])
        noc_name = row[7]
        olympic_game =  row[8]
        olympic_game_year = row[9]
        olympic_game_season = row[10]
        olympic_game_city = row[11]
        sport_name = row[12]
        event_name = row[13]
        medal_received = row[14]

        # create sports.csv and dictionary
        if sport_name not in sportDictionary:
            sport_id = len(sportDictionary) + 1
            sportDictionary[sport_name] = sport_id
            sports_writer.writerow([sport_id, sport_name])

        # create events.csv and disctionary
        if event_name not in eventDictionary:
            event_id = len(eventDictionary) + 1
            eventDictionary[event_name] = event_id
            events_writer.writerow([event_id, event_name])

        # create athletes.csv and disctionary
        if athlete_id not in athleteDictionary:
            athleteDictionary[athlete_id] = athlete_name
            athletes_writer.writerow([athlete_id, athlete_name])
        
        # create noc.csv and dictionary
        if noc_name not in nocDictionary:
            noc_id = len(nocDictionary) + 1 
            nocDictionary[noc_name] = noc_id
            noc_writer.writerow([noc_id,noc_name])

        # create medals.csv and dictioanary
        if medal_received not in medalDictionary:
            medal_id = len(medalDictionary) + 1
            medalDictionary[medal_received] = medal_id
            medals_writer.writerow([medal_id, medal_received])

        # create olympic_games.csv and dictionary
        if olympic_game not in olympicgamesDictionary:
            olympic_game_id = len(olympicgamesDictionary) + 1
            olympicgamesDictionary[olympic_game] = olympic_game_id
            olympic_games_writer.writerow([olympic_game_id, olympic_game_year, olympic_game_season, olympic_game_city])

        noc_id = nocDictionary[noc_name]
        olympic_game_id = olympicgamesDictionary[olympic_game]
        sport_id = sportDictionary[sport_name]
        event_id = eventDictionary[event_name]
        medal_id = medalDictionary[medal_received]
        

        # create the linkingTable.csv and dictionary
        linkingTable_writer.writerow([athlete_id,noc_id, olympic_game_id, sport_id, event_id, medal_id, athlete_height, athlete_weight, athlete_age, athlete_sex])


# 
