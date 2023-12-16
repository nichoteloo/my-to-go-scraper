import os
from dotenv import load_dotenv
from datetime import datetime, date, time
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm.exc import NoResultFound

load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'), echo=True)
Session = sessionmaker(bind=engine)
db_session = Session()

Base = declarative_base()

class BaseMixin(object):
    id         = Column(Integer, primary_key=True)
    created_at =        Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at =        Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_dict(self):
        cols = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for k, v in cols.items():
            if isinstance(v, datetime):
                cols[k] = v.isoformat()
            elif isinstance(v, date):
                cols[k] = v.strftime("%Y-%m-%d")
            elif isinstance(v, time):
                cols[k] = v.strftime("%H:%M:%S")
        return cols

    def save(self):
        db_session.add(self)
        db_session.commit()
        return self
    
class Item(Base, BaseMixin):
    __tablename__ = 'items'

    url = Column(String, unique=True)

class Keyword(Base, BaseMixin):
    __tablename__ = 'keywords'

    keyword = Column(String, unique=True)
    items = association_proxy("search_results", "item")

# class HockeyTeam(Base, BaseMixin):
#     __tablename__ = 'hoekey_teams'

#     name = Column(String)
#     year = Column(Integer)
#     wins = Column(Integer)
#     losses = Column(Integer)
#     hockey_teams = association_proxy("search_results", "hockey_team")

class SearchResult(Base, BaseMixin):
    __tablename__ = 'search_results'

    rank = Column(Integer)
    rank_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    item_id = Column(Integer, ForeignKey('items.id'))
    keyword_id = Column(Integer, ForeignKey('keywords.id'))

    item = relationship("Item", backref="search_results")
    keyword = relationship("Keyword", backref="search_results")

    @declared_attr
    def __table_args__(cls):
        return (
            UniqueConstraint('rank', 'rank_at', 'keyword_id', name='unique_rank_per_keyword_per_scrape'),
        )