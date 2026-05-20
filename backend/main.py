from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Video Intelligence Tool")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from youtube_service import get_channel_data
from groq_service import generate_insights
from pptx_service import create_pptx_report
from pydantic import BaseModel
from typing import List

class ReportRequest(BaseModel):
    company_name: str
    competitors: List[str]

@app.get("/")
def root():
    return {"message": "Video Intelligence Tool API is running"}

@app.post("/generate-report")
async def generate_report(request: ReportRequest):
    all_companies = [request.company_name] + request.competitors
    
    # Step 1: Fetch YouTube data for all companies
    all_data = {}
    for company in all_companies:
        print(f"Fetching data for: {company}")
        data = get_channel_data(company)
        all_data[company] = data
    
    # Step 2: Generate AI insights
    print("Generating AI insights...")
    insights = generate_insights(all_data)
    
    # Step 3: Create PowerPoint
    print("Creating PowerPoint...")
    pptx_path = create_pptx_report(all_data, insights, request.company_name)
    
    return {
        "success": True,
        "report_data": all_data,
        "insights": insights,
        "pptx_filename": pptx_path
    }

@app.get("/download-report/{filename}")
async def download_report(filename: str):
    file_path = f"./{filename}"
    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
    return {"error": "File not found"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)