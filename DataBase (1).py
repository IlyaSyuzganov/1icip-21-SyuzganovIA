from sqlalchemy import create_engine, Column, Integer, String, func
from sqlalchemy.orm import declarative_base, Session

password = int(input('Enter your password:'))
engine = create_engine(f"postgresql+psycopg2://postgres:{password}@localhost/UserDB")
Base = declarative_base()
session = Session(bind = engine)

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key = True)
    Login = Column(String(30), nullable=False)
    Password = Column(String(30), nullable=False)

Base.metadata.create_all(engine)