"""
Utility functions for the recommendation engine
"""

import hashlib
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class CacheManager:
    """
    Manages caching for expensive recommendation operations
    """
    
    def __init__(self, cache_dir: str = "cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        
    def get_cache_key(self, user_id: str, internships_hash: str) -> str:
        """Generate cache key for recommendations"""
        data = f"{user_id}_{internships_hash}"
        return hashlib.md5(data.encode()).hexdigest()
    
    def get_cached_recommendations(self, cache_key: str, max_age_hours: int = 24) -> Optional[List[int]]:
        """Get cached recommendations if still valid"""
        try:
            cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
            
            if not os.path.exists(cache_file):
                return None
                
            with open(cache_file, 'r') as f:
                cached_data = json.load(f)
                
            # Check if cache is still valid
            cached_time = datetime.fromisoformat(cached_data['timestamp'])
            if datetime.now() - cached_time > timedelta(hours=max_age_hours):
                return None
                
            return cached_data['recommendations']
            
        except Exception as e:
            logger.error(f"Cache retrieval failed: {e}")
            return None
    
    def cache_recommendations(self, cache_key: str, recommendations: List[int]):
        """Cache recommendations"""
        try:
            cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
            
            cache_data = {
                'timestamp': datetime.now().isoformat(),
                'recommendations': recommendations
            }
            
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f)
                
        except Exception as e:
            logger.error(f"Cache storage failed: {e}")

class ConfigManager:
    """
    Manages configuration for the recommendation engine
    """
    
    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """Get default configuration"""
        return {
            'ollama': {
                'url': 'http://localhost:11434',
                'model': 'llama3.2-vision:latest',
                'timeout': 60
            },
            'recommendation': {
                'top_k': 6,
                'cache_duration_hours': 24,
                'min_score_threshold': 0.1
            },
            'scoring_weights': {
                "skill_coverage": 0.15,
                "skill_jaccard": 0.12,
                "top_k_skills": 0.10,
                "sector_similarity": 0.08,
                "education_gap": 0.07,
                "geo_distance": 0.06,
                "remote_suitability": 0.05,
                "freshness": 0.05,
                "decayed_ctr": 0.04,
                "decayed_apply_rate": 0.04,
                "selection_ratio": 0.04,
                "title_similarity": 0.03,
                "description_alignment": 0.03,
                "sector_affinity": 0.03,
                "location_affinity": 0.03,
                "novelty_desire": 0.02,
                "fatigue_score": 0.02,
                "barrier_score": 0.02,
                "inclusivity_flag": 0.02,
                "diversity_rotation": 0.01
            }
        }

class ValidationUtils:
    """
    Utility functions for data validation
    """
    
    @staticmethod
    def validate_user_data(user_data: Dict) -> bool:
        """Validate user data structure"""
        required_fields = ['user_id', 'username']
        return all(field in user_data for field in required_fields)
    
    @staticmethod
    def validate_internship_data(internship_data: Dict) -> bool:
        """Validate internship data structure"""
        required_fields = ['internship_id', 'title', 'company_name']
        return all(field in internship_data for field in required_fields)
    
    @staticmethod
    def sanitize_skills_list(skills: str) -> List[str]:
        """Clean and normalize skills list"""
        if not skills:
            return []
            
        # Split by comma, clean whitespace, convert to lowercase
        cleaned_skills = []
        for skill in skills.split(','):
            skill = skill.strip().lower()
            if skill and len(skill) > 1:  # Ignore single characters
                cleaned_skills.append(skill)
                
        return cleaned_skills

class MetricsCollector:
    """
    Collects metrics for recommendation performance
    """
    
    def __init__(self):
        self.metrics = {
            'recommendations_generated': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'vision_extractions': 0,
            'extraction_failures': 0,
            'avg_recommendation_time': 0.0
        }
    
    def record_recommendation_generated(self, processing_time: float):
        """Record a recommendation generation event"""
        self.metrics['recommendations_generated'] += 1
        
        # Update average processing time
        current_avg = self.metrics['avg_recommendation_time']
        count = self.metrics['recommendations_generated']
        self.metrics['avg_recommendation_time'] = (current_avg * (count - 1) + processing_time) / count
    
    def record_cache_hit(self):
        """Record a cache hit"""
        self.metrics['cache_hits'] += 1
    
    def record_cache_miss(self):
        """Record a cache miss"""
        self.metrics['cache_misses'] += 1
    
    def record_vision_extraction(self, success: bool):
        """Record a vision extraction attempt"""
        if success:
            self.metrics['vision_extractions'] += 1
        else:
            self.metrics['extraction_failures'] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        total_cache_requests = self.metrics['cache_hits'] + self.metrics['cache_misses']
        cache_hit_rate = (
            self.metrics['cache_hits'] / total_cache_requests 
            if total_cache_requests > 0 else 0.0
        )
        
        total_extractions = self.metrics['vision_extractions'] + self.metrics['extraction_failures']
        extraction_success_rate = (
            self.metrics['vision_extractions'] / total_extractions
            if total_extractions > 0 else 0.0
        )
        
        return {
            **self.metrics,
            'cache_hit_rate': cache_hit_rate,
            'extraction_success_rate': extraction_success_rate
        }

class DatabaseUtils:
    """
    Database utility functions
    """
    
    @staticmethod
    def hash_internships_for_cache(internships: List[Dict]) -> str:
        """Create hash of internships for cache key generation"""
        # Create a simple hash based on internship IDs and last modified dates
        internship_signatures = []
        for internship in internships:
            signature = f"{internship.get('internship_id', '')}_{internship.get('posted_date', '')}"
            internship_signatures.append(signature)
        
        combined_signature = "_".join(sorted(internship_signatures))
        return hashlib.md5(combined_signature.encode()).hexdigest()
    
    @staticmethod
    def format_recommendation_list_for_db(recommendations: List[int]) -> str:
        """Format recommendation list for database storage"""
        return json.dumps(recommendations)
    
    @staticmethod
    def parse_recommendation_list_from_db(db_value: str) -> List[int]:
        """Parse recommendation list from database"""
        try:
            if not db_value:
                return []
            return json.loads(db_value)
        except:
            return []