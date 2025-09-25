"""
Main Engine Orchestrator - Coordinates all recommendation engine components
"""

import time
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

from ai_processing.vision_processor import VisionProcessor
from recommendation.engine import RecommendationEngine
from data_extraction.extractor import DataExtractor
from utils.helpers import CacheManager, ConfigManager, MetricsCollector, DatabaseUtils

logger = logging.getLogger(__name__)

class RecommendationOrchestrator:
    """
    Main orchestrator that coordinates the entire recommendation pipeline
    """
    
    def __init__(self, config: Optional[Dict] = None):
        # Load configuration
        self.config = config or ConfigManager.get_default_config()
        
        # Initialize components
        self.vision_processor = VisionProcessor(self.config['ollama']['url'])
        self.recommendation_engine = RecommendationEngine()
        self.data_extractor = DataExtractor()
        self.cache_manager = CacheManager()
        self.metrics = MetricsCollector()
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        logger.info("Recommendation Engine initialized")
    
    def generate_user_recommendations(self, user_data: Dict, internships: List[Dict], 
                                    force_refresh: bool = False) -> Dict[str, Any]:
        """
        Generate personalized recommendations for a user
        
        Args:
            user_data: Complete user profile data from database
            internships: List of available internships
            force_refresh: Whether to bypass cache and regenerate
            
        Returns:
            Dictionary containing recommendations and metadata
        """
        start_time = time.time()
        
        try:
            user_id = user_data.get('user_id', '')
            
            # Check cache first (unless force refresh)
            if not force_refresh:
                cached_recommendations = self._get_cached_recommendations(user_id, internships)
                if cached_recommendations:
                    self.metrics.record_cache_hit()
                    return {
                        'recommendations': cached_recommendations,
                        'source': 'cache',
                        'processing_time': time.time() - start_time
                    }
            
            self.metrics.record_cache_miss()
            
            # Step 1: Process vision data if certificates uploaded
            enhanced_user_data = self._process_user_vision_data(user_data)
            
            # Step 2: Normalize and enrich all data
            normalized_user = self.data_extractor.normalize_user_data(enhanced_user_data)
            normalized_internships = [
                self.data_extractor.normalize_internship_data(internship)
                for internship in internships
            ]
            
            # Step 3: Generate recommendations using the engine
            recommendation_ids = self.recommendation_engine.generate_recommendations(
                normalized_user,
                normalized_internships,
                self.config['recommendation']['top_k']
            )
            
            # Step 4: Cache the results
            self._cache_recommendations(user_id, internships, recommendation_ids)
            
            # Step 5: Record metrics
            processing_time = time.time() - start_time
            self.metrics.record_recommendation_generated(processing_time)
            
            logger.info(f"Generated {len(recommendation_ids)} recommendations for user {user_id} in {processing_time:.2f}s")
            
            return {
                'recommendations': recommendation_ids,
                'source': 'generated',
                'processing_time': processing_time,
                'user_profile_completion': self._calculate_profile_completeness(normalized_user),
                'recommendation_confidence': self._calculate_confidence_score(normalized_user, recommendation_ids)
            }
            
        except Exception as e:
            logger.error(f"Recommendation generation failed for user {user_data.get('user_id', 'unknown')}: {e}")
            return {
                'recommendations': [],
                'source': 'error',
                'error': str(e),
                'processing_time': time.time() - start_time
            }
    
    def process_uploaded_documents(self, user_id: str, file_paths: List[str]) -> Dict[str, Any]:
        """
        Process uploaded documents using vision AI
        
        Args:
            user_id: User identifier
            file_paths: List of uploaded document paths
            
        Returns:
            Extracted data from documents
        """
        try:
            logger.info(f"Processing {len(file_paths)} documents for user {user_id}")
            
            # Check if Ollama is available
            if not self.vision_processor.health_check():
                logger.warning("Ollama service not available, skipping vision processing")
                self.metrics.record_vision_extraction(False)
                return {
                    'success': False,
                    'error': 'Vision processing service unavailable',
                    'extracted_data': {}
                }
            
            # Process documents
            if len(file_paths) == 1:
                # Single document processing
                result = self.vision_processor.extract_from_document(file_paths[0])
            else:
                # Multiple documents processing
                result = self.vision_processor.process_multiple_documents(file_paths)
            
            # Record metrics
            success = result.get('success', False) if len(file_paths) == 1 else True
            self.metrics.record_vision_extraction(success)
            
            logger.info(f"Document processing completed for user {user_id}")
            return result
            
        except Exception as e:
            logger.error(f"Document processing failed for user {user_id}: {e}")
            self.metrics.record_vision_extraction(False)
            return {
                'success': False,
                'error': str(e),
                'extracted_data': {}
            }
    
    def get_recommendation_explanations(self, user_data: Dict, internship_ids: List[int], 
                                     internships: List[Dict]) -> List[Dict[str, Any]]:
        """
        Get explanations for why specific internships were recommended
        
        Args:
            user_data: User profile data
            internship_ids: List of recommended internship IDs
            internships: All internship data
            
        Returns:
            List of explanations for each recommendation
        """
        try:
            explanations = []
            
            # Create lookup for internships
            internship_lookup = {int_data['internship_id']: int_data for int_data in internships}
            
            # Normalize user data
            normalized_user = self.data_extractor.normalize_user_data(user_data)
            
            for internship_id in internship_ids:
                internship = internship_lookup.get(internship_id)
                if not internship:
                    continue
                    
                normalized_internship = self.data_extractor.normalize_internship_data(internship)
                
                # Generate explanation
                explanation = self._generate_recommendation_explanation(
                    normalized_user, normalized_internship
                )
                
                explanations.append({
                    'internship_id': internship_id,
                    'explanation': explanation,
                    'match_score': self.recommendation_engine._calculate_overall_score(
                        normalized_user, normalized_internship
                    )
                })
            
            return explanations
            
        except Exception as e:
            logger.error(f"Explanation generation failed: {e}")
            return []
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get system health and metrics"""
        return {
            'ollama_available': self.vision_processor.health_check(),
            'metrics': self.metrics.get_metrics(),
            'config': self.config,
            'status': 'healthy'
        }
    
    def _get_cached_recommendations(self, user_id: str, internships: List[Dict]) -> Optional[List[int]]:
        """Get cached recommendations if available"""
        try:
            internships_hash = DatabaseUtils.hash_internships_for_cache(internships)
            cache_key = self.cache_manager.get_cache_key(user_id, internships_hash)
            
            return self.cache_manager.get_cached_recommendations(
                cache_key, 
                self.config['recommendation']['cache_duration_hours']
            )
            
        except Exception as e:
            logger.error(f"Cache retrieval failed: {e}")
            return None
    
    def _cache_recommendations(self, user_id: str, internships: List[Dict], recommendations: List[int]):
        """Cache recommendations"""
        try:
            internships_hash = DatabaseUtils.hash_internships_for_cache(internships)
            cache_key = self.cache_manager.get_cache_key(user_id, internships_hash)
            
            self.cache_manager.cache_recommendations(cache_key, recommendations)
            
        except Exception as e:
            logger.error(f"Caching failed: {e}")
    
    def _process_user_vision_data(self, user_data: Dict) -> Dict[str, Any]:
        """Process and enhance user data with vision extracted information"""
        try:
            # Check if user has uploaded files that need processing
            vision_data = user_data.get('vision_extracted_data')
            
            if vision_data:
                # Data already processed, return as-is
                return user_data
            
            # If no vision data but has uploaded files, we could process them here
            # For now, return original data
            return user_data
            
        except Exception as e:
            logger.error(f"Vision data processing failed: {e}")
            return user_data
    
    def _calculate_profile_completeness(self, user_data: Dict) -> float:
        """Calculate how complete the user's profile is"""
        try:
            important_fields = [
                'technical_skills', 'education_level', 'degree', 'city', 'state',
                'preferred_industry', 'internship_type_preference', 'projects'
            ]
            
            filled_fields = sum(1 for field in important_fields if user_data.get(field))
            return filled_fields / len(important_fields)
            
        except:
            return 0.5
    
    def _calculate_confidence_score(self, user_data: Dict, recommendations: List[int]) -> float:
        """Calculate confidence in the recommendations"""
        try:
            # Factors that increase confidence
            confidence_factors = []
            
            # Profile completeness
            completeness = self._calculate_profile_completeness(user_data)
            confidence_factors.append(completeness)
            
            # Presence of vision extracted data
            if user_data.get('vision_data', {}).get('extracted_skills'):
                confidence_factors.append(0.8)
            else:
                confidence_factors.append(0.3)
            
            # Number of recommendations generated
            if len(recommendations) >= self.config['recommendation']['top_k']:
                confidence_factors.append(0.9)
            elif len(recommendations) > 0:
                confidence_factors.append(0.6)
            else:
                confidence_factors.append(0.1)
            
            return sum(confidence_factors) / len(confidence_factors)
            
        except:
            return 0.5
    
    def _generate_recommendation_explanation(self, user_data: Dict, internship_data: Dict) -> str:
        """Generate human-readable explanation for a recommendation"""
        try:
            explanations = []
            
            # Skill match explanation
            user_skills = set(user_data.get('all_skills', []))
            required_skills = self.data_extractor._extract_skills_from_text(
                internship_data.get('required_skills', '')
            )
            
            if user_skills and required_skills:
                # Find matching skills from any category
                all_required = set()
                for category_skills in required_skills.values():
                    all_required.update(category_skills)
                
                matches = user_skills.intersection(all_required)
                if matches:
                    explanations.append(f"Your skills match: {', '.join(list(matches)[:3])}")
            
            # Location match
            user_location = f"{user_data.get('city', '')} {user_data.get('state', '')}".strip()
            internship_location = f"{internship_data.get('city', '')} {internship_data.get('state', '')}".strip()
            
            if user_location and internship_location:
                if user_location.lower() in internship_location.lower():
                    explanations.append("Located in your preferred area")
                elif internship_data.get('remote_allowed'):
                    explanations.append("Offers remote work flexibility")
            
            # Industry match
            user_industry = user_data.get('preferred_industry', '').lower()
            internship_industry = internship_data.get('industry', '').lower()
            
            if user_industry and internship_industry and user_industry == internship_industry:
                explanations.append(f"Matches your {internship_industry} industry preference")
            
            # Experience level match
            experience_level = user_data.get('experience_level', '')
            if experience_level:
                explanations.append(f"Suitable for {experience_level} level")
            
            return "; ".join(explanations) if explanations else "Good overall match for your profile"
            
        except Exception as e:
            logger.error(f"Explanation generation failed: {e}")
            return "Recommended based on your profile"