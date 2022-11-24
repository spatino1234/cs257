'''
    app.py
    Jeff Ondich, 25 April 2016
    Updated 8 November 2021

    Modified by Ruben Boero and Serafin Patino
'''
import flask
import argparse
import api
import sys
import config
import psycopg2

app = flask.Flask(__name__, static_folder='static', template_folder='templates')
app.register_blueprint(api.api, url_prefix='/api')

api = flask.Blueprint('api', __name__)

def get_connection():
    ''' Returns a connection to the database described in the
        config module. May raise an exception as described in the
        documentation for psycopg2.connect. '''
    return psycopg2.connect(database=config.database,
                            user=config.user,
                            password=config.password)

def get_query_results_and_url(query, num_of_inputs, search_text):
    pokemon_list = []
    url = []

    try:
        connection = get_connection()
        cursor = connection.cursor()

        # the execute line is differente depending on which category is being searched
        if num_of_inputs == 0:
            cursor.execute(query,)
        elif num_of_inputs == 1:
            cursor.execute(query, (search_text,))
        elif num_of_inputs == 2:
            cursor.execute(query, (search_text, search_text,))
        elif num_of_inputs == 3:
            cursor.execute(query, (search_text, search_text, search_text,))

        for row in cursor:
            row = list(row)
            for i in range(len(row)):
                row[i] = str(row[i])
                # give a value of NA to any entry that has no value
                if row[i] == '':
                    row[i] = 'NA'

            pokemon_list.append({'dex_num':row[0], 'name':row[1], 'ability1':row[2], 'ability2':row[3],\
                'ability3':row[4], 'type1':row[5], 'type2':row[6], 'generation':row[7], 'id':row[8]})

            url.append('specific' + '/' + row[8])
                
        cursor.close()
        connection.close()

        return pokemon_list, url

    except Exception as e:
        print(e, file=sys.stderr)

@app.route('/')
def home():
    return flask.render_template('index.html')

@app.route('/api/help')
def help():
    with open('help.txt', 'r') as file:
        content = file.read()
    
    return flask.Response(content, mimetype='text/plain')
    
@app.route('/generations') 
def generations():
    return flask.render_template('generations.html')

@app.route('/legendaries') 
def legendaries():
    return flask.render_template('legendaries.html')

@app.route('/egg_groups') 
def egg_groups():
    return flask.render_template('egg_groups.html')

@app.route('/types') 
def types():
    return flask.render_template('types.html')

# queries the DB for all relevant information about a pokemon then passes it into pokedex.html
# in order to display it on that page
@app.route('/specific/<id>')
def pokedex(id):

    query = '''SELECT pokemon.dex_num, pokemon.name, ab1.name, ab2.name, ab3.name, typ1.name, typ2.name, linking_table.height, linking_table.weight, linking_table.normal_resist, linking_table.fire_resist, linking_table.water_resist, linking_table.electric_resist, linking_table.grass_resist, linking_table.ice_resist, linking_table.fighting_resist, linking_table.poison_resist, linking_table.ground_resist, linking_table.flying_resist, linking_table.psychic_resist, linking_table.bug_resist, linking_table.rock_resist, linking_table.ghost_resist, linking_table.dragon_resist, linking_table.dark_resist, linking_table.steel_resist, linking_table.fairy_resist, pokemon.hp, pokemon.atk, pokemon.def, pokemon.spatk, pokemon.spdef, pokemon.spd
            FROM pokemon, abilities ab1, abilities ab2, abilities ab3, types typ1, types typ2, linking_table
            WHERE 1 = 1
            AND pokemon.id = linking_table.pokemon_id
            AND ab1.id = linking_table.ability1_id
            AND ab2.id = linking_table.ability2_id
            AND ab3.id = linking_table.ability3_id
            AND typ1.id = linking_table.type1_id
            AND typ2.id = linking_table.type2_id
            AND pokemon.id = %s;'''
    
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(query, (id,))

        for row in cursor:
            row = list(row)
            # give a value of NA to any entry that has no value
            for i in range(len(row)):
                row[i] = str(row[i])
                if row[i] == '':
                    row[i] = 'NA'

            dex_num = row[0]
            name = row[1]
            ability1 = row[2]
            ability2 = row[3]
            ability3 = row[4]
            type1 = row[5]
            type2 = row[6]
            height = row[7]
            weight = row[8]
            normal_resist = row[9]
            fire_resist = row[10]
            water_resist = row[11] 
            electric_resist = row[12]
            grass_resist = row[13]
            ice_resist = row[14]
            fighting_resist = row[15]
            poison_resist = row[16]
            ground_resist = row[17]
            flying_resist = row[18]
            psychic_resist = row[19]
            bug_resist = row[20] 
            rock_resist = row[21]
            ghost_resist = row[22]
            dragon_resist = row[23] 
            dark_resist = row[24] 
            steel_resist = row[25]
            fairy_resist = row[26]
            hp = row[27]
            atk = row[28]
            defense = row[29]
            spatk = row[30]
            spdef = row[31]
            spd = row[32]
                
        cursor.close()
        connection.close()

        return flask.render_template('pokedex.html', dex_num = dex_num, name = name, ability1 = ability1, \
            ability2 = ability2, ability3 = ability3, type1 = type1, type2 = type2, height = height, weight = weight,\
            normal_resist = normal_resist, fire_resist = fire_resist, water_resist = water_resist, electric_resist = \
            electric_resist, grass_resist = grass_resist, ice_resist = ice_resist, fighting_resist = fighting_resist,\
            poison_resist = poison_resist, ground_resist = ground_resist, flying_resist = flying_resist, \
            psychic_resist = psychic_resist, bug_resist = bug_resist, rock_resist = rock_resist, ghost_resist = \
            ghost_resist, dragon_resist = dragon_resist, dark_resist = dark_resist, steel_resist = steel_resist, \
            fairy_resist = fairy_resist, hp = hp, atk = atk, defense = defense, spatk = spatk, spdef = spdef, \
            spd = spd)

    except Exception as e:
        print(e, file=sys.stderr)

