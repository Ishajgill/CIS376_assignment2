from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def test_api():
    return {"message": "API is working!"}