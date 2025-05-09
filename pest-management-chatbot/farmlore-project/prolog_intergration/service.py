from .connector import PrologConnector

class PrologService:
    def __init__(self):
        self.connector = PrologConnector()
    
    def get_pest_solutions(self, pest, region="global"):
        """Get solutions for a pest in a specific region with details"""
        solutions = self.connector.get_pest_solutions(pest, region)
        formatted = []
        
        for solution in solutions:
            # Get practice details
            query = f"practice(name:{solution}, type:Type, description:Desc, cost:Cost, difficulty:Diff)"
            results = self.connector.query(query)
            
            details = {}
            if results:
                details = {
                    'name': solution,
                    'type': results[0].get('Type', 'Unknown'),
                    'description': results[0].get('Desc', 'No description available'),
                    'cost': results[0].get('Cost', 'Unknown'),
                    'difficulty': results[0].get('Diff', 'Unknown')
                }
            else:
                details = {
                    'name': solution,
                    'description': 'No details available'
                }
                
            formatted.append(details)
            
        return formatted
    
    def recommend_solution(self, pest):
        """Get the recommended solution for a pest with details"""
        solution = self.connector.recommend_solution(pest)
        
        if solution:
            # Get practice details
            query = f"practice(name:{solution}, type:Type, description:Desc, cost:Cost, difficulty:Diff)"
            results = self.connector.query(query)
            
            if results:
                details = {
                    'name': solution,
                    'type': results[0].get('Type', 'Unknown'),
                    'description': results[0].get('Desc', 'No description available'),
                    'cost': results[0].get('Cost', 'Unknown'),
                    'difficulty': results[0].get('Diff', 'Unknown')
                }
                return details
                
        return None
    
    def get_pest_info(self, pest_name):
        """Get comprehensive information about a pest"""
        # Query for pest details
        query = f"pest(name:{pest_name}, type:Type, scientific_name:SciName, symptoms:Symptoms, monitoring:Monitoring, controls:Controls)"
        results = self.connector.query(query)
        
        if results:
            return {
                'name': pest_name,
                'type': results[0].get('Type', 'Unknown'),
                'scientific_name': results[0].get('SciName', 'Unknown'),
                'symptoms': results[0].get('Symptoms', []),
                'monitoring': results[0].get('Monitoring', []),
                'controls': results[0].get('Controls', [])
            }
        return None
    
    def search_prolog_kb(self, query_text):
        """
        Process a natural language query to find related information
        in the Prolog knowledge base
        """
        # Look for pest names in the query
        all_pests = self.connector.get_all_pests()
        for pest in all_pests:
            if pest.lower() in query_text.lower():
                # Found a pest reference, get solutions
                solutions = self.get_pest_solutions(pest)
                recommendation = self.recommend_solution(pest)
                pest_info = self.get_pest_info(pest)
                
                return {
                    'pest_found': pest,
                    'pest_info': pest_info,
                    'solutions': solutions,
                    'recommendation': recommendation
                }
        
        # Look for practice names in the query
        all_practices = self.connector.get_all_practices()
        for practice in all_practices:
            if practice.lower() in query_text.lower():
                # Get practice details
                query = f"practice(name:{practice}, type:Type, description:Desc, cost:Cost, difficulty:Diff, controls:Controls)"
                results = self.connector.query(query)
                
                if results:
                    return {
                        'practice_found': practice,
                        'practice_info': {
                            'name': practice,
                            'type': results[0].get('Type', 'Unknown'),
                            'description': results[0].get('Desc', 'No description available'),
                            'cost': results[0].get('Cost', 'Unknown'),
                            'difficulty': results[0].get('Diff', 'Unknown'),
                            'controls': results[0].get('Controls', [])
                        }
                    }
        
        # No specific entity found
        return {
            'generic_response': True,
            'message': "I couldn't find specific information about that in my knowledge base."
        }