AUTHORS: Ruben Boero and Serafin Patino

DATA: stats and attributes of all Pokémon from the first 8 generations of Pokémon

The raw data can be found on this site (CC BY-SA 4.0 license):
https://www.kaggle.com/datasets/mariotormo/complete-pokemon-dataset-updated-090420 
We used the 4.20 csv version.


STATUS:
- Search bar on home page and top right of all other pages
    - searches by category (Pokémon name, Pokémon ID number, 
      ability, and type)
    - if no search text is provided, all Pokémon are returned
    - Sends the user to a results page containing
      a table of results. Pokémon name in the table 
      is a link to a specific page about that Pokémon
- Generations page that allows sorting of Pokémon by generations
    - Returns a table of results. Pokémon name in the table 
      is a link to a specific page about that Pokémon
- Legendaries page that allows sorting of Pokémon by legendary
  status (if a Pokémon is a legendary, is not, etc.)
    - Returns a table of results. Pokémon name in the table 
      is a link to a specific page about that Pokémon
- Egg groups page that allows sorting of Pokémon by the egg
  group that they belong to
    - Returns a table of results. Pokémon name in the table 
      is a link to a specific page about that Pokémon
- Types page that allows sorting of Pokémon by their type(s)
    - Returns a table of results. Pokémon name in the table 
      is a link to a specific page about that Pokémon
- The names of Pokémon in the search results table are links
  to a specific page with more in detail about that Pokémon

NOTES:
- We deleted Slowbro from our data because our dataset did 
  not include any information for that Pokémon.
