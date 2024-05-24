from sqlalchemy import create_engine, Column, Integer, String,MetaData,Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

import os
from dotenv import load_dotenv

load_dotenv()

password = os.getenv('password')
user = os.getenv('user')

Base = declarative_base()

class QrCode(Base):
    __tablename__ = 'qr_code'
    ID = Column(Integer,primary_key=True,autoincrement=True)
    Link = Column(String(255))
    read = Column(Boolean,default=False)
    uuid = Column(String(225))
    
engine = create_engine(f'postgresql://{user}:{password}@localhost:5432/onlineTickets')
# engine = create_engine(f'postgresql://{user}:{password}@localhost:5432/test_db_b7vz',connect_args={'sslmode': 'require'})

# Base.metadata.drop_all(engine)
# Create a metadata object
metadata = MetaData()


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
