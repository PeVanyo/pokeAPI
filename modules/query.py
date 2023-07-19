# modules/query.py

class Query:
    def fetch_data(self):
        raise NotImplementedError

    def compute_answer(self, data):
        raise NotImplementedError