# queries the database for information relevant to the results table that is shown to the 
# user when they have used the search feature
@app.route('/search_results/<category>/<search_text>')
def display_search_results(category, search_text):

    if search_text == 'default':
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
                ORDER BY pokemon.dex_num ASC;'''

    elif category == 'pokemon':
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
                AND pokemon.name ILIKE CONCAT ('%%',%s,'%%')
                ORDER BY pokemon.dex_num ASC;'''

    elif category == 'pokedex_number':
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
                AND pokemon.dex_num = %s
                ORDER BY pokemon.dex_num ASC;'''

    elif category == 'ability':
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
                AND (ab1.name ILIKE CONCAT ('%%',%s,'%%')
                OR ab2.name ILIKE CONCAT ('%%',%s,'%%') 
                OR ab3.name ILIKE CONCAT ('%%',%s,'%%'))
                ORDER BY pokemon.dex_num ASC;'''

    elif category == 'type':
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
                AND (typ1.name ILIKE CONCAT ('%%',%s,'%%') OR typ2.name ILIKE CONCAT ('%%',%s,'%%'))
                ORDER BY pokemon.dex_num ASC;'''

    # if there is no search text, return all pokemon
    if search_text == 'default':
        result = get_query_results_and_url(query, 0, '')
        pokemon_list = result[0]
        url = result[1]
        
        # return the list of dictionaries to the search results page, then parse it inside HTML
        return flask.render_template('search_results.html', search_results=pokemon_list, url=url)

    elif category == 'pokemon' or category == 'pokedex_number':
        result = get_query_results_and_url(query, 1, search_text)
        pokemon_list = result[0]
        url = result[1]
        
        # return the list of dictionaries to the search results page, then parse it inside HTML
        return flask.render_template('search_results.html', search_results=pokemon_list, url=url)
    
    elif category == 'ability':
        result = get_query_results_and_url(query, 3, search_text)
        pokemon_list = result[0]
        url = result[1]

        # return the list of dictionaries to the search results page, then parse it inside HTML
        return flask.render_template('search_results.html', search_results=pokemon_list, url=url)
    
    elif category == 'type':
        result = get_query_results_and_url(query, 2, search_text)
        pokemon_list = result[0]
        url = result[1]

        # return the list of dictionaries to the search results page, then parse it inside HTML
        return flask.render_template('search_results.html', search_results=pokemon_list, url=url)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A Pokémon search engine/database')
    parser.add_argument('host', help='the host to run on')
    parser.add_argument('port', type=int, help='the port to listen on')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
