# main.py
import sys
import asyncio
from modules.query1 import Query1
from modules.query2 import Query2

QUESTION_NUMBER = 0

async def main():
    # Create an instance of the selected query class
    if QUESTION_NUMBER == 0:
        query = Query1()
    elif QUESTION_NUMBER == 1:
        query = Query2()
    else:
        print("Invalid question number. Please provide 0 for query1 or 1 for query2.", file=sys.stderr)
        sys.exit(1)

    # Fetch the data and compute the answer asynchronously
    data = await query.fetch_data()
    answer = await query.compute_answer(data)  # Use await here

    # Print the answer to STDOUT
    if isinstance(query, Query1):
        print(f"The percentage of Pokemon species with evolution ability: {answer:.2f}%", file=sys.stdout)
    elif isinstance(query, Query2):
        print(f"The average number of abilities per Pokemon species with hidden abilities: {answer:.2f}", file=sys.stdout)

if __name__ == "__main__":
    asyncio.run(main())
