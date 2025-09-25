"""
Data extraction utilities for processing user and internship data
"""

import json
import re
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

class DataExtractor:
    """
    Utility class for extracting and processing data from various sources
    """
    
    def __init__(self):
        self.skill_patterns = self._load_skill_patterns()
        
    def _load_skill_patterns(self) -> Dict[str, List[str]]:
        """Load patterns for skill extraction"""
        return {
            'programming': [
                r'\b(?:python|java|javascript|js|typescript|ts|c\+\+|cpp|c#|csharp|php|ruby|go|rust|kotlin|swift|scala|r|matlab|perl)\b',
            ],
            'web_frameworks': [
                r'\b(?:react|angular|vue|django|flask|spring|express|laravel|rails|nextjs|gatsby|svelte)\b',
            ],
            'databases': [
                r'\b(?:mysql|postgresql|postgres|mongodb|sqlite|redis|cassandra|oracle|sql server|dynamodb)\b',
            ],
            'cloud_platforms': [
                r'\b(?:aws|azure|gcp|google cloud|docker|kubernetes|heroku|netlify|vercel)\b',
            ],
            'tools': [
                r'\b(?:git|github|gitlab|jira|slack|trello|figma|photoshop|illustrator|sketch)\b',
            ],
            'data_science': [
                r'\b(?:machine learning|ml|ai|artificial intelligence|tensorflow|pytorch|pandas|numpy|scikit-learn|jupyter|tableau|power bi)\b',
            ]
        }
    
    def extract_skills_from_text(self, text: str, categories: Optional[List[str]] = None) -> Dict[str, List[str]]:
        """
        Extract skills from text using pattern matching
        
        Args:
            text: Input text to extract skills from
            categories: Specific skill categories to extract (optional)
            
        Returns:
            Dictionary mapping categories to found skills
        """
        if not text:
            return {}
            
        text_lower = text.lower()
        extracted_skills = {}
        
        categories_to_check = categories or list(self.skill_patterns.keys())
        
        for category in categories_to_check:
            if category not in self.skill_patterns:
                continue
                
            category_skills = []
            for pattern in self.skill_patterns[category]:
                matches = re.findall(pattern, text_lower, re.IGNORECASE)
                category_skills.extend(matches)
            
            if category_skills:
                extracted_skills[category] = list(set(category_skills))  # Remove duplicates
                
        return extracted_skills
    
    def normalize_user_data(self, user_data: Dict) -> Dict[str, Any]:
        """
        Normalize and enrich user data for recommendation processing
        
        Args:
            user_data: Raw user data from database
            
        Returns:
            Processed and normalized user data
        """
        try:
            normalized = {}
            
            # Basic information
            normalized['user_id'] = user_data.get('user_id', '')
            normalized['name'] = user_data.get('name', '')
            normalized['email'] = user_data.get('username', '')
            
            # Location data
            normalized['city'] = user_data.get('city', '')
            normalized['state'] = user_data.get('state', '')
            normalized['pincode'] = user_data.get('pincode', '')
            
            # Education
            normalized['education_level'] = user_data.get('education_level', '')
            normalized['degree'] = user_data.get('degree', '')
            normalized['year_of_study'] = user_data.get('year_of_study', '')
            normalized['gpa_percentage'] = user_data.get('gpa_percentage', 0.0)
            
            # Skills and preferences
            normalized['technical_skills'] = user_data.get('technical_skills', '')
            normalized['soft_skills'] = user_data.get('soft_skills', '')
            normalized['preferred_industry'] = user_data.get('preferred_industry', '')
            normalized['internship_type_preference'] = user_data.get('internship_type_preference', '')
            normalized['duration_preference'] = user_data.get('duration_preference', '')
            normalized['stipend_expectation'] = user_data.get('stipend_expectation', 0)
            
            # Experience
            normalized['previous_internships'] = user_data.get('previous_internships', '')
            normalized['projects'] = user_data.get('projects', '')
            
            # Process vision extracted data
            vision_data = user_data.get('vision_extracted_data')
            if vision_data:
                normalized['vision_data'] = self._process_vision_data(vision_data)
            else:
                normalized['vision_data'] = {}
                
            # Derive additional fields
            normalized['all_skills'] = self._combine_all_skills(normalized)
            normalized['experience_level'] = self._calculate_experience_level(normalized)
            normalized['location_flexibility'] = self._assess_location_flexibility(normalized)
            
            return normalized
            
        except Exception as e:
            logger.error(f"User data normalization failed: {e}")
            return user_data  # Return original data if processing fails
    
    def normalize_internship_data(self, internship_data: Dict) -> Dict[str, Any]:
        """
        Normalize and enrich internship data for recommendation processing
        
        Args:
            internship_data: Raw internship data from database
            
        Returns:
            Processed and normalized internship data
        """
        try:
            normalized = {}
            
            # Basic information
            normalized['internship_id'] = internship_data.get('internship_id', '')
            normalized['title'] = internship_data.get('title', '')
            normalized['company_name'] = internship_data.get('company_name', '')
            normalized['description'] = internship_data.get('description', '')
            
            # Location
            normalized['city'] = internship_data.get('city', '')
            normalized['state'] = internship_data.get('state', '')
            normalized['remote_allowed'] = internship_data.get('remote_allowed', False)
            
            # Requirements
            normalized['required_skills'] = internship_data.get('required_skills', '')
            normalized['education_requirement'] = internship_data.get('education_requirement', '')
            normalized['experience_required'] = internship_data.get('experience_required', '')
            
            # Details
            normalized['duration'] = internship_data.get('duration', '')
            normalized['stipend'] = internship_data.get('stipend', 0)
            normalized['type'] = internship_data.get('type', '')
            normalized['industry'] = internship_data.get('industry', '')
            
            # Dates
            normalized['posted_date'] = internship_data.get('posted_date', '')
            normalized['application_deadline'] = internship_data.get('application_deadline', '')
            
            # Performance metrics (for recommendation scoring)
            normalized['click_through_rate'] = internship_data.get('click_through_rate', 0.05)
            normalized['apply_rate'] = internship_data.get('apply_rate', 0.02)
            normalized['total_applications'] = internship_data.get('total_applications', 0)
            normalized['total_selections'] = internship_data.get('total_selections', 0)
            
            # Process and extract skills
            normalized['parsed_skills'] = self.extract_skills_from_text(
                f"{normalized['required_skills']} {normalized['description']}"
            )
            
            # Calculate derived metrics
            normalized['competitiveness'] = self._calculate_competitiveness(normalized)
            normalized['popularity_score'] = self._calculate_popularity_score(normalized)
            
            return normalized
            
        except Exception as e:
            logger.error(f"Internship data normalization failed: {e}")
            return internship_data
    
    def _process_vision_data(self, vision_data: Any) -> Dict[str, Any]:
        """Process vision extracted data"""
        try:
            if isinstance(vision_data, str):
                vision_data = json.loads(vision_data)
            
            processed = {
                'extracted_skills': [],
                'extracted_technologies': [],
                'certificates': [],
                'projects': [],
                'education_details': {}
            }
            
            if isinstance(vision_data, dict):
                # Extract combined skills
                processed['extracted_skills'] = vision_data.get('combined_skills', [])
                processed['extracted_technologies'] = vision_data.get('combined_technologies', [])
                
                # Process individual extractions
                individual_extractions = vision_data.get('individual_extractions', [])
                for extraction in individual_extractions:
                    if extraction.get('success', False):
                        data = extraction.get('extracted_data', {})
                        doc_type = extraction.get('document_type', '')
                        
                        if doc_type == 'certificate':
                            processed['certificates'].append(data)
                        elif doc_type == 'resume':
                            if 'projects' in data:
                                processed['projects'].extend(data['projects'])
                            if 'education' in data:
                                processed['education_details'] = data['education']
                        elif doc_type == 'transcript':
                            processed['education_details'].update(data)
            
            return processed
            
        except Exception as e:
            logger.error(f"Vision data processing failed: {e}")
            return {}
    
    def _combine_all_skills(self, user_data: Dict) -> List[str]:
        """Combine skills from all sources"""
        all_skills = set()
        
        # Manual skills
        tech_skills = user_data.get('technical_skills', '')
        if tech_skills:
            all_skills.update([s.strip() for s in tech_skills.split(',') if s.strip()])
            
        soft_skills = user_data.get('soft_skills', '')
        if soft_skills:
            all_skills.update([s.strip() for s in soft_skills.split(',') if s.strip()])
        
        # Vision extracted skills
        vision_data = user_data.get('vision_data', {})
        all_skills.update(vision_data.get('extracted_skills', []))
        all_skills.update(vision_data.get('extracted_technologies', []))
        
        return list(all_skills)
    
    def _calculate_experience_level(self, user_data: Dict) -> str:
        """Calculate experience level based on available data"""
        try:
            # Factors to consider
            previous_internships = user_data.get('previous_internships', '')
            projects = user_data.get('projects', '')
            year_of_study = user_data.get('year_of_study', '')
            
            score = 0
            
            # Previous experience
            if previous_internships and len(previous_internships) > 50:  # Substantial description
                score += 2
            elif previous_internships:
                score += 1
                
            # Project experience
            if projects and len(projects) > 100:  # Detailed projects
                score += 2
            elif projects:
                score += 1
                
            # Academic level
            if 'final' in year_of_study.lower() or '4' in year_of_study:
                score += 1
            elif '3' in year_of_study:
                score += 0.5
                
            # Vision-extracted experience
            vision_data = user_data.get('vision_data', {})
            certificates = len(vision_data.get('certificates', []))
            score += min(certificates * 0.5, 2)  # Max 2 points from certificates
            
            # Classify experience level
            if score >= 4:
                return 'experienced'
            elif score >= 2:
                return 'intermediate'
            else:
                return 'beginner'
                
        except:
            return 'beginner'
    
    def _assess_location_flexibility(self, user_data: Dict) -> Dict[str, Any]:
        """Assess user's location flexibility"""
        try:
            flexibility = {
                'willing_to_relocate': True,  # Default assumption
                'remote_work_preference': False,
                'preferred_locations': [],
                'current_location': f"{user_data.get('city', '')} {user_data.get('state', '')}"
            }
            
            # Analyze internship type preference for remote indicators
            type_pref = user_data.get('internship_type_preference', '').lower()
            if 'remote' in type_pref or 'online' in type_pref:
                flexibility['remote_work_preference'] = True
                
            # Extract preferred locations from various fields
            preferred_industry = user_data.get('preferred_industry', '')
            if any(location in preferred_industry.lower() for location in ['mumbai', 'delhi', 'bangalore', 'pune', 'hyderabad', 'chennai']):
                # Industry preference might indicate location preference
                pass
                
            return flexibility
            
        except:
            return {'willing_to_relocate': True, 'remote_work_preference': False}
    
    def _calculate_competitiveness(self, internship_data: Dict) -> float:
        """Calculate how competitive an internship is"""
        try:
            applications = internship_data.get('total_applications', 0)
            selections = internship_data.get('total_selections', 1)
            
            if applications == 0:
                return 0.0  # No data
                
            # Higher applications per selection = more competitive
            ratio = applications / selections
            
            # Normalize to 0-1 scale (assume max competitive ratio of 100)
            return min(1.0, ratio / 100.0)
            
        except:
            return 0.5
    
    def _calculate_popularity_score(self, internship_data: Dict) -> float:
        """Calculate internship popularity score"""
        try:
            ctr = internship_data.get('click_through_rate', 0.05)
            apply_rate = internship_data.get('apply_rate', 0.02)
            
            # Combine CTR and apply rate
            popularity = (ctr * 0.7) + (apply_rate * 0.3)
            
            # Normalize (typical good CTR might be 0.1, apply rate 0.05)
            return min(1.0, popularity / 0.1)
            
        except:
            return 0.5