# modules/query.py
import abc

class Query(abc.ABC):
    def fetch_data(self):
        raise NotImplementedError
    
        pass

    def compute_answer(self, data):
        raise NotImplementedError
    
        pass

