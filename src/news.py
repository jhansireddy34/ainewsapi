from functools import lru_cache
import aiohttp
import config
import datetime
import database
import models
from sqlalchemy import delete
from cache import AsyncLRU
import base64





async def get_news_update(filter="Artificial Intelligence"):
    yesterday=(datetime.datetime.today()+datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
    headers={"X-Api-Key": config.secrets["news_api"]}
    params={"from": yesterday,"q": filter,"searchIn": "content","language": "en"}


    async with aiohttp.ClientSession() as session:
        async with session.get(config.NEWS_API_URL,params=params,headers=headers) as response:
            output=await response.json()
            
            if output.get("articles"):
                return output.get("articles")
            

async def update_news_to_db(filter="Artificial Intelligence"):
    
    new_news=await get_news_update(filter=filter)
    session=database.SessionLocal()
    try:

        for record in new_news:
            dbrecord=models.News()
            dbrecord.author=record.get("author")
            dbrecord.title=record.get("title")
            dbrecord.id=base64.b16encode(bytes(record.get("title"),'utf-8'))[slice(30)]
            dbrecord.description=record.get("description")
            dbrecord.url=record.get("url")
            dbrecord.source=record.get("source",{}).get("name","unknown")
            dbrecord.imageUrl=record.get("urlToImage")
            dbrecord.content=record.get("content")
            dbrecord.publishedAt=record.get("publishedAt")
            dbrecord.newsdate=datetime.datetime.strptime(record.get("publishedAt").split("T")[0],"%Y-%m-%d")
            dbrecord.filter=filter
            session.merge(dbrecord)
            session.commit()
            print("db insert successfull")
    except Exception as err:
        print(err)
        session.rollback()

    finally:
        session.close()

async def fetch_news_from_db(filter):
    session=database.SessionLocal()
    output=[]
    try:
        allrecords=session.query(models.News).where(models.News.filter==filter).all()
        print(allrecords)
        for record in allrecords:
            recorddict=record.__dict__
            output.append(recorddict)
    except Exception as err:
        print(err)
    finally:
        session.close()
    return output                




@AsyncLRU(maxsize=128)
async def refresh_news(thishour,filter):
    print("running it")
    session=database.SessionLocal()
    try:

        await update_news_to_db(filter=filter)
        daybefore=(datetime.datetime.today()+datetime.timedelta(days=-2))
        oldnews=session.query(models.News).where(models.News.newsdate < daybefore)
        
        session.commit()
    except Exception as err:
        raise err
    finally:
        if session:
            session.close()        

    









    

