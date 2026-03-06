from fastapi import FastAPI, HTTPException
import requests
import re
# Create the FastAPI application
app = FastAPI()
URL = "https://foyzulhassan.github.io/files/favs.json"
# Regular expression used to find URLs inside tweet text
# Matches http:// or https:// followed by any characters until whitespace
URL_RE = re.compile(r"https?://[^\s]+")
# Endpoints
# Get tweets
@app.get("/tweets")
def get_all_tweets():
    try:
        # Download the JSON file and .json parses JSON string to python structure
        data = requests.get(URL, timeout=15).json()
        # Build a new list containing only selected tweet fields
        return [{
            "created_at": t.get("created_at"),
            "id": t.get("id") or t.get("id_str"),
            "text": t.get("text"),
        } for t in data]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get tweets/links

@app.get("/tweets/links")
def get_links_grouped():
    data = requests.get(URL, timeout=15).json()
    # Dictionary that will store:
    # {tweet_id : [list_of_links]}
    grouped = {}
    for t in data:
        tid = str(t.get("id") or t.get("id_str"))
        text = t.get("text") or ""
        # Use regex to find all URLs in the tweet text
        links = URL_RE.findall(text)
        #  cleanup for trailing punctuation
        links = [u.rstrip(").,!?]\"'") for u in links]

        grouped[tid] = links

    return grouped

 # GET /tweets/{tweet_id}

@app.get("/tweets/{tweet_id}")
def get_tweet_by_id(tweet_id: str):
    data = requests.get(URL, timeout=15).json()
    for t in data:
        # Convert tweet ID to string for comparison
        tid = str(t.get("id") or t.get("id_str"))
        # Check if this tweet matches the requested ID
        if tid == tweet_id:
            return {
                "created_at": t.get("created_at"),
                "text": t.get("text"),
                "screen_name": t.get("user", {}).get("screen_name")
            }

    raise HTTPException(status_code=404, detail="Tweet not found")

# user profile by screen name
@app.get("/users/{screen_name}")
def get_user_profile(screen_name: str):
    # Download the JSON file  and .json parses JSON string to python structure
    data = requests.get(URL, timeout=15).json()
    # Go through every tweet in that list
    for t in data:
        # Each tweet has a "user" object (dictionary)
        user = t.get("user") or {}
        #  Compare the user's screen_name to what is given in the URL
        if (user.get("screen_name") or "").lower().strip() == screen_name.lower().strip():
            return {
                "location": user.get("location"),
                "description": user.get("description"),
                "followers_count": user.get("followers_count"),
                "friends_count": user.get("friends_count"),
            }

    raise HTTPException(status_code=404, detail="User not found")
