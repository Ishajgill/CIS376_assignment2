# Assignment 02 - REST API

## Setup

1. Clone the repository
2. Create virtual environment
3. Install dependencies

pip install -r requirements.txt
## Run the server
python -m uvicorn api:app --reload --port 8001
## Endpoints

- GET /tweets
- GET /tweets/{tweet_id}
- GET /tweets/links
- GET /users/{screen_name}