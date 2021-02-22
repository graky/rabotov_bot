from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class form(Base):
    __tablename__ = 'form'
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer)
    vacancy = Column(String)
    duties =  Column(String)
    requirements = Column(String)
    conditions =   Column(String)
    pay_level =    Column(String)
    salary =       Column(Integer)
    nickname =     Column(String)
    just_finished =Column(Boolean)
    active = Column(Boolean)
    #editing = Column(Boolean)


engine = create_engine('sqlite:///forms.db')
Base.metadata.create_all(engine)
