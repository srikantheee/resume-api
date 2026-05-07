from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber

app = FastAPI()

# Enable CORS (important)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def calculate_score(text):
    text = text.lower()
    score = 0

    skills = ["python", "sql", "aws", "etl", "US GAAP","AUDIT","MONTH END CLOSE","GST","TDS","IND AS"]
    score += min(sum(1 for s in skills if s in text) * 5, 30)

    if "experience" in text:
        score += 70

    if "project" in text:
        score += 15

    if len(text) > 800:
        score += 10

    return min(score, 100)


@app.post("/upload-resume")
async def upload_resume(file: UploadFile):
    text = ""

    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    score = calculate_score(text)

    return {
        "score": score,
        "message": "Resume analyzed"
    }
