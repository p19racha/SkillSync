# SkillSync

A smart internship matching platform that connects students with relevant opportunities. Built with Flask, machine learning, and document processing capabilities.

## What it does

SkillSync analyzes student profiles and matches them with internships that fit their skills, location, and career goals. Students can upload their resumes and certificates, and the system extracts relevant information to improve matching accuracy.

Companies can post internships and find qualified candidates automatically.

## Features

- Student profile creation with document upload
- AI-powered internship recommendations 
- Company dashboard for posting and managing internships
- Document processing using Ollama for skill extraction
- Location-based matching
- Clean REST API

## Setup

You'll need Python 3.9+, MySQL, and Ollama installed.

1. Clone the repo and install dependencies:
```bash
git clone https://github.com/p19racha/SkillSync.git
cd SkillSync

# Backend
cd backend
pip install -r requirements.txt

# AI Engine  
cd ../Engine
pip install -r requirements.txt
```

2. Set up your database and create a `.env` file in the backend folder:
```env
DATABASE_URL=mysql://username:password@localhost/skillsync_db
SECRET_KEY=your-secret-key
OLLAMA_API_URL=http://localhost:11434
```

3. Install Ollama and pull the required models:
```bash
ollama pull llava
```

4. Run the application:
```bash
# Start backend
cd backend && python run.py

# Start frontend (in another terminal)
cd frontend && python serve.py
```

Visit http://localhost:8000 for the student portal and http://localhost:8000/company for companies.

## Project Structure

The codebase is split into three main parts:

- `backend/` - Flask web app with API endpoints and database models
- `Engine/` - Machine learning recommendation system and document processing
- `frontend/` - HTML/CSS/JS user interfaces for students and companies

## Tech Stack

**Backend**: Flask, SQLAlchemy, MySQL, bcrypt
**AI/ML**: scikit-learn, pandas, Ollama, NLTK
**Frontend**: Vanilla JavaScript, CSS, HTML

## Contributing

Feel free to open issues or submit pull requests. The code follows standard Python conventions.