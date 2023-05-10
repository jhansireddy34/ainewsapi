from fastapi import FastAPI
from typing import Union
import config
import news
import models
import datetime

from fastapi.middleware.cors import CORSMiddleware

origins = [
  
    "http://localhost",
    "http://localhost:5173",

]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.create_db()


@app.get("/news/{category}")
async def get_latest_ainews(category):
    print(category)
    
    now=datetime.datetime.now().strftime("%Y%m%d%h")
    await news.refresh_news(now,category)
    output=await news.fetch_news_from_db(category)
    
    return output
    
   


