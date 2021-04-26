from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import random
import os
from os import environ

Base = declarative_base()


class form(Base):
    __tablename__ = 'form'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    vacancy = Column(String)
    duties = Column(String)
    requirements = Column(String)
    conditions = Column(String)
    pay_level = Column(String)
    salary = Column(Integer)
    nickname = Column(String)
    just_finished = Column(Boolean, default=False)
    active = Column(Boolean)
    recruiter_count = Column(Integer, default=0)
    done = Column(Boolean, default=False)
    taken_in_work = Column(Boolean, default=False)
    # editing = Column(Boolean)


class workers(Base):
    __tablename__ = 'worker'
    id = Column(Integer, primary_key=True)
    closed_tasks = Column(Integer, default=0)
    level = Column(String, default='LIGHT')
    user_id = Column(Integer)
    educ_lvl = Column(Integer, default=0)
    list_of_forms = Column(String, default='')
    test_stage = Column(Integer, default=0)
    first_test_1 = Column(Boolean, default=False)
    first_test_2 = Column(Boolean, default=False)
    first_test_3 = Column(Boolean, default=False)
    first_test_4 = Column(Boolean, default=False)
    first_test_5 = Column(Boolean, default=False)
    first_test_6 = Column(Boolean, default=False)
    second_test_1 = Column(Boolean, default=False)
    second_test_2 = Column(Boolean, default=False)
    second_test_3 = Column(Boolean, default=False)
    second_test_4 = Column(Boolean, default=False)
    third_test_1 = Column(Boolean, default=False)
    third_test_2 = Column(Boolean, default=False)
    third_test_3 = Column(Boolean, default=False)
    third_test_4 = Column(Boolean, default=False)
    done = Column(Boolean, default=False)
class candidates(Base):
    __tablename__ = 'candidates'
    id = Column(Integer, primary_key=True)
    id_form = Column(Integer)
    worker_id = Column(Integer)
    name = Column(String)
    interview = Column(String)
    video_review = Column(String)
    meeting_result = Column(String)
    mark = Column(String, default='wait')
    contact = Column(String)
    exit_proof = Column(Boolean, default=False)



'''
user = 'bot_admin'
password = 'bot_admin'
db_name = 'rabotov_bot'
db_host = 'db'
'''
'''user = os.environ.get('SQL_USER')
password = os.environ.get('SQL_PASSWORD')
db_name = os.environ.get('SQL_DATABASE')
db_host = os.environ.get('SQL_HOST')
engine = create_engine('postgresql+psycopg2://%s:%s@%s/%s' % (str(user), str(password), str(db_host), str(db_name)))
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
DBSession.bind = engine
session = DBSession()
'''
engine = create_engine(r'sqlite:///forms.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
DBSession.bind = engine
session = DBSession()

pay_level_list = {'LIGHT':[0, 0], 'MEDIUM':[1, 5000], 'HARD':[5000,10000], 'PRO':[10000, 100000]}
def get_nickname(numb):
    nick = '@nickname' + str(numb)
    phone =  '+7' + str(random.randint(9000000000, 9999999999))
    return random.choice([nick, phone])
for i in range(30):
    key = random.choice(list(pay_level_list.keys()))
    value = random.randint(pay_level_list[key][0], pay_level_list[key][1])
    session.add(form(user_id =i, vacancy = 'Тестовая вакансия {0}'.format(str(i)), duties ='Выполнять работу {0}'.format(str(i)), requirements ='необходимые требования{0}'.format(str(i)), conditions = 'необходимые условия {0}'.format(str(i)),  pay_level =key, salary = value, nickname = get_nickname(i), active = True))
    session.commit()
    session.close()
print('done')