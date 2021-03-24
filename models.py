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
    just_finished =Column(Boolean, default=False)
    active = Column(Boolean)
    recruiter_count = Column(Integer, default=0)
    #editing = Column(Boolean)

class workers(Base):
    __tablename__ = 'worker'
    id = Column(Integer, primary_key = True)
    closed_tasks = Column(Integer, default=0)
    level = Column(String, default='LIGHT')
    user_id = Column(Integer)
    educ_lvl = Column(Integer, default=0)
    list_of_forms = Column(String, default='')
    test_stage = Column(Integer, default=0)
    first_test_1  = Column(Boolean, default=False)
    first_test_2  = Column(Boolean, default=False)
    first_test_3  = Column(Boolean, default=False)
    first_test_4  = Column(Boolean, default=False)
    first_test_5  = Column(Boolean, default=False)
    first_test_6  = Column(Boolean, default=False)
    second_test_1 = Column(Boolean, default=False)
    second_test_2 = Column(Boolean, default=False)
    second_test_3 = Column(Boolean, default=False)
    second_test_4 = Column(Boolean, default=False)
    third_test_1 = Column(Boolean, default=False)
    third_test_2 = Column(Boolean, default=False)
    third_test_3 = Column(Boolean, default=False)
    third_test_4 = Column(Boolean, default=False)

engine = create_engine(r'sqlite:///db/forms.db')
Base.metadata.create_all(engine)
