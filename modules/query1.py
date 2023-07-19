import requests
from .query import Query
import json
import os

class Query1(Query):
    CACHE_FILE = "cache_query1.json"

    def fetch_data(self):
        if os.path.exists(self.CACHE_FILE):
            with open(self.CACHE_FILE, "r") as f:
                data = json.load(f)
        else:
            response = requests.get("https://pokeapi.co/api/v2/pokemon")
            data = response.json()

            with open(self.CACHE_FILE, "w") as f:
                json.dump(data, f)

        return data

    def compute_answer(self, data):
        num_species_with_evolution_ability = 0
        total_species = len(data["results"])

        for species in data["results"]:
            species_response = requests.get(species["url"]).json()
            abilities = species_response["abilities"]

            for ability in abilities:
                if ability["is_hidden"]:
                    num_species_with_evolution_ability += 1
                    break

        percentage = (num_species_with_evolution_ability / total_species) * 100
        return percentage
