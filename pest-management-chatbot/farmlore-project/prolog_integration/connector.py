from pyswip import Prolog
import os

class PrologConnector:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PrologConnector, cls).__new__(cls)
            cls._instance.prolog = Prolog()
            # Load the knowledge base
            kb_path = os.path.join(os.path.dirname(__file__), 'knowledgebase.pl')
            cls._instance.prolog.consult(kb_path)
        return cls._instance
    
    def query(self, query_string):
        """Execute a Prolog query and return results"""
        try:
            results = list(self.prolog.query(query_string))
            return results
        except Exception as e:
            print(f"Prolog query error: {e}")
            return []
    
    def get_pest_solutions(self, pest, region="global"):
        """Get solutions for a specific pest in a region"""
        query = f"pest_solutions({pest}, {region}, Solutions)"
        results = self.query(query)
        if results and 'Solutions' in results[0]:
            return results[0]['Solutions']
        return []
    
    def recommend_solution(self, pest):
        """Get recommended solution for a pest based on IPM priority"""
        query = f"recommend_solution({pest}, Solution)"
        results = self.query(query)
        if results and 'Solution' in results[0]:
            return results[0]['Solution']
        return None
    
    def get_pest_info(self, pest_name):
        """Get detailed information about a pest"""
        query = f"pest(name:{pest_name}, X)"
        results = self.query(query)
        if results:
            return results[0]['X']
        return {}
    
    def get_all_pests(self):
        """Get a list of all pests in the knowledge base"""
        query = "pest(name:Name, _)"
        results = self.query(query)
        return [result['Name'] for result in results]
    
    def get_all_practices(self):
        """Get a list of all practices in the knowledge base"""
        query = "practice(name:Name, _)"
        results = self.query(query)
        return [result['Name'] for result in results]
    
    def get_practice_details(self, practice_name):
        """Get details about a specific practice"""
        query = f"practice(name:{practice_name}, X)"
        results = self.query(query)
        if results:
            return results[0]['X']
        return {}