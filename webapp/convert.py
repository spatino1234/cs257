#this file was created by Ruben Boero and Serafin Patino
# https://www.kaggle.com/datasets/mariotormo/complete-pokemon-dataset-updated-090420 
# This is a link to the database
# we're using the 4.20 csv version, we also deleted line 241 which
# contained slowking, as all his data was empty
import csv

dict_of_pokemon= {}
dict_of_types = {}
dict_of_legendaries = {}
dict_of_generations = {}
dict_of_egg_groups = {}
dict_of_abilities = {}

# note we renamed the kaggle csv to 'pokemon_data.csv'
with open ('pokemon_data.csv', 'r') as read_file, \
    open ('pokedex.csv', 'w') as pokedex_file, \
    open ('types.csv', 'w') as types_file, \
    open ('egg_groups.csv', 'w') as egg_file, \
    open ('abilities.csv', 'w') as abilities_file:
        reader = csv.reader(read_file, delimiter = ',')
        pokemon_writer = csv.writer(pokedex_file)
        ability_writer = csv.writer(abilities_file)
        type_writer = csv.writer(types_file)
        egg_group_writer = csv.writer(egg_file)

        next(reader) # skips the header line in the csv file

        # if the ability is not present in the csv, i.e. it's an empty string. give val of 0
        # (this happens if a pokemon doesnt have the max number of abilities)
        dict_of_abilities[''] = 0
        ability_writer.writerow([0, ''])

        # if the type is not present in the csv, i.e. it's an empty string. give val of 0
        dict_of_types[''] = 0
        type_writer.writerow([0, ''])

        dict_of_egg_groups[''] = 0
        egg_group_writer.writerow([0, ''])

        for row in reader:
            # ---- Creating pokedex.csv ----

            dex_num = row[1]
            name = row[2]
            hp = row[20]
            atk = row[21]
            defense = row[22]
            sp_atk = row[23]
            sp_defense = row[24]
            speed = row[25]
            id = len(dict_of_pokemon) # starts at 0, when added it updates
            dict_of_pokemon[name] = id
            pokemon_writer.writerow([id, dex_num, name, hp, atk, defense, sp_atk, sp_defense, speed])

            # ---- Creating abilities.csv ----

            ability1 = row[16]
            ability2 = row[17]
            ability3 = row[18]

            # if the ability is not in the dictionary, add it to the dictionary and the csv
            if ability1 not in dict_of_abilities:
                id = len(dict_of_abilities)
                dict_of_abilities[ability1] = id
                ability_writer.writerow([id, ability1])

            if ability2 not in dict_of_abilities:
                id = len(dict_of_abilities)
                dict_of_abilities[ability2] = id
                ability_writer.writerow([id, ability2])
                
            if ability3 not in dict_of_abilities:
                id = len(dict_of_abilities)
                dict_of_abilities[ability3] = id
                ability_writer.writerow([id, ability3])

            # ---- Creating types.csv ----

            type1 = row[11]
            type2 = row[12]

            # if the ability is not in the dictionary, add it to the dictionary and the csv
            if type1 not in dict_of_types:
                id = len(dict_of_types)
                dict_of_types[type1] = id
                type_writer.writerow([id, type1])
            
            if type2 not in dict_of_types:
                id = len(dict_of_types)
                dict_of_types[type2] = id
                type_writer.writerow([id, type2])
            
            # ---- Creating the egg_group.csv ----

            group1 = row[31]
            group2 = row[32]

            # if the egg group is not in the dictionary, add it to the dictionary and the csv
            if group1 not in dict_of_egg_groups:
                id = len(dict_of_egg_groups)
                dict_of_egg_groups[group1] = id
                egg_group_writer.writerow([id, group1])
                
            if group2 not in dict_of_egg_groups:
                id = len(dict_of_egg_groups)
                dict_of_egg_groups[group2] = id
                egg_group_writer.writerow([id, group2])
                
# Creating the csv of legendaries
with open ('legendaries.csv', 'w') as write_file:
    legendary_writer = csv.writer(write_file)

    dict_of_legendaries['non-legendary'] = 0
    legendary_writer.writerow([0, 'non-legendary'])

    dict_of_legendaries['legendary'] = 1
    legendary_writer.writerow([1, 'legendary'])

    dict_of_legendaries['sub-legendary'] = 2
    legendary_writer.writerow([2, 'sub-legendary'])

    dict_of_legendaries['mythical'] = 3
    legendary_writer.writerow([3, 'mythical'])

# Creating the csv of generations
with open ('generations.csv', 'w') as write_file:
    generation_writer = csv.writer(write_file)

    for i in range(1, 9):
        dict_of_generations['generation ' + str(i)] = i
        generation_writer.writerow([i, 'generation ' + str(i)])


# create the linking table
with open ('pokemon_data.csv', 'r') as read_file, \
    open ('linking_table.csv', 'w') as write_file:

    linking_reader = csv.reader(read_file)
    linking_writer = csv.writer(write_file)

    next(linking_reader)


    for row in linking_reader:

        name = row[2]

        generation_num = row[5]

        is_sub_legendary = row[6]
        is_legendary = row[7]
        is_mythic = row[8]

        ability1 = row[16]
        ability2 = row[17]
        ability3 = row[18]

        type1 = row[11]
        type2 = row[12]

        group1 = row[31]
        group2 = row[32]

        height = row[13]
        weight = row[14]
        normal_resist = row [35]
        fire_resist = row [36]
        water_resist = row [37]
        electric_resist = row[38]
        grass_resist = row [39]
        ice_resist = row[40]
        fighting_resist = row[41]
        poison_resist = row [42]
        ground_resist = row[43]
        flying_resist = row[44]
        psychic_resist = row[45]
        bug_resist = row[46]
        rock_resist = row[47]
        ghost_resist = row[48]
        dragon_resist = row[49]
        dark_resist = row [50]
        steel_resist = row[51]
        fairy_resist = row[52]

        pokemon_id = dict_of_pokemon[name]
        generation_id = dict_of_generations['generation ' + generation_num]
        ability1_id = dict_of_abilities[ability1]
        ability2_id = dict_of_abilities[ability2]
        ability3_id = dict_of_abilities[ability3]

        type1_id = dict_of_types[type1]
        type2_id = dict_of_types[type2]

        group1_id = dict_of_egg_groups[group1]
        group2_id = dict_of_egg_groups[group2]
        
        if is_sub_legendary == str(1):
            legendary_id = dict_of_legendaries['sub-legendary']
        elif is_legendary == str(1):
            legendary_id = dict_of_legendaries['legendary']
        elif is_mythic == str(1):
            legendary_id = dict_of_legendaries['mythical']
        else:
            legendary_id = dict_of_legendaries['non-legendary']

        linking_writer.writerow([pokemon_id, type1_id, type2_id, ability1_id, ability2_id, \
            ability3_id,generation_id, group1_id, group2_id, legendary_id, height, weight, \
            normal_resist, fire_resist, water_resist, electric_resist, grass_resist, \
            ice_resist, fighting_resist, poison_resist,ground_resist, flying_resist, \
            psychic_resist, bug_resist, rock_resist, ghost_resist, dragon_resist, \
            dark_resist, steel_resist, fairy_resist])

    
