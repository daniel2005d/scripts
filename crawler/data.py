from sqlalchemy import create_engine, Column, Integer, String, DateTime, or_
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()

class Pages(Base):
    __tablename__ = "pages"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    created = Column(DateTime, default=datetime.now)

class Metadata(Base):
    __tablename__ = "metadata"
    id = Column(Integer, primary_key=True)
    file_id = Column(Integer)
    created = Column(DateTime, default=datetime.now)
    key = Column(String)
    value = Column(String)

class Files(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    created = Column(DateTime, default=datetime.now)

class DBData:
    def __init__(self, database_name:str):
        engine = create_engine(f"sqlite:///{database_name}", echo=False)
        Base.metadata.create_all(engine)
        self._Session = sessionmaker(bind=engine)
        

    def add(self, item):
        session = self._Session()
        session.add(item)
        session.commit()
        return item.id
    
    def add_all(self, items):
        session = self._Session()
        session.add_all(items)
        session.commit()
    
    def select_page(self, url:str):
        session = self._Session()
        query = session.query(Pages).where(Pages.url == url).all()
        return query
    
    def select_files(self, url:str):
        session = self._Session()
        query = session.query(Files).where(Files.url == url).all()
        return query

    def get_summary(self):
        session = self._Session()
        query = session.query(Metadata).filter(
            or_(
                Metadata.key == 'PDF:Author',
                Metadata.key == 'PDF:Creator'
            )
        ).distinct()
        return query.all()

    
    
    
