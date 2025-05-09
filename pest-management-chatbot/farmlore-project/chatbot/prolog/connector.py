from pyswip import Prolog
import os

class PrologConnector:
    def __init__(self):
        self.prolog = Prolog()
        # Load the knowledge base
        kb_path = os.path.join(os.path.dirname(__file__), 'knowledgebase.pl')
        self.prolog.consult(kb_path)
    
    def query(self, query_string):
        """Execute a Prolog query and return results"""
        try:
            results = list(self.prolog.query(query_string))
            return results
        except Exception as e:
            print(f"Prolog query error: {e}")
            return []
    
    def get_pest_solutions(self, pest, region):
        """Get solutions for a specific pest in a region"""
        query = f"pest_solutions({pest}, {region}, Solutions)"
        results = self.query(query)
        if results:
            return results[0]['Solutions']
        return []
    
    def recommend_solution(self, pest):
        """Get recommended solution for a pest based on IPM priority"""
        query = f"recommend_solution({pest}, Solution)"
        results = self.query(query)
        if results:
            return results[0]['Solution']
        return None
    
    def get_pest_info(self, pest):
        """Get information about a pest"""
        query = f"pest(name:{pest}, Type)"
        results = self.query(query)
        if results:
            return results[0]['Type']
        return None
    
    def check_intervention_needed(self, pest, crop):
        """Check if intervention is needed based on thresholds"""
        query = f"intervention_needed({pest}, {crop})"
        results = list(self.prolog.query(query))
        return len(results) > 0