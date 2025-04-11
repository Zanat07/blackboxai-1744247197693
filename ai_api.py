from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
import json
from typing import Dict

app = FastAPI()

# Configurar puerto
import os
PORT = int(os.getenv("PORT", 8001))

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_URL = "https://83qvo7bbkb.execute-api.us-east-1.amazonaws.com/default/dav-dem-chatInvestmentAssistant"

@app.post("/query")
async def query_chatbot(request: Request):
    """Query the external chatbot API"""
    body = await request.json()
    prompt = body.get("prompt", "")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            API_URL,
            json={"prompt": prompt},
            timeout=30.0
        )
    
    if response.status_code != 200:
        return {"error": "Failed to get response from chatbot API"}
    
    return response.json()

@app.get("/")
async def root():
    """Root endpoint that redirects to health check"""
    return {"status": "ok", "message": "Chat Investment Assistant API"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}

@app.get("/favicon.ico")
async def favicon():
    """Empty favicon response to prevent 404 errors"""
    return Response(status_code=204)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT)
