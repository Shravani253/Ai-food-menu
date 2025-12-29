from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

ENV = os.getenv("ENV")

app = FastAPI(title="FoodTransibility API")

@app.get("/env")
def env():
    return {"env": ENV}
