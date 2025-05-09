from ..prolog.connector import PrologConnector

class PrologService:
    def __init__(self):
        self.connector = PrologConnector()
    
    def get_pest_solutions(self, pest, region):
        """Get solutions for a pest in a specific region"""
        solutions = self.connector.get_pest_solutions(pest, region)
        return self._format_solutions(solutions)
    
    def recommend_solution(self, pest):
        """Get the recommended solution for a pest"""
        solution = self.connector.recommend_solution(pest)
        if solution:
            # Get more details about the solution
            details = self._get_practice_details(solution)
            return {
                'name': solution,
                'details': details
            }
        return None
    
    def _format_solutions(self, solutions):
        """Format the solutions with additional details"""
        formatted = []
        for solution in solutions:
            details = self._get_practice_details(solution)
            formatted.append({
                'name': solution,
                'details': details
            })
        return formatted
    
    def _get_practice_details(self, practice):
        """Get details for a specific practice"""
        query = f"practice(name:{practice}, type:Type, description:Desc, cost:Cost, difficulty:Diff)"
        results = self.connector.query(query)
        if results:
            return results[0]
        return {}
    
    def get_all_pests(self):
        """Get a list of all pests in the knowledge base"""
        query = "pest(name:Name, _)"
        results = self.connector.query(query)
        return [result['Name'] for result in results]
    
    def get_all_crops(self):
        """Get a list of all crops in the knowledge base"""
        query = "crop(name:Name, _)"
        results = self.connector.query(query)
        return [result['Name'] for result in results]