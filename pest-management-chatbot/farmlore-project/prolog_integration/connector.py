import os
# Try to guide pyswip if SWI_HOME_DIR is not set, using the path from the warning.
# This must be done BEFORE 'from pyswip import Prolog'
if 'SWI_HOME_DIR' not in os.environ:
    # Path from the warning: "c:/program files/swipl"
    potential_swi_home = 'C:/Program Files/swipl' # Use a consistent format
    if os.path.isdir(potential_swi_home) and os.path.isdir(os.path.join(potential_swi_home, 'bin')):
        print(f"[PrologConnector] Attempting to set SWI_HOME_DIR to: {potential_swi_home}")
        os.environ['SWI_HOME_DIR'] = potential_swi_home
    else:
        print(f"[PrologConnector] SWI_HOME_DIR not set and default '{potential_swi_home}' not found or invalid.")

# Now import Prolog
from pyswip import Prolog
from pathlib import Path

class PrologConnector:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PrologConnector, cls).__new__(cls)
            cls._instance.prolog = Prolog()
            # Load the knowledge base
            kb_path_obj = Path(os.path.dirname(__file__)) / 'knowledgebase.pl'
            prolog_path_atom = kb_path_obj.as_posix() # e.g., 'C:/Users/user/file.pl'
            
            query_string = f"consult('{prolog_path_atom}')"
            print(f"[PrologConnector] Executing consult query: {query_string}")
            try:
                list(cls._instance.prolog.query(query_string))
            except Exception as e:
                print(f"[PrologConnector] Error during explicit consult query: {e}")
                # Optionally, re-raise or handle as appropriate
                raise
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