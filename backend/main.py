from fastapi import FastAPI, Form
import requests

app = FastAPI()

def query_model(prompt: str):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "mistral", "prompt": prompt, "stream": False}
    )
    return response.json()["response"].strip()

@app.post("/analyze/")
def analyze_call(text: str = Form(...)):
    prompts = {
        "summary": f"Summarize the following earnings call transcript in 3 sentences:\n{text}",
        "sentiment": f"What is the overall sentiment (Positive, Neutral, Negative) of the following transcript?\n{text}",
        "insights": f"Extract key financial insights (growth, risk, guidance, etc.) from the following transcript:\n{text}"
    }
    result = {k: query_model(p) for k, p in prompts.items()}
    return result
