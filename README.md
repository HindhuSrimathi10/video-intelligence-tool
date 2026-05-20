# 🎬 VideoIntel — Video Competitor Intelligence Tool

A fully deployed web application that analyzes YouTube channel data for any company and its competitors, generates AI-powered insights, and produces a downloadable professional PowerPoint report.

---

## 🔗 Live Demo

👉 **[https://video-intelligence-tool.vercel.app](https://video-intelligence-tool.vercel.app)**

---

## 📌 What It Does

- Enter your company name and up to 4 competitors
- Fetches real YouTube data for all companies using YouTube Data API v3
- Analyzes the data using Groq AI (Llama 3)
- Displays a full competitive intelligence report on the web page
- Generates and downloads a professional 11-slide PowerPoint report

---

## 📊 PowerPoint Report Includes

| Slide | Content |
|---|---|
| 1 | Cover slide with company names and report date |
| 2 | Executive summary — who is leading and why |
| 3 | Channel overview — subscribers, videos, upload frequency |
| 4 | Content performance — top videos by views and engagement |
| 5 | Engagement analysis — avg views, likes, comments with charts |
| 6 | Content topics and themes — what each company covers |
| 7 | Posting frequency and consistency comparison |
| 8 | Gap analysis — missed opportunities and content gaps |
| 9 | Video marketing recommendations — actionable steps |
| 10 | Company rankings and scores out of 10 |
| 11 | Summary slide |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React + Vite |
| Backend | Python FastAPI |
| YouTube Data | YouTube Data API v3 |
| AI Insights | Groq API (Llama 3.3 70B) |
| PowerPoint | python-pptx |
| Frontend Deploy | Vercel |
| Backend Deploy | Render |

---

## 📁 Project Structure

```
video-intelligence-tool/
├── backend/
│   ├── main.py              # FastAPI app and routes
│   ├── youtube_service.py   # YouTube Data API integration
│   ├── groq_service.py      # Groq AI insight generation
│   ├── pptx_service.py      # PowerPoint report generation
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # API keys (not committed)
└── frontend/
    ├── src/
    │   ├── App.jsx          # Main React component
    │   └── App.css          # Styling
    ├── package.json
    └── vite.config.js
```

---

## ⚙️ Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/HindhuSrimathi10/video-intelligence-tool.git
cd video-intelligence-tool
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the backend folder:
```
YOUTUBE_API_KEY=your_youtube_api_key_here
GROQ_API_KEY=your_groq_api_key_here
```

Run the backend:
```bash
uvicorn main:app --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Open 👉 **http://localhost:5173**

---

## 🔑 API Keys Required

| API | Where to get |
|---|---|
| YouTube Data API v3 | [Google Cloud Console](https://console.cloud.google.com) |
| Groq API | [Groq Console](https://console.groq.com) |

---

## 🚀 Deployment

| Service | Platform | URL |
|---|---|---|
| Frontend | Vercel | https://video-intelligence-tool.vercel.app |
| Backend | Render | https://video-intelligence-backend.onrender.com |

---

## 📝 How to Use

1. Open the live tool 👉 https://video-intelligence-tool.vercel.app
2. Enter your company name
3. Enter up to 4 competitor names
4. Click **"Generate Intelligence Report"**
5. Wait 30-60 seconds for the report to generate
6. Read the full report on screen
7. Click **"Download PowerPoint"** to get the .pptx file

---

## ✨ Features

- ✅ Real YouTube data — not mock or placeholder data
- ✅ AI-generated strategic insights
- ✅ Professional PowerPoint with charts and rankings
- ✅ Clean, responsive UI
- ✅ Fully deployed and publicly accessible
- ✅ No login required

---

## 👩‍💻 Built By

**Hindhu Srimathi S K**
