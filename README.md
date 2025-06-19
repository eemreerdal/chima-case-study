# AI Product Video Generator (Chima Full Stack Case Study)

## 🎯 Overview
This project turns any Shopify (or compatible) product page into a modern vertical video ad using AI and video automation.

## 🧱 Tech Stack
- Frontend: React.js (w/ Axios, custom UI, modern styling)
- Backend: FastAPI (Python)
- AI: OpenAI (LLM for ad generation)
- Video: MoviePy
- Scraping: BeautifulSoup

## 🚀 Features
- URL input and product scraping
- AI ad copy generation
- Video creation with animations and transitions
- Responsive UI: preview + download
- 9:16 vertical format

## 🛠️ Setup Instructions

1. Clone the repo:
git clone

2. Create Environment File
In the backend/ directory, create a .env file:
OPENAI_API_KEY=your_openai_key_here

📥 Install Dependencies
Backend (Python)
pip install -r 
fastapi
uvicorn
requests
beautifulsoup4
moviepy
python-dotenv
openai
cd backend

uvicorn main:app --reload


Frontend (React)
npm install
