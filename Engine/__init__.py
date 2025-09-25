"""
AI-Powered Internship Recommendation Engine

This module provides intelligent internship recommendations using:
- Ollama Llama3.2-vision for document/certificate analysis  
- 20-parameter scoring algorithm for personalized matching
- Real-time recommendation generation and caching
"""

__version__ = "1.0.0"
__author__ = "AI Engine Team"

from .ai_processing.vision_processor import VisionProcessor
from .recommendation.engine import RecommendationEngine
from .data_extraction.extractor import DataExtractor

__all__ = [
    'VisionProcessor',
    'RecommendationEngine', 
    'DataExtractor'
]