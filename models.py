from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import random
import os
from os import environ

Base = declarative_base()

user = os.environ['SQL_USER']
password = os.environ['SQL_PASSWORD']
db_name = os.environ['SQL_DATABASE']
db_host = os.environ['SQL_HOST']
"""
user = "bot_admin"
password = "bot_admin"
db_name = "rabotov_bot"
db_host = "localhost"
"""
engine = create_engine('postgresql+psycopg2://%s:%s@%s/%s' % (str(user), str(password), str(db_host), str(db_name)))
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
DBSession.bind = engine
session = DBSession()


class Category(Base):
    __tablename__ = "category"
    category_id = Column(Integer, primary_key=True)
    name = Column(String)
    vacancy = relationship("Vacancy")


class User(Base):
    __tablename__ = "user"
    telegram_id = Column(Integer, primary_key=True)
    employer = relationship("Employer", back_populates="user")
    recruiter = relationship("Recruiter", back_populates="user")
    feedbacker = relationship("Feedback", back_populates="user")
    answer = relationship("Answer", back_populates="user")
    superuser = Column(Boolean, default=False)
    first_name = Column(String)
    last_name = Column(String)


class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True)
    feedback_message = Column(String)
    user_id = Column(Integer, ForeignKey('user.telegram_id'))
    user = relationship("User", back_populates="feedbacker")


class Employer(Base):
    __tablename__ = 'employer'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.telegram_id'))
    user = relationship("User", back_populates="employer")
    vacancies = relationship("Vacancy")


class Vacancy(Base):
    __tablename__ = 'vacancy'
    id = Column(Integer, primary_key=True)
    employer_id = Column(Integer, ForeignKey('employer.id'))
    employer = relationship("Employer", back_populates="vacancies")
    city = Column(String)
    company = Column(String)
    category_id = Column(Integer, ForeignKey('category.category_id'))
    website = Column(String)
    name = Column(String)
    duties = Column(String)
    requirements = Column(String)
    conditions = Column(String)
    pay_level = Column(String)
    numb_level = Column(Integer)
    salary = Column(Integer)
    finite_state = Column(Integer, default=0)
    active = Column(Boolean, default=False)
    inwork = relationship("InWork", back_populates="vacancy")
    candidate = relationship("Candidate", back_populates="vacancy")

    def __repr__(self):
        form = """
Заявка на подбор персонала : {0}

Категория: {9}

Компания: {1}

Вебсайт: {2}

Город: {10}

Наименование вакансии: {3}

Обязанности: {4}

Требования: {5}

Условия: {6}

Уровень вознаграждения за подбор: {7}

Сумма вознаграждения: {8}
"""
        form = form.format(
            self.id,
            self.company,
            self.website,
            self.name,
            self.duties,
            self.requirements,
            self.conditions,
            self.pay_level,
            self.salary,
            session.query(Category.name).filter_by(category_id=self.category_id).first()[0],
            self.city
        )
        return form


class Recruiter(Base):
    __tablename__ = 'recruiter'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.telegram_id'))
    user = relationship("User", back_populates="recruiter")
    level = Column(String)
    level_numb = Column(Integer)
    resume = relationship("Resume", back_populates="recruiter")
    finished_educ = Column(Boolean, default=False)
    inwork = relationship("InWork", back_populates="recruiter")
    candidate = relationship("Candidate", back_populates="recruiter")
    closed_vacancies = Column(Integer, default=0)


class Resume(Base):
    __tablename__ = "resume"
    id = Column(Integer, primary_key=True)
    recruiter_id = Column(Integer, ForeignKey('recruiter.id'))
    recruiter = relationship("Recruiter", back_populates="resume")
    fio = Column(String)
    years = Column(String)
    specialization = Column(String)
    tools = Column(String)
    difficulties = Column(String)
    invitation = Column(String)
    letter = Column(String)
    refusal = Column(String)
    reviewed = Column(Boolean, default=False)

    def __repr__(self):
        resume = """
- Ваше ФИО\n
{0}\n
- Сколько лет вы в подборе\n
{1}\n
- В какой области вы специализируетесь\n
{2}\n
- Какими инструментами пользуетесь при подборе\n
{3}\n
- С какими трудностями сталкивались при подборе\n
{4}\n
- Напишите краткое приглашение соискателю на вакансию\n
{5}\n
- Вы не можете долго закрыть заявку и понимаете, что заработная плата не в рынке. Напишите письмо работодателю с предложением откорректировать заявку.\n
{6}\n
- Не все соискатели подошли. Как вы откажете соискателю\n
{7} \n
"""
        resume = resume.format(
            self.fio,
            self.years,
            self.specialization,
            self.tools,
            self.difficulties,
            self.invitation,
            self.letter,
            self.refusal,
        )
        return resume


class Question(Base):
    __tablename__ = "question"
    poll_id = Column(String, primary_key=True)
    question = Column(String)


class Answer(Base):
    __tablename__ = "answer"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.telegram_id'))
    user = relationship("User", back_populates="answer")
    score = Column(Integer, default=0)


class InWork(Base):
    __tablename__ = "inwork"
    id = Column(Integer, primary_key=True)
    recruiter_id = Column(Integer, ForeignKey('recruiter.id'))
    recruiter = relationship("Recruiter", back_populates="inwork")
    vacancy_id = Column(Integer, ForeignKey('vacancy.id'))
    vacancy = relationship("Vacancy", back_populates="inwork")


class Candidate(Base):
    __tablename__ = "candidate"
    id = Column(Integer, primary_key=True)
    recruiter_id = Column(Integer, ForeignKey('recruiter.id'))
    recruiter = relationship("Recruiter", back_populates="candidate")
    vacancy_id = Column(Integer, ForeignKey('vacancy.id'))
    vacancy = relationship("Vacancy", back_populates="candidate")
    name = Column(String)
    interview = Column(String)
    video = Column(String)
    meeting = Column(String)
    mark = Column(String)
    resume_text = Column(String)
    resume_file = Column(String)
    taken_refused = Column(String, default="")
    finite_state = Column(Integer, default=0)

    def __repr__(self):
        candidate_string = """
Имя кандидата: {0}
Итоги интервью: {1}
Итоги видеоконференции: {2}
Итоги встречи: {3}
Оценка кандидата на соответствие предлагаемой должности: {4}
Резюме: {5}
        """
        candidate_string = candidate_string.format(
            self.name,
            self.interview,
            self.video,
            self.meeting,
            self.mark,
            self.resume_text
        )
        return candidate_string


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).one_or_none()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


Base.metadata.create_all(engine)
Base.metadata.bind = engine

"""Создание категорий"""
categories = ['Информационные технологии',
              'Строительство, недвижимость',
              'Продажи',
              'Медицина,',
              'Логистика',
              'Производство',
              'Сельское хозяйство',
              'Закупки',
              'Страхование',
              'Юристы',
              'Маркетинг',
              'Бухгалтерия',
              'Административный персонал',
              'Искусство, развлечения',
              'Высший менеджмент',
              'Автомобильный бизнес',
              'Безопасность',
              'Добыча сырья',
              'Туризм, гостиницы, рестораны',
              'Спорт, фитнес',
              'Индустрия красоты',
              'Рабочий персонал',
              'Домашний персонал',
              'Инсталляция и сервис',
              'Консультирование',
              'Наука, образование',
              'Иное']


def create_vacancy():
    if not session.query(Category).first():
        for category in categories:
            session.add(Category(name=category))
            session.commit()
            session.close()
