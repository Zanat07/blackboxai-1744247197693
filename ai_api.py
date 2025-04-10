from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import httpx
from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data
with open('data.json') as f:
    data = json.load(f)

# Initialize embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Pre-embed financial data
financial_embeddings = []
for record in data['financial']:
    text = f"On {record['Date']}, stock price was {record['StockPrice']}, revenue was {record['Revenue']}, net income was {record['NetIncome']}, ROI was {record['ROI']}%, market cap was {record['MarketCap']}"
    embedding = model.encode(text)
    financial_embeddings.append(embedding)
financial_embeddings = np.array(financial_embeddings)

@app.get("/query")
async def query_financial_data(q: str, top_k: int = 3):
    """Query financial data using semantic search"""
    query_embedding = model.encode(q)
    similarities = np.dot(financial_embeddings, query_embedding)
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    
    results = []
    for idx in top_indices:
        results.append(data['financial'][idx])
    
    return {"query": q, "results": results}

@app.get("/data")
async def get_all_data():
    """Get all financial data"""
    return data

@app.post("/chat")
async def post_to_aws(prompt: str):
    """Send a prompt to the AWS service and return the response."""
    payload = {"prompt": prompt}
    async with httpx.AsyncClient() as client:
        response = await client.post("https://83qvo7bbkb.execute-api.us-east-1.amazonaws.com/default/dav-dem-chatInvestmentAssistant", json=payload)
        response_data = response.json()
    
    # Assuming the response contains a "chat_response" field
    return {"chat_response": response_data.get("chat_response", "No response from service")}
