'''
    api.py
    Jeff Ondich, 25 April 2016
    Updated 8 November 2021
    
    Modified by Ruben Boero and Serafin Patino
'''
import sys
import flask
import json
import config
import psycopg2

api = flask.Blueprint('api', __name__)

def get_connection():
    ''' Returns a connection to the database described in the
        config module. May raise an exception as described in the
        documentation for psycopg2.connect. '''
    return psycopg2.connect(database=config.database,
                            user=config.user,
                            password=config.password)

# -------Generations Page-------
@api.route('/generations') 
def get_generations():
    ''' Returns a list of all the pokemon in a given generation. 
        By default the list is in ascending order by idx number.  
            http://.../generations
        Returns an empty list if there's any database failure.
    '''
    query = '''SELECT name FROM generations
               ORDER BY id ASC;'''
    generations_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, tuple())
        for row in cursor:
            generation = row[0]
            generations_list.append(generation)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(generations_list)

@api.route('/generation/<gen_name>')
def get_pokemon_for_generation(gen_name):
    query = '''SELECT  pokemon.dex_num, pokemon.name, ab1.name, ab2.name, ab3.name, typ1.name, typ2.name, generations.name, pokemon.id
            FROM pokemon, abilities ab1, abilities ab2, abilities ab3, types typ1, types typ2, generations, linking_table
            WHERE 1 = 1
            AND pokemon.id = linking_table.pokemon_id
            AND ab1.id = linking_table.ability1_id
            AND ab2.id = linking_table.ability2_id
            AND ab3.id = linking_table.ability3_id
            AND typ1.id = linking_table.type1_id
            AND typ2.id = linking_table.type2_id
            AND generations.id = linking_table.generation_id
            AND generations.name = %s
            ORDER BY pokemon.dex_num ASC;
            '''
    pokemon_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (gen_name,))
        for row in cursor:
            row = list(row)
            # give a value of NA to any entry that has no value
            for i in range(len(row)):
                if row[i] == '':
                    row[i] = 'NA'

            pokemon_list.append({'dex_num':row[0], 'name':row[1], 'ability1':row[2], 'ability2':row[3],\
                'ability3':row[4], 'type1':row[5], 'type2':row[6], 'generation':row[7], 'id':row[8]})
        
        cursor.close()
        connection.close()

    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(pokemon_list)

# -------Legendaries Page-------
@api.route('/legendaries') 
def get_legendaries():
    ''' Returns a list of all the pokemon in a given legendary category. 
        By default the list is in ascending order by idx number.  
            http://.../legendaries
        Returns an empty list if there's any database failure.
    '''
    query = '''SELECT name FROM legendaries;'''
    legendaries_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(query, tuple())
        for row in cursor:
            legendary = row[0]
            legendaries_list.append(legendary)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(legendaries_list)

@api.route('/legendaries/<legendary_category>')
def get_pokemon_for_legendary_category(legendary_category):
    query = '''SELECT  pokemon.dex_num, pokemon.name, ab1.name, ab2.name, ab3.name, typ1.name, typ2.name, generations.name, pokemon.id
            FROM legendaries, pokemon, abilities ab1, abilities ab2, abilities ab3, types typ1, types typ2, generations, linking_table
            WHERE 1 = 1
            AND legendaries.name = %s
            AND pokemon.id = linking_table.pokemon_id
            AND ab1.id = linking_table.ability1_id
            AND ab2.id = linking_table.ability2_id
            AND ab3.id = linking_table.ability3_id
            AND typ1.id = linking_table.type1_id
            AND typ2.id = linking_table.type2_id
            AND generations.id = linking_table.generation_id
            AND legendaries.id = linking_table.legendary_id
            ORDER BY pokemon.dex_num ASC;
            '''
    pokemon_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (legendary_category,))
        for row in cursor:
            row = list(row)
            # give a value of NA to any entry that has no value
            for i in range(len(row)):
                if row[i] == '':
                    row[i] = 'NA'

            pokemon_list.append({'dex_num':row[0], 'name':row[1], 'ability1':row[2], 'ability2':row[3],\
                'ability3':row[4], 'type1':row[5], 'type2':row[6], 'generation':row[7], 'id':row[8]})
                
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(pokemon_list)
    
