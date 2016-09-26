from sqlalchemy import create_engine, Column, Integer, String, Unicode
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from functools import wraps


db_url = 'postgresql+psycopg2://beat@localhost/chat2_db'

engine = create_engine(db_url)
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()


def call_query(func):
    @wraps(func)
    def wrapper():
        query = db_session.query(User)
        return func(query)
    return wrapper


def init_db():
    Base.metadata.create_all(engine)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    userid = Column(String(20), nullable=False)
    password_hash = Column(String(60), nullable=False)
    username = Column(Unicode(20), nullable=False)

    def __init__(self, userid, password_hash, username):
        self.userid = userid
        self.password_hash = password_hash
        self.username = username

    def __repr__(self):
        return "<User : %s, %s, %s>" % (self.userid, self.password_hash, self.username)
