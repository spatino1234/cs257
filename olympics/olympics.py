'''
    olympics.py
    Serafin Patino Jr


    Using psycopg2 to connect and query psql olympics database
'''
import sys
import psycopg2
import config

def get_connection():
    ''' Returns a database connection object with which you can create cursors,
        issue SQL queries, etc. This function is extremely aggressive about
        failed connections--it just prints an error message and kills the whole
        program. Sometimes that's the right choice, but it depends on your
        error-handling needs. '''
    try:
        return psycopg2.connect(database=config.database,
                                user=config.user,
                                password=config.password)
    except Exception as e:
        print(e, file=sys.stderr)
        exit()

def get_noc_gold_medals():
    ''' Returns a list of all the NOCs, their gold medals in desc order via medals'''
    noc_medal_number = []
    try:
        # Create a "cursor", which is an object with which you can iterate
        # over query results.
        connection = get_connection()
        cursor = connection.cursor()

        # Execute the query
        query = '''SELECT nocs.abbreviation, COUNT(medals.version)
                    FROM nocs, medals, linkingtable
                    WHERE medals.id = linkingtable.medal_id
                    AND medals.version = 'Gold'
                    AND nocs.id = linkingtable.noc_id
                    GROUP BY nocs.abbreviation
                    ORDER BY COUNT(medals.version) DESC;'''
        cursor.execute(query)

        # Iterate over the query results to produce the list of author names.
        for row in cursor:
            noc = row[0]
            numsGold = row[1]
            noc_medal_number.append(f'{noc} {numsGold}')

    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return noc_medal_number

def get_athletes_from_noc(search_text):
    ''' Returns a list of the full names of the athletes from a specific NOC'''
    athletes = []
    try:
        query = '''SELECT DISTINCT athletes.name
                FROM athletes, nocs, linkingtable
                WHERE athletes.id = linkingtable.athlete_id
                AND nocs.id = linkingtable.noc_id
                AND nocs.abbreviation = %s'''
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (search_text,))
        for row in cursor:
            athletes_name = row[0]
            athletes.append(f'{athletes_name}')

    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return athletes

def get_events():
    ''' Returns a list of all events'''
    all_events = []
    try:
        # Create a "cursor", which is an object with which you can iterate
        # over query results.
        connection = get_connection()
        cursor = connection.cursor()

        # Execute the query
        query = '''SELECT events.event
                FROM events, linkingtable
                WHERE events.id = linkingtable.event_id;'''
        cursor.execute(query)

        # Iterate over the query results to produce the list of author names.
        for row in cursor:
            event = row[0]
            all_events.append(f'{event}')

    except Exception as e:
        print(e, file=sys.stderr)

    connection.close()
    return all_events

def show_usage():
    usage = open('usage.txt')
    print(usage.read())
    usage.close()

def main():
    # deals with the using asking for help
    usercommand = sys.argv[1]
    if usercommand == '--help' or usercommand == '--h':
        show_usage()

    # deals with the user typing in the gold command
    elif usercommand == 'gold':
        if len(sys.argv) == 2:
            print('========== all nocs, their gold medals won, descing order via medal ==========')
            nocs_gold = get_noc_gold_medals
            for noc in nocs_gold:
                print (noc)
        else:
            print('your command is invalid, try again')

    # deals with the user typing in the events command
    elif usercommand == 'events':
        if len(sys.argv) == 2:
            print('========== all events in the olympics ==========')
            event_olympics = get_events
            for everyevent in event_olympics:
                print(everyevent)
        else:
            print('your command is invalid, try again')
    
    # deals with the user typing in the athletes command
    elif usercommand == 'athletes':
        if len(sys.argv) == 3:
            search_text = sys.argv[2]
            print('========== all athletes from NOC: "{search_text}" ==========')
            athletes_noc = get_athletes_from_noc(search_text)
            for athlete in athletes_noc:
                print(athlete)
        else:
            print('your command is invalid, try again')
            
    # deals with the user typing in a invalid command
    else:
        print('your command is invalid, try again')

if __name__ == '__main__':
    main()