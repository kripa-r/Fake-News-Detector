from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import pandas as pd

# Custom modules
from scraper import scrape_article_text
from model import clean_text # Reuse the cleaning function

app = FastAPI(title="Fake News Detector API")

# This allows the frontend (running on a different origin) to communicate with the backend
origins = ["*"] # In production, restrict this to your frontend's domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the trained model and vectorizer
with open("trained_model/model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("trained_model/vectorizer.pkl", "rb") as vectorizer_file:
    vectorizer = pickle.load(vectorizer_file)

# Pydantic models for request and response data validation
class URLRequest(BaseModel):
    url: str

class AnalysisResponse(BaseModel):
    url: str
    classification: str
    confidence_score: float

@app.get("/")
def read_root():
    return {"status": "API is running"}

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_url(request: URLRequest):
    """
    Accepts a URL, scrapes its content, and classifies it as real or fake.
    """
    scraped_text = scrape_article_text(request.url)
    
    if not scraped_text:
        return {"url": request.url, "classification": "Error", "confidence_score": 0.0}

    # Preprocess and vectorize the text
    cleaned_text = clean_text(scraped_text)
    text_vector = vectorizer.transform([cleaned_text])
    
    # Make prediction
    prediction = model.predict(text_vector)[0]
    prediction_prob = model.predict_proba(text_vector)[0]

    if prediction == 1:
        classification = "Real News"
        confidence = prediction_prob[1]
    else:
        classification = "Fake News"
        confidence = prediction_prob[0]

    return {
        "url": request.url,
        "classification": classification,
        "confidence_score": float(confidence)
    }

# Placeholder endpoints for history and stats
@app.get("/api/history")
def get_history():
    # In a real app, this would fetch from a database.
    return {"message": "History endpoint not fully implemented."}

@app.get("/api/stats")
def get_stats():
    # Returns some basic model stats
    return {"model": "Logistic Regression", "accuracy_on_test_set": 0.988} # Example value