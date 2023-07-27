import requests
import pandas as pd
import json
class Pokemon: 

    def __init__(self,name):
        self.id = None
        self.name = name
        self.height = None
        self.weight = None
        self.evolution = None
        self._fetch_data()
    
    def _fetch_data(self):
        try: 
            url = "https://pokeapi.co/api/v2/pokemon/" + self.name.lower()

            response = requests.get(url)
            data = response.json()

            
            self.id = data["id"]
            self.weight = data["weight"]
            self.height = data["height"]
            self.pictureFront = data["sprites"]["other"]["official-artwork"]["front_default"]
            self.abilities = data["abilities"]
            self.types = data["types"]
            self.type1 = data["types"][0]["type"]["name"]
            self.type2 = data["types"][1]["type"]["name"]
            self.stats = data["stats"]
        except Exception as e:
            print(f"Error fetching data for {self.name}: {e}")
            
    def get_list_of_abilities(self):
        abilities = []
        for i in range(len(self.abilities)):
            abilities.append(self.abilities[i]["ability"]["name"])
        return abilities
    
    def find_latAndLong_from_dataset(self):
        df = pd.read_csv("300k.csv")
        pokemonLat = [] 
        pokemonLong = []
        for i in range(len(df)):
            if df["pokemonId"][i] == self.id:
                pokemonLat.append(df["latitude"][i])
                pokemonLong.append(df["longitude"][i])
        
        return [pokemonLat, pokemonLong]
    
    def get_list_of_stats(self):
        df = pd.read_csv("pokemon.csv")
        pokemonStats = df[df["Name"] == self.name.capitalize()]
        pokemonHp = pokemonStats["HP"].values[0]
        pokemonAttack = pokemonStats["Attack"].values[0]
        pokemonDefense = pokemonStats["Defense"].values[0]
        pokemonSpAtk = pokemonStats["Sp. Atk"].values[0]
        pokemonSpDef = pokemonStats["Sp. Def"].values[0]
        pokemonSpeed = pokemonStats["Speed"].values[0]
        return [pokemonHp, pokemonAttack,pokemonDefense,pokemonSpAtk,pokemonSpDef,pokemonSpeed]
    
        
    def get_list_of_all_pokemon():
        url = "https://pokeapi.co/api/v2/pokemon?limit=721"
        response = requests.get(url)
        pokemon = json.loads(response.text)
        pokemonList = []
        for i in range(len(pokemon["results"])):
            pokemonList.append(pokemon["results"][i]["name"])
        return pokemonList
    
    def get_number_of_types(self):
        num = 0 
        for i in range(len(self.types)):
            num += 1
        return num
    
    def get_evolution(self):  
        evolutionUrl = "https://pokeapi.co/api/v2/evolution-chain/" + str(self.id)
        evolutionResponse = requests.get(evolutionUrl)
        evolutionData = evolutionResponse.json()
        self.evolution = evolutionData["chain"]["evolves_to"][0]["species"]["name"]
        return self.evolution
    
    def get_evolution_level(self):
        evolutionUrl = "https://pokeapi.co/api/v2/evolution-chain/" + str(self.id)
        evolutionResponse = requests.get(evolutionUrl)
        evolutionData = evolutionResponse.json()
        self.evolutionLevel = evolutionData["chain"]["evolves_to"][0]["evolution_details"][0]["min_level"]
        return str(self.evolutionLevel)