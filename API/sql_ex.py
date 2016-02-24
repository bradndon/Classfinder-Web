#Copyright (C) Brandon Fox 2016

import os
import sys
import datetime
import json
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, DateTime, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Apikey(Base):
    __tablename__ = 'apikeys'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    apikey = Column(String(36), unique=True)
    email = Column(String(75), nullable=False, unique=True)


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('mysql+pymysql://root:7rebrahuxetrewuc@localhost/apidb?charset=utf8&use_unicode=0', pool_recycle=3600)

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
