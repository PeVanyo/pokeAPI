# main.py
import sys
from modules.query1 import Query1
from modules.query2 import Query2

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the question number (0 for query1, 1 for query2) as an argument.")
        sys.exit(1)
    
    question_number = int(sys.argv[1])
    
    # Create an instance of the selected query class
    if question_number == 0:
        query = Query1()
    elif question_number == 1:
        query = Query2()
    else:
        print("Invalid question number. Please provide 0 for query1 or 1 for query2.")
        sys.exit(1)
    
    # Fetch the data and compute the answer
    data = query.fetch_data()
    answer = query.compute_answer(data)
    
    # Print the answer to STDOUT
    if isinstance(query, Query1):
        print(f"The percentage of Pokemon species with evolution ability: {answer:.2f}%")
    elif isinstance(query, Query2):
        print(f"The average number of abilities per Pokemon species with hidden abilities: {answer:.2f}")

