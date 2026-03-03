from fastapi import FastAPI, HTTPException
import requests
import time
START_TIME = time.time()
app = FastAPI()
@app.get("/fingerprint")
def fingerprint():
    return {"start_time": START_TIME, "file": __file__}


URL = "https://foyzulhassan.github.io/files/favs.json"

@app.get("/whereami")
def whereami():
    return {"loaded_file": __file__}

@app.get("/tweets")
def get_all_tweets():
    try:
        data = requests.get(URL, timeout=15).json()
        result = []
        for t in data:
            result.append({
                "created_at": t.get("created_at"),
                "id": t.get("id") or t.get("id_str"),
                "text": t.get("text"),
            })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))