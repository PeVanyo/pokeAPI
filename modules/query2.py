# modules/query2.py
import requests
from .query import Query

class Query2(Query):
    def fetch_data(self):
        response = requests.get('https://pokeapi.co/api/v2/pokemon')
        data = response.json()
        return data

    def compute_answer(self, data):
        total_abilities = 0
        total_species = len(data['results'])
        
        for species in data['results']:
            species_response = requests.get(species['url']).json()
            abilities = species_response['abilities']
            total_abilities += len(abilities)
        
        average_abilities = total_abilities / total_species
        
        return average_abilities
