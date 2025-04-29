from sqlalchemy import create_engine, Column, Integer, String, DateTime, or_
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from crawler.metadata import MetadataItem

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
        engine = create_engine(f"sqlite:///{database_name}", echo=False, pool_size=10, max_overflow=20)
        Base.metadata.create_all(engine)
        self._Session = sessionmaker(bind=engine)
        

    def add(self, item):
        session = self._Session()
        session.add(item)
        session.commit()
        #session.close()
        return item.id
    
    def add_all(self, items):
        session = self._Session()
        session.add_all(items)
        session.commit()
        session.close()
    
    def select_page(self, url:str):
        session = self._Session()
        query = session.query(Pages).where(Pages.url == url).all()
        #session.close()
        return query
    
    def select_files(self, url:str):
        session = self._Session()
        query = session.query(Files).where(Files.url == url).all()
        #session.close()
        return query
    
    def get_metadata(self, filters) -> MetadataItem:
        session = self._Session()
        conditions = [Metadata.key.like(f"%{k}") for k in filters]
        query = session.query(Metadata, Files.url).join(Files, Files.id == Metadata.file_id).where(
            or_(*conditions)).distinct()
        
        result = query.all()
        rows = []
        for v,u in result:
            rows.append(MetadataItem(key=v.key, id=v.id, url=u, value=v.value, created=v.created))
        
        return rows
    
    def get_users(self):
        return self.get_metadata(['Author','author','user','User'])
        

    def get_summary(self):
        return self.get_metadata(['Author','Creator'])
        

    
    
    
