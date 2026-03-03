from fastapi import FastAPI, HTTPException
import requests
import re

app = FastAPI()
URL = "https://foyzulhassan.github.io/files/favs.json"
URL_RE = re.compile(r"https?://[^\s]+")
@app.get("/tweets")
def get_all_tweets():
    try:
        data = requests.get(URL, timeout=15).json()
        return [{
            "created_at": t.get("created_at"),
            "id": t.get("id") or t.get("id_str"),
            "text": t.get("text"),
        } for t in data]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/tweets/{tweet_id}")
def get_tweet_by_id(tweet_id: str):
    data = requests.get(URL, timeout=15).json()
    for t in data:
        tid = str(t.get("id") or t.get("id_str"))
        if tid == tweet_id:
            return {
                "created_at": t.get("created_at"),
                "text": t.get("text"),
                "screen_name": t.get("user", {}).get("screen_name")
            }

    raise HTTPException(status_code=404, detail="Tweet not found")
@app.get("/tweets/links")
def get_links_grouped():
    data = requests.get(URL, timeout=15).json()

    grouped = {}
    for t in data:
        tid = str(t.get("id") or t.get("id_str"))
        text = t.get("text") or ""
        links = URL_RE.findall(text)

        # optional cleanup for trailing punctuation
        links = [u.rstrip(").,!?]\"'") for u in links]

        grouped[tid] = links

    return grouped
