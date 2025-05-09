"""
Response processing utilities for Ollama output.

This module provides functions to clean, validate, and improve responses
from the Ollama LLM, ensuring consistent formatting and factuality.
"""

import re
import logging
from typing import Dict, List, Optional, Any, Tuple
import json
from django.db.models import Q

logger = logging.getLogger(__name__)

class ResponseProcessor:
    """
    Processes and improves LLM responses with various enhancement strategies.
    """
    
    def __init__(self):
        """Initialize the response processor."""
        # Common regex patterns for cleaning
        self.code_block_pattern = re.compile(r'```[a-zA-Z]*\n|```')
        self.excess_newlines_pattern = re.compile(r'\n{3,}')
        self.list_item_pattern = re.compile(r'^\s*[-*]\s+', re.MULTILINE)
        self.numbered_list_pattern = re.compile(r'^\s*\d+\.\s+', re.MULTILINE)
        
        # Citation markers
        self.citation_markers = [
            r'\[\d+\]',  # [1], [2], etc.
            r'\(\d+\)',  # (1), (2), etc.
            r'\^(\d+)',  # ^1, ^2, etc.
            r'\[citation\s+\d+\]',  # [citation 1], etc.
        ]
        self.citation_pattern = re.compile('|'.join(self.citation_markers))
        
        # Agricultural terms for validation
        self.pest_terms = [
            "aphid", "whitefly", "thrips", "mealybug", "scale", "mite", 
            "beetle", "weevil", "caterpillar", "moth", "fly", "maggot",
            "nematode", "fungus", "bacteria", "virus", "disease"
        ]
        
        self.crop_terms = [
            "maize", "corn", "wheat", "rice", "sorghum", "millet",
            "tomato", "potato", "cabbage", "lettuce", "carrot", "onion",
            "bean", "pea", "soybean", "cowpea", "groundnut", "cassava",
            "yam", "sweet potato", "banana", "plantain"
        ]
        
        self.management_terms = [
            "organic", "pesticide", "insecticide", "fungicide", "herbicide",
            "biological control", "predator", "parasite", "trap crop",
            "rotation", "intercropping", "companion planting", "mulch",
            "compost", "manure", "fertilizer", "irrigation", "drainage"
        ]
        
    def basic_clean(self, text: str) -> str:
        """
        Perform basic cleaning and formatting on the response text.
        
        Args:
            text: Raw response text from LLM
            
        Returns:
            Cleaned and formatted text
        """
        if not text or not isinstance(text, str):
            return ""
            
        # Remove code block markers but leave the content
        cleaned = self.code_block_pattern.sub('', text)
        
        # Remove excessive newlines (more than 2 in a row)
        cleaned = self.excess_newlines_pattern.sub('\n\n', cleaned)
        
        # Remove leading/trailing whitespace
        cleaned = cleaned.strip()
        
        # Remove citation markers without context
        cleaned = self.citation_pattern.sub('', cleaned)
        
        # Normalize list formatting (ensure consistent spacing)
        def normalize_list_items(match):
            return f"- {match.group(0).strip()[1:].strip()}"
            
        cleaned = self.list_item_pattern.sub(normalize_list_items, cleaned)
        
        return cleaned
        
    def structure_content(self, text: str) -> str:
        """
        Improve the structure of content with better paragraph breaks and formatting.
        
        Args:
            text: Partially cleaned text
            
        Returns:
            Better structured text
        """
        if not text:
            return ""
            
        # Ensure appropriate paragraph breaks
        paragraphs = [p.strip() for p in text.split('\n\n')]
        structured = '\n\n'.join(p for p in paragraphs if p)
        
        # Ensure lists have proper spacing and formatting
        structured = re.sub(r'([^\n])\n- ', r'\1\n\n- ', structured)
        
        # Format headings consistently (if any)
        structured = re.sub(r'(?m)^([A-Z][A-Za-z0-9 ]+):$', r'**\1**:', structured)
        
        # Add section breaks for readability
        if len(structured) > 500 and "\n\n" not in structured[:200]:
            sections = []
            current_section = []
            lines = structured.split('\n')
            
            for line in lines:
                if re.match(r'^[A-Z][A-Za-z0-9 ]+:$', line):
                    if current_section:
                        sections.append('\n'.join(current_section))
                        current_section = []
                current_section.append(line)
            
            if current_section:
                sections.append('\n'.join(current_section))
            
            structured = '\n\n'.join(sections)
        
        return structured
    
    def fact_check(self, text: str, query: str) -> Tuple[str, List[str]]:
        """
        Check for factual accuracy and detect potential misinformation.
        
        This function searches for relevant knowledge in the database to validate
        claims made in the LLM response. It flags potential inaccuracies and
        enhances the response with correct information where appropriate.
        
        Args:
            text: LLM response text
            query: The original user query
            
        Returns:
            Tuple of (enhanced_text, warnings) where warnings lists potential issues
        """
        # List to store warning messages for potentially inaccurate information
        warnings = []
        
        try:
            # Attempt to fetch relevant knowledge from the database
            from community.models import IndigenousKnowledge
            
            # Extract key terms from the query for searching
            # This is a simple approach - could be improved with NLP
            key_terms = self._extract_key_terms(query)
            
            # Skip fact checking if we couldn't extract terms
            if not key_terms:
                return text, warnings
                
            # Get relevant verified knowledge entries
            relevant_knowledge = IndigenousKnowledge.objects.filter(
                verification_status='verified'
            ).filter(
                Q(title__icontains=key_terms[0]) | 
                Q(description__icontains=key_terms[0])
            )
            
            if len(key_terms) > 1:
                # Add additional filters for other key terms
                for term in key_terms[1:]:
                    relevant_knowledge = relevant_knowledge.filter(
                        Q(title__icontains=term) | 
                        Q(description__icontains=term)
                    )
            
            # If we found relevant knowledge, check for contradictions
            if relevant_knowledge.exists():
                # Simple approach: look for contradiction markers in the text
                contradiction_markers = [
                    "not effective", "doesn't work", "ineffective", 
                    "no evidence", "myth", "false belief"
                ]
                
                for marker in contradiction_markers:
                    if marker in text.lower():
                        warnings.append(f"Potential contradiction to verified knowledge: '{marker}'")
                        
                # Try to enhance the text with citations
                enhanced_text = self._add_indigenous_citations(text, relevant_knowledge)
                return enhanced_text, warnings
            
            # Agricultural knowledge validation
            self._validate_agricultural_content(text, warnings)
                
        except Exception as e:
            logger.warning(f"Error during fact checking: {str(e)}")
            
        # Return the original text if we couldn't fact check
        return text, warnings
    
    def _validate_agricultural_content(self, text: str, warnings: List[str]) -> None:
        """
        Validate agricultural content for common mistakes or unlikely claims.
        
        Args:
            text: Response text to validate
            warnings: List to add warnings to
        """
        # Check for uncommon pest-crop associations
        text_lower = text.lower()
        
        # Unlikely combinations to flag
        unlikely_combinations = [
            ("aphid", "root"),
            ("nematode", "leaf"),
            ("whitefly", "soil"),
            ("mealybug", "root"),
        ]
        
        for pest, plant_part in unlikely_combinations:
            pattern = rf'{pest}.*{plant_part}|{plant_part}.*{pest}'
            if re.search(pattern, text_lower):
                warnings.append(f"Potential inaccuracy: association between '{pest}' and '{plant_part}'")
        
        # Check for unlikely control methods
        unlikely_controls = [
            (r'soap.*fungal', "Soap is not typically effective for fungal diseases"),
            (r'neem.*soil pest', "Neem oil is less effective for soil pests"),
            (r'rotat.*virus', "Crop rotation has limited effect on viral diseases"),
        ]
        
        for pattern, warning_msg in unlikely_controls:
            if re.search(pattern, text_lower):
                warnings.append(f"Potential inaccuracy: {warning_msg}")
    
    def _extract_key_terms(self, query: str) -> List[str]:
        """
        Extract key terms from the query for knowledge retrieval.
        
        Args:
            query: User query text
            
        Returns:
            List of key terms
        """
        # Remove common stop words and split into words
        stop_words = {'what', 'how', 'when', 'where', 'why', 'is', 'are', 'the', 
                     'a', 'an', 'to', 'of', 'for', 'in', 'on', 'with', 'about'}
        
        words = query.lower().split()
        filtered_words = [w for w in words if w not in stop_words and len(w) > 2]
        
        # Check for pest terms in query
        pest_terms = [w for w in filtered_words if w in self.pest_terms]
        if pest_terms:
            filtered_words = pest_terms + [w for w in filtered_words if w not in pest_terms]
            
        # Check for crop terms in query
        crop_terms = [w for w in filtered_words if w in self.crop_terms]
        if crop_terms:
            filtered_words = crop_terms + [w for w in filtered_words if w not in crop_terms]
        
        # Return up to 3 most significant terms (could be improved with TF-IDF)
        return filtered_words[:3]
    
    def _add_indigenous_citations(self, text: str, knowledge_entries) -> str:
        """
        Add citations to indigenous knowledge sources.
        
        Args:
            text: Response text
            knowledge_entries: QuerySet of knowledge entries
            
        Returns:
            Text with added citations
        """
        if not knowledge_entries:
            return text
            
        # Append a "Sources" section with references
        entries_text = "\n\nSources from Indigenous Knowledge:\n"
        
        for i, entry in enumerate(knowledge_entries[:3], 1):  # Limit to top 3
            entries_text += f"{i}. {entry.title} - Shared by {entry.keeper.full_name} "
            entries_text += f"from {entry.keeper.village}, {entry.keeper.district}\n"
            
        return text + entries_text
    
    def process_response(self, response_text: str, query: str) -> str:
        """
        Apply all processing steps to improve a response.
        
        Args:
            response_text: Raw response from LLM
            query: Original user query
            
        Returns:
            Processed and improved response
        """
        if not response_text:
            return ""
            
        # Apply basic cleaning
        cleaned = self.basic_clean(response_text)
        
        # Improve structure
        structured = self.structure_content(cleaned)
        
        # Fact check and enhance with citations
        enhanced, warnings = self.fact_check(structured, query)
        
        # Log any warnings
        for warning in warnings:
            logger.warning(warning)
            
        return enhanced
    
    def enhance_agricultural_content(self, text: str, query: str) -> str:
        """
        Add agricultural best practices context to responses where appropriate.
        
        Args:
            text: Processed response
            query: Original query
            
        Returns:
            Enhanced response with added context
        """
        # Skip enhancement if response is already long
        if len(text) > 500:
            return text
            
        # Determine query category
        query_lower = query.lower()
        
        # Pest management context
        if any(term in query_lower for term in ["pest", "insect", "control", "damage"]):
            if "organic" in query_lower or "natural" in query_lower:
                return text + "\n\nRemember: Integrated Pest Management (IPM) combines multiple strategies for sustainable pest control, including cultural practices, biological control, and targeted interventions only when necessary."
            
        # Soil health context
        if any(term in query_lower for term in ["soil", "fertility", "nutrient"]):
            return text + "\n\nNote: Healthy soil is the foundation of sustainable agriculture. Regular soil testing, organic matter incorporation, and appropriate pH management are key practices for long-term soil health."
            
        # Crop management context
        if any(term in query_lower for term in ["grow", "plant", "crop", "cultivate"]):
            return text + "\n\nTip: Consider local climate conditions, traditional farming knowledge, and sustainable practices when planning your cultivation approach."
            
        return text

# Single instance for repeated use
response_processor = ResponseProcessor()

def process_response(response_text: str, query: str) -> str:
    """
    Process and improve an LLM response.
    
    Args:
        response_text: Raw response from LLM
        query: Original user query
        
    Returns:
        Processed and improved response
    """
    processed = response_processor.process_response(response_text, query)
    enhanced = response_processor.enhance_agricultural_content(processed, query)
    return enhanced 