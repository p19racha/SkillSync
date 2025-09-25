"""
Add sample internship and company data for testing the recommendation engine
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Company, Internship
from datetime import datetime

app = create_app()

def add_sample_data():
    """Add sample companies and internships for testing"""
    
    with app.app_context():
        try:
            # Sample companies
            companies_data = [
                {
                    'company_name': 'TechCorp Solutions',
                    'company_email': 'hr@techcorp.com',
                    'password': 'password123',
                    'company_website': 'https://techcorp.com',
                    'company_description': 'Leading software development company specializing in web and mobile applications.'
                },
                {
                    'company_name': 'DataMinds Analytics',
                    'company_email': 'careers@dataminds.com',
                    'password': 'password123',
                    'company_website': 'https://dataminds.com',
                    'company_description': 'Data science and analytics company helping businesses make data-driven decisions.'
                },
                {
                    'company_name': 'Creative Studios',
                    'company_email': 'jobs@creativestudios.com',
                    'password': 'password123',
                    'company_website': 'https://creativestudios.com',
                    'company_description': 'Design agency creating stunning digital experiences and brand identities.'
                },
                {
                    'company_name': 'CloudTech Systems',
                    'company_email': 'internships@cloudtech.com',
                    'password': 'password123',
                    'company_website': 'https://cloudtech.com',
                    'company_description': 'Cloud infrastructure and DevOps solutions provider.'
                },
                {
                    'company_name': 'Green Energy Inc',
                    'company_email': 'hr@greenenergy.com',
                    'password': 'password123',
                    'company_website': 'https://greenenergy.com',
                    'company_description': 'Renewable energy solutions and sustainable technology development.'
                }
            ]

            companies = []
            for company_data in companies_data:
                # Check if company already exists
                existing_company = Company.query.filter_by(company_email=company_data['company_email']).first()
                if not existing_company:
                    company = Company(**company_data)
                    db.session.add(company)
                    companies.append(company)
                    print(f"✓ Added company: {company_data['company_name']}")
                else:
                    companies.append(existing_company)
                    print(f"⚠ Company already exists: {company_data['company_name']}")

            # Commit companies first
            db.session.commit()

            # Sample internships
            internships_data = [
                {
                    'company_email': 'hr@techcorp.com',
                    'internship_title': 'Full Stack Web Development Intern',
                    'industry_domain': 'Software Development',
                    'location_type': 'Hybrid',
                    'education_level': 'Undergraduate',
                    'duration': '3 months',
                    'minimum_gpa': 3.0,
                    'stipend': '₹15,000/month',
                    'fulltime_conversion': True,
                    'required_skills': 'React, Node.js, JavaScript, MongoDB, HTML, CSS',
                    'job_description': 'Work on building modern web applications using React and Node.js. Gain experience with full-stack development, API design, and database management. Perfect for students interested in web development career.'
                },
                {
                    'company_email': 'careers@dataminds.com',
                    'internship_title': 'Data Science & Machine Learning Intern',
                    'industry_domain': 'Data Science',
                    'location_type': 'Remote',
                    'education_level': 'Undergraduate',
                    'duration': '6 months',
                    'minimum_gpa': 3.2,
                    'stipend': '₹20,000/month',
                    'fulltime_conversion': True,
                    'required_skills': 'Python, Machine Learning, Pandas, NumPy, TensorFlow, SQL, Statistics',
                    'job_description': 'Analyze large datasets, build predictive models, and create data visualizations. Work with real-world data problems and learn cutting-edge ML techniques. Ideal for students with programming and math background.'
                },
                {
                    'company_email': 'jobs@creativestudios.com',
                    'internship_title': 'UI/UX Design Intern',
                    'industry_domain': 'Design',
                    'location_type': 'On-site',
                    'education_level': 'Undergraduate',
                    'duration': '4 months',
                    'minimum_gpa': 2.8,
                    'stipend': '₹12,000/month',
                    'fulltime_conversion': False,
                    'required_skills': 'Figma, Adobe XD, Prototyping, User Research, Wireframing, Design Thinking',
                    'job_description': 'Design user interfaces for web and mobile applications. Conduct user research, create wireframes and prototypes. Learn modern design principles and work with experienced design team.'
                },
                {
                    'company_email': 'internships@cloudtech.com',
                    'internship_title': 'DevOps & Cloud Infrastructure Intern',
                    'industry_domain': 'Cloud Computing',
                    'location_type': 'Remote',
                    'education_level': 'Undergraduate',
                    'duration': '5 months',
                    'minimum_gpa': 3.1,
                    'stipend': '₹18,000/month',
                    'fulltime_conversion': True,
                    'required_skills': 'AWS, Docker, Kubernetes, Linux, Python, Jenkins, Terraform',
                    'job_description': 'Learn cloud infrastructure management, containerization, and CI/CD pipelines. Work with AWS services and modern DevOps tools. Great for students interested in system administration and cloud technologies.'
                },
                {
                    'company_email': 'hr@techcorp.com',
                    'internship_title': 'Mobile App Development Intern',
                    'industry_domain': 'Mobile Development',
                    'location_type': 'Hybrid',
                    'education_level': 'Undergraduate',
                    'duration': '4 months',
                    'minimum_gpa': 2.9,
                    'stipend': '₹14,000/month',
                    'fulltime_conversion': True,
                    'required_skills': 'Flutter, Dart, React Native, JavaScript, Mobile UI/UX, APIs',
                    'job_description': 'Develop cross-platform mobile applications using Flutter and React Native. Learn mobile-specific design patterns and work on real client projects. Perfect for students interested in mobile development.'
                },
                {
                    'company_email': 'careers@dataminds.com',
                    'internship_title': 'Business Intelligence Analyst Intern',
                    'industry_domain': 'Business Analytics',
                    'location_type': 'On-site',
                    'education_level': 'Undergraduate',
                    'duration': '3 months',
                    'minimum_gpa': 3.0,
                    'stipend': '₹16,000/month',
                    'fulltime_conversion': False,
                    'required_skills': 'SQL, Tableau, Power BI, Excel, Data Visualization, Business Analysis',
                    'job_description': 'Create business reports and dashboards. Analyze business metrics and provide insights to management. Learn business intelligence tools and data storytelling techniques.'
                },
                {
                    'company_email': 'hr@greenenergy.com',
                    'internship_title': 'Renewable Energy Research Intern',
                    'industry_domain': 'Renewable Energy',
                    'location_type': 'On-site',
                    'education_level': 'Graduate',
                    'duration': '6 months',
                    'minimum_gpa': 3.3,
                    'stipend': '₹22,000/month',
                    'fulltime_conversion': True,
                    'required_skills': 'MATLAB, Python, Energy Systems, Research Methods, Data Analysis, Sustainability',
                    'job_description': 'Research renewable energy technologies and analyze energy efficiency data. Work on sustainability projects and contribute to clean energy solutions. Ideal for engineering students interested in environmental impact.'
                },
                {
                    'company_email': 'internships@cloudtech.com',
                    'internship_title': 'Cybersecurity Intern',
                    'industry_domain': 'Cybersecurity',
                    'location_type': 'Remote',
                    'education_level': 'Undergraduate',
                    'duration': '4 months',
                    'minimum_gpa': 3.2,
                    'stipend': '₹17,000/month',
                    'fulltime_conversion': True,
                    'required_skills': 'Network Security, Ethical Hacking, Python, Linux, Vulnerability Assessment, Security Tools',
                    'job_description': 'Learn cybersecurity fundamentals, conduct security assessments, and work with security monitoring tools. Gain hands-on experience in threat detection and incident response.'
                }
            ]

            # Add internships
            for internship_data in internships_data:
                # Find the company
                company = Company.query.filter_by(company_email=internship_data['company_email']).first()
                if not company:
                    print(f"✗ Company not found for email: {internship_data['company_email']}")
                    continue

                # Remove company_email from internship data and add company_id
                internship_info = internship_data.copy()
                del internship_info['company_email']
                internship_info['company_id'] = company.company_id

                # Check if internship already exists
                existing_internship = Internship.query.filter_by(
                    company_id=company.company_id,
                    internship_title=internship_info['internship_title']
                ).first()

                if not existing_internship:
                    internship = Internship(**internship_info)
                    db.session.add(internship)
                    print(f"✓ Added internship: {internship_data['internship_title']} at {company.company_name}")
                else:
                    print(f"⚠ Internship already exists: {internship_data['internship_title']} at {company.company_name}")

            # Commit all changes
            db.session.commit()
            
            print("\n✓ Successfully added sample companies and internships!")
            print(f"Total companies: {Company.query.count()}")
            print(f"Total internships: {Internship.query.count()}")
            
            return True
            
        except Exception as e:
            print(f"✗ Error adding sample data: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    add_sample_data()