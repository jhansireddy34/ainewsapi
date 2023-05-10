from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime
from sqlalchemy.orm import relationship

from database import Base,SessionLocal,engine


class News(Base):
    __tablename__ = "News"

    id = Column(String, primary_key=True)
    source = Column(String)
    author= Column(String)
    url=Column(String)
    imageUrl=Column(String)
    publishedAt=Column(String)
    title = Column(String)
    description = Column(String)
    content = Column(String)
    filter = Column(String)
    newsdate = Column(DateTime)
    

   



def create_db():
    Base.metadata.create_all(engine)
