from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, FileResponse
from summarizer import VideoSummarizer
from transcript import TranscriptFetcher
from datetime import datetime
import textwrap
import os
import fitz
import uuid
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Video Summarizer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


#Initialize Summarizer
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables.")

summarizer = VideoSummarizer(api_key=GROQ_API_KEY)

LATEST_SUMMARY = ""

#Common CSS for Centering
COMMON_STYLE = """
<style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin: 0;
        background-color: #f8f9fa;
        display: flex;
        justify-content: center;
        min-height: 100vh;
        padding: 40px 20px;
        box-sizing: border-box;
    }
    .container {
        width: 100%;
        max-width: 600px;
        margin: auto;
    }
    .card {
        background: white;
        padding: 40px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        text-align: center;
    }
    input {
        padding: 12px;
        width: 100%;
        box-sizing: border-box;
        border: 1px solid #ddd;
        border-radius: 8px;
        margin-bottom: 20px;
        font-size: 16px;
    }
    button {
        padding: 12px 24px;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        width: 100%;
        font-size: 16px;
        font-weight: 600;
        transition: background 0.2s;
    }
    button:hover { background-color: #0056b3; }
    
    .output-container {
        width: 100%;
        max-width: 800px;
        margin: auto;
    }
    .output {
        padding: 30px;
        margin-bottom: 20px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        white-space: pre-wrap;
        line-height: 1.7;
        color: #333;
    }
    .header-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    .download-btn {
        display: flex;
        align-items: center;
        gap: 8px;
        background: #28a745;
        color: white;
        padding: 8px 16px;
        border-radius: 6px;
        text-decoration: none;
        font-size: 14px;
        transition: opacity 0.2s;
    }
    .download-btn:hover { opacity: 0.9; }
    .back-link {
        display: inline-block;
        margin-top: 25px;
        margin-bottom: 40px;
        color: black;
        text-decoration: none;
    }
</style>
"""

# Home Page
@app.get("/", response_class=HTMLResponse)
def home():
    return f"""
    <html>
        <head>
            <title>AI Video Summarizer</title>
            {COMMON_STYLE}
        </head>
        <body>
            <div class="container">
                <div class="card">
                    <h2 style="margin-top:0">🎥 AI Video Summarizer</h2>
                    <form action="/generate" method="post">
                        <input type="text" name="video_id" placeholder="Enter YouTube Video ID" required />
                        <button type="submit">Generate Summary</button>
                    </form>
                </div>
            </div>
        </body>
    </html>
    """

# Generate Summary
@app.post("/generate", response_class=HTMLResponse)
def generate(video_id: str = Form(...)):
    global LATEST_SUMMARY
    try:
        transcript = TranscriptFetcher.get_transcript(video_id)
        if not transcript or transcript.strip() == "":
            raise ValueError("Transcript not available for this video.")
        result = summarizer.generate_brief_summary(transcript)
        LATEST_SUMMARY = result
    except Exception as e:
        result = f"Error: {str(e)}"

    return f"""
    <html>
        <head>
            <title>Summary Result</title>
            {COMMON_STYLE}
        </head>
        <body>
            <div class="output-container">
                <div class="header-row">
                    <h2 style="margin:0">Generated Summary</h2>
                    <a href="/download?video_id={video_id}" class="download-btn">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
                        Download PDF
                    </a>
                </div>

                <div class="output">{result}</div>

                <a href="/" class="back-link">⬅ Back to Summarizer</a>
            </div>
        </body>
    </html>
    """

# Download PDF
@app.get("/download")
def download_pdf(video_id: str = ""):
    global LATEST_SUMMARY
    if not LATEST_SUMMARY:
        return {"error": "No summary available."}

    filename = f"summary_{uuid.uuid4().hex}.pdf"
    filepath = filename
    doc = fitz.open()
    margin, page_width, page_height = 72, 595, 842
    page = doc.new_page(width=page_width, height=page_height)
    
    y_position = margin
    page.insert_text((margin, y_position), "AI Video Summary Report", fontsize=20, fontname="helv")
    y_position += 40
    metadata = f"Video ID: {video_id}\nGenerated On: {datetime.now().strftime('%d %B %Y, %H:%M')}"
    page.insert_text((margin, y_position), metadata, fontsize=11, fontname="helv")
    y_position += 50
    page.draw_line((margin, y_position), (page_width - margin, y_position))
    y_position += 20

    wrapped_text = textwrap.wrap(LATEST_SUMMARY, width=90)
    for line in wrapped_text:
        if y_position > page_height - margin:
            page = doc.new_page(width=page_width, height=page_height)
            y_position = margin
        page.insert_text((margin, y_position), line, fontsize=12, fontname="helv")
        y_position += 18

    doc.save(filepath)
    doc.close()
    return FileResponse(path=filepath, filename="video_summary.pdf", media_type="application/pdf")
