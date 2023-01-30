from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_URL = "sqlite:///./sqlite.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread":False})

Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