# -------Types Page-------
@api.route('/types')
def get_types():
    ''' Returns a list of all types. 
        By default the list is sorted alphabetically.  
            http://.../types
        Returns an empty list if there's any database failure.
    '''
    query = '''SELECT name FROM types
            ORDER BY name;'''
    type_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, tuple())
        for row in cursor:
            type = row[0]
            type_list.append(type)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(type_list)

@api.route('/type/<search_type>') 
def get_pokemon_from_type(search_type):
    ''' Returns a list of all the pokemon with a given type. 
            http://.../type/<search_type>
        Returns an empty list if there's any database failure.
    '''
    
    query = '''SELECT pokemon.dex_num, pokemon.name, ab1.name, ab2.name, ab3.name, typ1.name, typ2.name, generations.name, pokemon.id
            FROM pokemon, abilities ab1, abilities ab2, abilities ab3, types typ1, types typ2, generations, linking_table
            WHERE 1 = 1
            AND pokemon.id = linking_table.pokemon_id
            AND ab1.id = linking_table.ability1_id
            AND ab2.id = linking_table.ability2_id
            AND ab3.id = linking_table.ability3_id
            AND typ1.id = linking_table.type1_id
            AND typ2.id = linking_table.type2_id
            AND generations.id = linking_table.generation_id
            AND (typ1.name = %s OR typ2.name = %s)
            ORDER BY pokemon.dex_num ASC;'''
    pokemon_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (search_type, search_type,))
        for row in cursor:
            row = list(row)
            # give a value of NA to any entry that has no value
            for i in range(len(row)):
                if row[i] == '':
                    row[i] = 'NA'

            pokemon_list.append({'dex_num':row[0], 'name':row[1], 'ability1':row[2], 'ability2':row[3],\
                'ability3':row[4], 'type1':row[5], 'type2':row[6], 'generation':row[7], 'id':row[8]})
        
        cursor.close()
        connection.close()

    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(pokemon_list)

# -------Egg Types Page-------
@api.route('/egg_groups') 
def get_egg_groups():
    ''' Returns a list of all egg groups. 
        By default the list is sorted alphabetically.  
            http://.../egg_groups
        Returns an empty list if there's any database failure.
    '''
    query = '''SELECT name FROM egg_groups
            ORDER BY name;'''
    egg_group_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, tuple())
        for row in cursor:
            egg_group = row[0]
            egg_group_list.append(egg_group)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(egg_group_list)

@api.route('/egg_group/<egg_group>') 
def get_pokemon_from_egg_group(egg_group):
    ''' Returns a list of all the pokemon in a given egg group. 
            http://.../egg_groups/<egg_group>
        Returns an empty list if there's any database failure.
    '''
    query = '''SELECT pokemon.dex_num, pokemon.name, ab1.name, ab2.name, ab3.name, typ1.name, typ2.name, generations.name, pokemon.id
            FROM pokemon, abilities ab1, abilities ab2, abilities ab3, types typ1, types typ2, generations, egg_groups, linking_table
            WHERE 1 = 1
            AND pokemon.id = linking_table.pokemon_id
            AND ab1.id = linking_table.ability1_id
            AND ab2.id = linking_table.ability2_id
            AND ab3.id = linking_table.ability3_id
            AND typ1.id = linking_table.type1_id
            AND typ2.id = linking_table.type2_id
            AND generations.id = linking_table.generation_id
            AND (egg_groups.id = linking_table.egg_group1_id
            OR egg_groups.id = linking_table.egg_group2_id)
            AND egg_groups.name = %s
            ORDER BY pokemon.dex_num ASC;'''
    pokemon_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (egg_group,))
        for row in cursor:
            row = list(row)
            # give a value of NA to any entry that has no value
            for i in range(len(row)):
                if row[i] == '':
                    row[i] = 'NA'

            pokemon_list.append({'dex_num':row[0], 'name':row[1], 'ability1':row[2], 'ability2':row[3],\
                'ability3':row[4], 'type1':row[5], 'type2':row[6], 'generation':row[7], 'id':row[8]})
                
        cursor.close()
        connection.close()

    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(pokemon_list)
