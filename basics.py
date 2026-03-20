from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello":"I am Manthan."}

@app.get("/about")
def about():
    return {"message":"I am an AI/ML Developer."}