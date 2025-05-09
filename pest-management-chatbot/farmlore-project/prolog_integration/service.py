from .connector import PrologConnector
import logging # Add logging

logger = logging.getLogger(__name__)

class PrologService:
    def __init__(self):
        self.connector = PrologConnector()

    # Helper function to parse the ['key:value', ...] list from Prolog frame queries
    def _parse_frame_attributes(self, attributes_list: list) -> dict:
        attrs_dict = {}
        if not isinstance(attributes_list, list):
            logger.warning(f"_parse_frame_attributes received non-list input: {type(attributes_list)}")
            return attrs_dict
        for attr_str in attributes_list:
            if isinstance(attr_str, str) and ':' in attr_str:
                try:
                    key, val = attr_str.split(':', 1)
                    key = key.strip()
                    val = val.strip()
                    # Handle list-like values stored as strings '[a,b,c]'
                    if val.startswith('[') and val.endswith(']') and len(val) > 2:
                        # Simple split, might need refinement for complex list elements (e.g., containing commas)
                        parsed_list = [item.strip() for item in val[1:-1].split(',')]
                        attrs_dict[key] = parsed_list
                    elif val.lower() in ['true', 'false']:
                        attrs_dict[key] = val.lower() == 'true'
                    elif val.isdigit():
                        attrs_dict[key] = int(val)
                    # Add more type conversions if needed (floats, etc.)
                    else:
                        attrs_dict[key] = val # Store as string
                except Exception as e:
                    logger.error(f"Error parsing attribute string '{attr_str}': {e}")
            else:
                 logger.warning(f"Skipping unexpected attribute format: {attr_str}")
        return attrs_dict

    # Existing _get_practice_details needs updating to use the parser
    # Make it public as it seems useful directly
    def get_practice_details(self, practice_name):
        """Get details for a specific practice (Updated)"""
        practice_name_lower = practice_name.lower()
        query = f"practice(name:{practice_name_lower}, X)"
        results = self.connector.query(query)
        if results and isinstance(results[0].get('X'), list):
            attributes = results[0]['X']
            # Use the parser
            parsed_details = self._parse_frame_attributes(attributes)
            parsed_details['name'] = practice_name # Ensure original casing for name
            return parsed_details
        logger.warning(f"Details not found for practice: {practice_name}")
        return {'name': practice_name, 'error': 'Details not found'} # Return structure indicating failure

    # New method for crop details
    def get_crop_details(self, crop_name):
        """Get details for a specific crop"""
        crop_name_lower = crop_name.lower()
        query = f"crop(name:{crop_name_lower}, X)"
        results = self.connector.query(query)
        if results and isinstance(results[0].get('X'), list):
            attributes = results[0]['X']
            # Use the parser
            parsed_details = self._parse_frame_attributes(attributes)
            parsed_details['name'] = crop_name # Ensure original casing for name
            return parsed_details
        logger.warning(f"Details not found for crop: {crop_name}")
        return {'name': crop_name, 'error': 'Details not found'}

    # Existing get_pest_solutions - update to use get_practice_details
    def get_pest_solutions(self, pest, region="global"):
        """Get solutions for a pest in a specific region with details (Updated)"""
        solution_names = self.connector.get_pest_solutions(pest, region) # Connector returns list of solution names
        formatted = []
        if not isinstance(solution_names, list):
             logger.error(f"Connector returned non-list solutions for {pest}: {type(solution_names)}")
             return formatted
        for solution_name in solution_names:
            if isinstance(solution_name, str):
                 # Get details using the updated get_practice_details
                 details = self.get_practice_details(solution_name)
                 formatted.append(details) # Append the whole details dict
            else:
                 logger.warning(f"Skipping non-string solution name: {solution_name}")
        return formatted

    # Existing recommend_solution - update to use get_practice_details
    def recommend_solution(self, pest):
        """Get the recommended solution for a pest with details (Updated)"""
        solution_name = self.connector.recommend_solution(pest) # Returns name
        if solution_name and isinstance(solution_name, str):
            # Get details using the updated get_practice_details
            details = self.get_practice_details(solution_name)
            return details # Return the whole details dict
        elif solution_name:
             logger.warning(f"recommend_solution connector returned non-string name: {solution_name}")
        return None

    def get_pest_info(self, pest_name):
        """Get comprehensive information about a pest"""
        # Query for pest details using the frame structure
        pest_name_lower = pest_name.lower()
        query = f"pest(name:{pest_name_lower}, X)"
        results = self.connector.query(query)
        
        if results and isinstance(results[0].get('X'), list):
             attributes = results[0]['X']
             parsed_details = self._parse_frame_attributes(attributes)
             parsed_details['name'] = pest_name # Ensure original casing
             return parsed_details
        logger.warning(f"Details not found for pest: {pest_name}")
        return None # Consistent return type (or dict with error)

    def search_prolog_kb(self, query_text):
        """
        Process a natural language query to find related information
        in the Prolog knowledge base
        """
        # Look for pest names in the query
        try:
            all_pests = self.connector.get_all_pests()
            if not isinstance(all_pests, list):
                 logger.error(f"get_all_pests returned non-list: {type(all_pests)}")
                 all_pests = []
        except Exception as e:
             logger.error(f"Error calling get_all_pests: {e}")
             all_pests = []

        found_pest_info = None
        for pest in all_pests:
            if isinstance(pest, str) and pest.lower() in query_text.lower():
                # Found a pest reference, get details
                pest_info = self.get_pest_info(pest) # Use updated method
                if pest_info and not pest_info.get('error'):
                    solutions = self.get_pest_solutions(pest) # Use updated method
                    recommendation = self.recommend_solution(pest) # Use updated method
                    found_pest_info = {
                        'pest_found': pest,
                        'pest_info': pest_info,
                        'solutions': solutions,
                        'recommendation': recommendation
                    }
                    break # Stop after first pest match for simplicity
        
        if found_pest_info: return found_pest_info

        # Look for practice names in the query
        try:
             all_practices = self.connector.get_all_practices()
             if not isinstance(all_practices, list):
                  logger.error(f"get_all_practices returned non-list: {type(all_practices)}")
                  all_practices = []
        except Exception as e:
             logger.error(f"Error calling get_all_practices: {e}")
             all_practices = []
             
        found_practice_info = None
        for practice in all_practices:
            if isinstance(practice, str) and practice.lower() in query_text.lower():
                # Get practice details
                practice_info = self.get_practice_details(practice) # Use updated method
                if practice_info and not practice_info.get('error'):
                    found_practice_info = {
                        'practice_found': practice,
                        'practice_info': practice_info
                    }
                    break # Stop after first practice match

        if found_practice_info: return found_practice_info
        
        # No specific entity found
        return {
            'generic_response': True,
            'message': "I couldn't find specific information about that in my knowledge base."
        } 