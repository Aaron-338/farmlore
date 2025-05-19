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
import logging # Added for more detailed logging

# Configure logging for the connector
connector_logger = logging.getLogger(__name__)
# Set a default handler if no handlers are configured
if not connector_logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    connector_logger.addHandler(handler)
    connector_logger.setLevel(logging.INFO)

class PrologConnector:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PrologConnector, cls).__new__(cls)
            try:
                connector_logger.info("Initializing Prolog instance in PrologConnector...")
                cls._instance.prolog = Prolog()
                connector_logger.info("Prolog instance created successfully.")
                
                # Load the knowledge base
                # Log current working directory from within the container for context
                try:
                    cwd = os.getcwd()
                    connector_logger.info(f"[PrologConnector] Current working directory inside container: {cwd}")
                except Exception as e_cwd:
                    connector_logger.error(f"[PrologConnector] Error getting CWD: {e_cwd}")

                script_dir = Path(os.path.dirname(__file__))
                kb_path_obj = script_dir / 'knowledgebase.pl'
                
                connector_logger.info(f"[PrologConnector] Resolved script directory: {script_dir}")
                connector_logger.info(f"[PrologConnector] Attempting to load KB from path object: {kb_path_obj}")
                connector_logger.info(f"[PrologConnector] Does KB file exist at path object? {kb_path_obj.exists()}")
                
                prolog_path_atom = kb_path_obj.as_posix() 
                
                query_string = f"consult('{prolog_path_atom}')"
                connector_logger.info(f"[PrologConnector] Executing consult query: {query_string}")
                
                # Perform the consult
                consult_result = list(cls._instance.prolog.query(query_string))
                connector_logger.info(f"[PrologConnector] Consult query result: {consult_result}")
                # Typically, a successful consult returns an empty list or a list with an empty dict for pyswip.
                # A failure might raise an exception or return specific error structures.
                # Check if the consult was successful (pyswip often raises exception on failure)
                connector_logger.info(f"[PrologConnector] Knowledge base '{prolog_path_atom}' loaded (or consult attempted).")

            except Exception as e:
                connector_logger.error(f"[PrologConnector] CRITICAL ERROR during PrologConnector initialization or KB consult: {e}", exc_info=True)
                # Optionally, re-raise or handle as appropriate. If Prolog cannot be initialized, the service is unusable.
                raise # Re-raise the exception so it's clear initialization failed.
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