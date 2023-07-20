# modules/query1.py
import aiohttp
import asyncio
from .query import Query
import json
import os
from datetime import datetime

class Query1(Query):
    CACHE_FILE = "cache_query1.json"
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
        num_species_with_evolution_ability = 0
        total_species = len(data["results"])

        async def fetch_species_ability(species_url):
            async with aiohttp.ClientSession() as session:
                async with session.get(species_url) as response:
                    return await response.json()

        async def check_species_ability(species):
            species_response = await fetch_species_ability(species["url"])
            abilities = species_response["abilities"]

            for ability in abilities:
                if ability["is_hidden"]:
                    return True
            return False

        tasks = [check_species_ability(species) for species in data["results"]]
        results = await asyncio.gather(*tasks)
        num_species_with_evolution_ability = sum(results)

        percentage = (num_species_with_evolution_ability / total_species) * 100
        return percentage
