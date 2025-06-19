# AI Product Video Generator (Chima Full Stack Case Study)

## 🎯 Loom Video
Link:

## 🎯 Sample Videos
Inside `backend/generated`

## 🎯 Overview
This project turns any Shopify (or compatible) product page into a modern vertical video ad using AI and video automation.

## 🧱 Tech Stack
- **Frontend:** React.js (w/ Axios, custom UI, modern styling)  
- **Backend:** FastAPI (Python)  
- **AI:** OpenAI (LLM for ad generation)  
- **Video:** MoviePy  
- **Scraping:** BeautifulSoup  

## 🚀 Features
- URL input and product scraping  
- AI ad copy generation  
- Video creation with animations and transitions  
- Responsive UI with video preview and download  
- 9:16 vertical format optimized for mobile

## 🛠️ Setup Instructions

### 1. Clone the Repository
git clone https://github.com/eemreerdal/chima-case-study.git
cd chima-case-study

### 2. Create Environment File
In the `backend/` directory, create a `.env` file:
OPENAI_API_KEY=your_openai_key_here

### 3. Install Dependencies
#### Backend (Python)
cd backend
pip install -r requirements
fastapi
uvicorn
requests
beautifulsoup4
moviepy
python-dotenv
openai

uvicorn main:app --reload

#### Frontend (React)
cd frontend
npm install
npm start
