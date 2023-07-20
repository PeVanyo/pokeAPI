# modules/query2.py
import aiohttp
import json
import os
import asyncio
from datetime import datetime

from .query import Query

class Query2(Query):
    CACHE_FILE = "cache_query2.json"
    UPDATE_TIME = "02:00"

    async def fetch_data(self):
        if os.path.exists(self.CACHE_FILE):
            cache_timestamp = os.path.getmtime(self.CACHE_FILE)
            cache_datetime = datetime.fromtimestamp(cache_timestamp)
            now = datetime.now()

            if cache_datetime.date() < now.date() and now.strftime("%H:%M") >= self.UPDATE_TIME:
                print("Updating cache")
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://pokeapi.co/api/v2/pokemon") as response:
                        data = await response.json()

                with open(self.CACHE_FILE, "w") as f:
                    json.dump(data, f)
            else:
                print("Using cache")
                with open(self.CACHE_FILE, "r") as f:
                    data = json.load(f)
        else:
            print("Using remote")
            async with aiohttp.ClientSession() as session:
                async with session.get("https://pokeapi.co/api/v2/pokemon") as response:
                    data = await response.json()

            with open(self.CACHE_FILE, "w") as f:
                json.dump(data, f)

        return data

    async def compute_answer(self, data):
        total_abilities = 0
        total_species = len(data['results'])
        
        async def fetch_species_abilities(species_url):
            async with aiohttp.ClientSession() as session:
                async with session.get(species_url) as response:
                    return await response.json()

        async def count_species_abilities(species):
            species_response = await fetch_species_abilities(species['url'])
            abilities = species_response['abilities']
            return len(abilities)
        
        tasks = [count_species_abilities(species) for species in data['results']]
        total_abilities = sum(await asyncio.gather(*tasks))
        average_abilities = total_abilities / total_species
        
        return average_abilities
