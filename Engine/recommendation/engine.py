"""
Advanced Recommendation Engine with 20-parameter scoring system
"""

import json
import math
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any, Optional
from geopy.distance import geodesic
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

logger = logging.getLogger(__name__)

class RecommendationEngine:
    """
    20-parameter internship recommendation engine
    """
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        self.parameter_weights = self._initialize_weights()
        
    def _initialize_weights(self) -> Dict[str, float]:
        """Initialize parameter weights for scoring"""
        return {
            "skill_coverage": 0.15,          # Critical match factor
            "skill_jaccard": 0.12,           # Overall skill similarity  
            "top_k_skills": 0.10,            # Key skills match
            "sector_similarity": 0.08,       # Industry alignment
            "education_gap": 0.07,           # Education requirements
            "geo_distance": 0.06,            # Location factor
            "remote_suitability": 0.05,      # Remote work match
            "freshness": 0.05,               # Posting recency
            "decayed_ctr": 0.04,             # Click performance
            "decayed_apply_rate": 0.04,      # Apply performance
            "selection_ratio": 0.04,         # Quality proxy
            "title_similarity": 0.03,        # Job title match
            "description_alignment": 0.03,   # Description match
            "sector_affinity": 0.03,         # User preferences
            "location_affinity": 0.03,       # Location preferences
            "novelty_desire": 0.02,          # Diversity factor
            "fatigue_score": 0.02,           # Overexposure penalty
            "barrier_score": 0.02,           # Accessibility
            "inclusivity_flag": 0.02,        # Diversity boost
            "diversity_rotation": 0.01       # Deduplication
        }
    
    def generate_recommendations(self, user_data: Dict, internships: List[Dict], 
                               top_k: int = 6) -> List[int]:
        """
        Generate top-k internship recommendations for a user
        
        Args:
            user_data: Complete user profile data
            internships: List of available internships
            top_k: Number of recommendations to return
            
        Returns:
            List of internship IDs ordered by recommendation score
        """
        try:
            scores = []
            
            for internship in internships:
                score = self._calculate_overall_score(user_data, internship)
                scores.append((internship['internship_id'], score))
            
            # Sort by score (descending) and return top-k IDs
            scores.sort(key=lambda x: x[1], reverse=True)
            
            # Apply diversity rotation to avoid same company/sector dominance
            diversified_scores = self._apply_diversity_rotation(scores, internships)
            
            return [internship_id for internship_id, _ in diversified_scores[:top_k]]
            
        except Exception as e:
            logger.error(f"Recommendation generation failed: {e}")
            return []
    
    def _calculate_overall_score(self, user: Dict, internship: Dict) -> float:
        """Calculate weighted score using all 20 parameters"""
        
        scores = {}
        
        # 1. Skill Coverage of Requirements
        scores['skill_coverage'] = self._skill_coverage_score(user, internship)
        
        # 2. Skill Overlap (Jaccard)
        scores['skill_jaccard'] = self._jaccard_similarity_score(user, internship)
        
        # 3. Top-K Key Skill Hit
        scores['top_k_skills'] = self._top_k_skill_hit(user, internship)
        
        # 4. Sector Similarity
        scores['sector_similarity'] = self._sector_similarity_score(user, internship)
        
        # 5. Education Gap
        scores['education_gap'] = self._education_gap_score(user, internship)
        
        # 6. Geo Distance
        scores['geo_distance'] = self._geo_distance_score(user, internship)
        
        # 7. Remote Suitability
        scores['remote_suitability'] = self._remote_suitability_score(user, internship)
        
        # 8. Freshness Score
        scores['freshness'] = self._freshness_score(internship)
        
        # 9. Decayed CTR
        scores['decayed_ctr'] = self._decayed_ctr_score(internship)
        
        # 10. Decayed Apply Rate
        scores['decayed_apply_rate'] = self._decayed_apply_rate_score(internship)
        
        # 11. Selection/Completion Ratio
        scores['selection_ratio'] = self._selection_ratio_score(internship)
        
        # 12. Title-Profile Similarity
        scores['title_similarity'] = self._title_similarity_score(user, internship)
        
        # 13. Description-Skill Alignment
        scores['description_alignment'] = self._description_alignment_score(user, internship)
        
        # 14. Sector Affinity (User)
        scores['sector_affinity'] = self._sector_affinity_score(user, internship)
        
        # 15. Location Affinity (User)
        scores['location_affinity'] = self._location_affinity_score(user, internship)
        
        # 16. Novelty Desire
        scores['novelty_desire'] = self._novelty_desire_score(user, internship)
        
        # 17. Fatigue/Overexposure Score
        scores['fatigue_score'] = self._fatigue_score(user, internship)
        
        # 18. Barrier Score
        scores['barrier_score'] = self._barrier_score(user, internship)
        
        # 19. Inclusivity Flag
        scores['inclusivity_flag'] = self._inclusivity_score(user, internship)
        
        # 20. Diversity Rotation Count
        scores['diversity_rotation'] = 1.0  # Applied later in diversification
        
        # Calculate weighted sum
        total_score = sum(
            scores[param] * self.parameter_weights[param] 
            for param in scores
        )
        
        return total_score
    
    def _skill_coverage_score(self, user: Dict, internship: Dict) -> float:
        """Parameter 1: |S∩R| / |R|"""
        try:
            user_skills = self._extract_user_skills(user)
            required_skills = self._extract_required_skills(internship)
            
            if not required_skills:
                return 1.0  # No requirements = perfect match
                
            intersection = len(user_skills.intersection(required_skills))
            return intersection / len(required_skills)
        except:
            return 0.0
    
    def _jaccard_similarity_score(self, user: Dict, internship: Dict) -> float:
        """Parameter 2: |S∩R| / |S∪R|"""
        try:
            user_skills = self._extract_user_skills(user)
            required_skills = self._extract_required_skills(internship)
            
            intersection = len(user_skills.intersection(required_skills))
            union = len(user_skills.union(required_skills))
            
            return intersection / union if union > 0 else 0.0
        except:
            return 0.0
    
    def _top_k_skill_hit(self, user: Dict, internship: Dict, k: int = 3) -> float:
        """Parameter 3: Binary match for top-k important skills"""
        try:
            user_skills = self._extract_user_skills(user)
            
            # Get top-k most important skills from internship
            required_skills = self._extract_required_skills(internship)
            top_skills = list(required_skills)[:k]  # Assume first k are most important
            
            # Check if any top skills match
            return 1.0 if any(skill in user_skills for skill in top_skills) else 0.0
        except:
            return 0.0
    
    def _sector_similarity_score(self, user: Dict, internship: Dict) -> float:
        """Parameter 4: Sector/industry alignment"""
        try:
            user_interests = user.get('preferred_industry', '').lower()
            internship_sector = internship.get('industry', '').lower()
            
            if not user_interests or not internship_sector:
                return 0.5  # Neutral score
                
            # Simple string similarity - can be enhanced with taxonomy
            return 1.0 if user_interests == internship_sector else 0.0
        except:
            return 0.5
    
    def _education_gap_score(self, user: Dict, internship: Dict) -> float:
        """Parameter 5: Education level alignment"""
        try:
            education_levels = {
                'high school': 1, 'diploma': 2, 'undergraduate': 3, 
                'bachelor': 3, 'graduate': 4, 'master': 4, 'phd': 5
            }
            
            user_edu = user.get('education_level', '').lower()
            required_edu = internship.get('education_requirement', '').lower()
            
            user_level = education_levels.get(user_edu, 3)
            required_level = education_levels.get(required_edu, 3)
            
            # Score based on education gap (prefer slight overqualification)
            gap = user_level - required_level
            if gap >= 0:
                return max(0.0, 1.0 - (gap * 0.1))  # Small penalty for overqualification
            else:
                return max(0.0, 1.0 + (gap * 0.2))  # Larger penalty for underqualification
                
        except:
            return 0.5
    
    def _geo_distance_score(self, user: Dict, internship: Dict) -> float:
        """Parameter 6: Geographic distance penalty"""
        try:
            user_location = (user.get('latitude', 0), user.get('longitude', 0))
            internship_location = (
                internship.get('latitude', 0), 
                internship.get('longitude', 0)
            )
            
            if not all([user_location[0], user_location[1], internship_location[0], internship_location[1]]):
                return 0.5  # Neutral if location data missing
                
            distance_km = geodesic(user_location, internship_location).kilometers
            
            # Score decay with distance (max reasonable commute ~50km)
            return max(0.0, 1.0 - (distance_km / 100.0))
            
        except:
            return 0.5
    
    def _remote_suitability_score(self, user: Dict, internship: Dict) -> float:
        """Parameter 7: Remote work alignment"""
        try:
            user_remote_ok = user.get('remote_work_preference', False)
            internship_remote = internship.get('remote_allowed', False)
            
            if internship_remote and user_remote_ok:
                return 1.0
            elif internship_remote and not user_remote_ok:
                return 0.8  # Remote available but user prefers office
            elif not internship_remote and user_remote_ok:
                return 0.3  # User wants remote but not available
            else:
                return 0.7  # Both prefer office
                
        except:
            return 0.5
    
    def _freshness_score(self, internship: Dict) -> float:
        """Parameter 8: Posting recency score"""
        try:
            posted_date = datetime.fromisoformat(internship.get('posted_date', datetime.now().isoformat()))
            days_old = (datetime.now() - posted_date).days
            
            # Exponential decay (half-life of 7 days)
            return math.exp(-days_old / 10.0)
            
        except:
            return 0.5
    
    def _decayed_ctr_score(self, internship: Dict) -> float:
        """Parameter 9: Time-decayed click-through rate"""
        try:
            raw_ctr = internship.get('click_through_rate', 0.05)
            days_since_posted = (datetime.now() - datetime.fromisoformat(
                internship.get('posted_date', datetime.now().isoformat())
            )).days
            
            # Smooth and decay CTR
            smoothed_ctr = (raw_ctr + 0.01) / 1.01  # Laplace smoothing
            decayed_ctr = smoothed_ctr * math.exp(-days_since_posted / 30.0)
            
            return min(1.0, decayed_ctr * 10)  # Scale to 0-1
            
        except:
            return 0.1
    
    def _decayed_apply_rate_score(self, internship: Dict) -> float:
        """Parameter 10: Time-decayed apply rate"""
        try:
            raw_apply_rate = internship.get('apply_rate', 0.02)
            days_since_posted = (datetime.now() - datetime.fromisoformat(
                internship.get('posted_date', datetime.now().isoformat())
            )).days
            
            smoothed_rate = (raw_apply_rate + 0.005) / 1.005
            decayed_rate = smoothed_rate * math.exp(-days_since_posted / 30.0)
            
            return min(1.0, decayed_rate * 20)
            
        except:
            return 0.1
    
    def _selection_ratio_score(self, internship: Dict) -> float:
        """Parameter 11: Selection/completion quality proxy"""
        try:
            applications = internship.get('total_applications', 1)
            selections = internship.get('total_selections', 0)
            
            # Smoothed ratio
            ratio = (selections + 1) / (applications + 10)
            return min(1.0, ratio * 5)  # Scale appropriately
            
        except:
            return 0.2
    
    def _title_similarity_score(self, user: Dict, internship: Dict) -> float:
        """Parameter 12: Job title vs user profile similarity"""
        try:
            user_profile = f"{user.get('degree', '')} {user.get('technical_skills', '')} {user.get('preferred_role', '')}"
            job_title = internship.get('title', '')
            
            if not user_profile.strip() or not job_title.strip():
                return 0.5
                
            # Use TF-IDF cosine similarity
            documents = [user_profile.lower(), job_title.lower()]
            tfidf_matrix = self.vectorizer.fit_transform(documents)
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return similarity
            
        except:
            return 0.5
    
    def _description_alignment_score(self, user: Dict, internship: Dict) -> float:
        """Parameter 13: Skills vs job description alignment"""
        try:
            user_skills = " ".join(self._extract_user_skills(user))
            job_description = internship.get('description', '')
            
            if not user_skills or not job_description:
                return 0.5
                
            documents = [user_skills.lower(), job_description.lower()]
            tfidf_matrix = self.vectorizer.fit_transform(documents)
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return similarity
            
        except:
            return 0.5
    
    def _sector_affinity_score(self, user: Dict, internship: Dict) -> float:
        """Parameter 14: User's historical sector interest"""
        try:
            # This would use user's historical interaction data
            # For now, use preference matching
            user_interests = user.get('preferred_industry', '').lower().split(',')
            internship_sector = internship.get('industry', '').lower()
            
            return 1.0 if internship_sector in user_interests else 0.3
            
        except:
            return 0.5
    
    def _location_affinity_score(self, user: Dict, internship: Dict) -> float:
        """Parameter 15: User's location preferences"""
        try:
            user_preferred_locations = user.get('preferred_locations', '').lower().split(',')
            internship_location = f"{internship.get('city', '')} {internship.get('state', '')}".lower()
            
            return 1.0 if any(loc.strip() in internship_location for loc in user_preferred_locations) else 0.3
            
        except:
            return 0.5
    
    def _novelty_desire_score(self, user: Dict, internship: Dict) -> float:
        """Parameter 16: Diversity from recent interactions"""
        try:
            # This would compare with user's recent clicks/applications
            # For now, return neutral score
            return 0.7  # Slight preference for novelty
            
        except:
            return 0.5
    
    def _fatigue_score(self, user: Dict, internship: Dict) -> float:
        """Parameter 17: Overexposure penalty"""
        try:
            # This would track how often company/sector was shown to user
            # For now, return neutral score
            return 0.8  # Slight penalty assumption
            
        except:
            return 1.0
    
    def _barrier_score(self, user: Dict, internship: Dict) -> float:
        """Parameter 18: Accessibility barriers"""
        try:
            barriers = 0
            
            # Check various barriers
            if internship.get('requires_fee', False):
                barriers += 0.3
            if internship.get('strict_hours', False) and user.get('flexible_hours_needed', False):
                barriers += 0.2
            if internship.get('requires_relocation', False) and not user.get('willing_to_relocate', True):
                barriers += 0.4
                
            return max(0.0, 1.0 - barriers)
            
        except:
            return 0.8
    
    def _inclusivity_score(self, user: Dict, internship: Dict) -> float:
        """Parameter 19: Diversity and inclusion boost"""
        try:
            boost = 0.0
            
            # Various inclusivity factors
            if internship.get('pwd_friendly', False) and user.get('requires_accessibility', False):
                boost += 0.5
            if internship.get('women_encouraged', False) and user.get('gender', '').lower() == 'female':
                boost += 0.3
            if internship.get('local_quota', False) and user.get('is_local', False):
                boost += 0.2
                
            return min(1.0, 0.5 + boost)  # Base + boost
            
        except:
            return 0.5
    
    def _apply_diversity_rotation(self, scores: List[Tuple[int, float]], 
                                internships: List[Dict]) -> List[Tuple[int, float]]:
        """Parameter 20: Ensure diversity in recommendations"""
        try:
            seen_companies = set()
            seen_sectors = set()
            diversified = []
            
            # Create lookup for internship details
            internship_lookup = {int['internship_id']: int for int in internships}
            
            for internship_id, score in scores:
                internship = internship_lookup.get(internship_id, {})
                company = internship.get('company_name', '')
                sector = internship.get('industry', '')
                
                # Apply diversity penalty
                penalty = 0.0
                if company in seen_companies:
                    penalty += 0.1
                if sector in seen_sectors:
                    penalty += 0.05
                    
                adjusted_score = score * (1.0 - penalty)
                diversified.append((internship_id, adjusted_score))
                
                seen_companies.add(company)
                seen_sectors.add(sector)
            
            # Re-sort by adjusted scores
            diversified.sort(key=lambda x: x[1], reverse=True)
            return diversified
            
        except:
            return scores  # Return original if diversity rotation fails
    
    def _extract_user_skills(self, user: Dict) -> set:
        """Extract and normalize user skills"""
        try:
            skills = set()
            
            # Technical skills from form
            tech_skills = user.get('technical_skills', '')
            if tech_skills:
                skills.update([s.strip().lower() for s in tech_skills.split(',')])
            
            # Skills from vision-extracted data
            vision_data = user.get('vision_extracted_data', {})
            if isinstance(vision_data, str):
                try:
                    vision_data = json.loads(vision_data)
                except:
                    vision_data = {}
                    
            extracted_skills = vision_data.get('combined_skills', [])
            skills.update([s.lower() for s in extracted_skills])
            
            # Skills from projects/experience
            projects = user.get('projects', '')
            if projects:
                # Simple keyword extraction from projects description
                project_skills = self._extract_skills_from_text(projects)
                skills.update(project_skills)
                
            return skills
            
        except Exception as e:
            logger.error(f"Skill extraction failed: {e}")
            return set()
    
    def _extract_required_skills(self, internship: Dict) -> set:
        """Extract required skills from internship"""
        try:
            skills = set()
            
            required_skills = internship.get('required_skills', '')
            if required_skills:
                skills.update([s.strip().lower() for s in required_skills.split(',')])
                
            # Extract from job description
            description = internship.get('description', '')
            if description:
                desc_skills = self._extract_skills_from_text(description)
                skills.update(desc_skills)
                
            return skills
            
        except:
            return set()
    
    def _extract_skills_from_text(self, text: str) -> set:
        """Simple skill extraction from text"""
        # Common technical skills keywords
        common_skills = {
            'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'mysql',
            'mongodb', 'docker', 'kubernetes', 'aws', 'azure', 'git', 'html',
            'css', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
            'machine learning', 'ai', 'data science', 'analytics', 'tableau',
            'power bi', 'excel', 'linux', 'android', 'ios', 'flutter', 'django',
            'flask', 'spring', 'angular', 'vue', 'tensorflow', 'pytorch'
        }
        
        found_skills = set()
        text_lower = text.lower()
        
        for skill in common_skills:
            if skill in text_lower:
                found_skills.add(skill)
                
        return found_skills