CREATE TABLE pokemon (
    id SERIAL,
    dex_num integer,
    name text,
    hp float,
    atk float,
    def float,
    spatk float,
    spdef float,
    spd float
);

CREATE TABLE egg_groups (
    id SERIAL,
    name text
);

CREATE TABLE types (
    id SERIAL,
    name text
);

CREATE TABLE legendaries (
    id SERIAL,
    name text
);

CREATE TABLE abilities (
    id SERIAL,
    name text
);


CREATE TABLE generations (
    id SERIAL,
    name text
);

CREATE TABLE linking_table (
    pokemon_id integer,
    type1_id integer,
    type2_id integer,
    ability1_id integer,
    ability2_id integer,
    ability3_id integer,
    generation_id integer,
    egg_group1_id integer,
    egg_group2_id integer,
    legendary_id integer,
    height float,
    weight float,
    normal_resist float,
    fire_resist float,
    water_resist float,
    electric_resist float,
    grass_resist float,
    ice_resist float,
    fighting_resist float,
    poison_resist float,
    ground_resist float,
    flying_resist float,
    psychic_resist float,
    bug_resist float,
    rock_resist float,
    ghost_resist float,
    dragon_resist float,
    dark_resist float,
    steel_resist float,
    fairy_resist float
);