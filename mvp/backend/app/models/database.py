from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from . import USER, PASSWORD, DBNAME


SQLALCHEMY_DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@localhost/{DBNAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
