import logging
import models
import os
from time import sleep
from models import (User,
                    Employer,
                    Vacancy,
                    Recruiter,
                    Resume,
                    Question,
                    Answer,
                    InWork,
                    Category,
                    Candidate,
                    Feedback,
                    MessageFromAdmin)
from aiogram.utils.exceptions import FileIsTooBig
from models import get_or_create
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType, InputFile

API_TOKEN = os.environ['TOKEN']
ADMIN_KEY = "d873ec68-2729-4c5d-9753-39540c011c75"
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

models.create_vacancy()
session = models.DBSession()

profile_board = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons1 = ["РАБОТОДАТЕЛЬ", "РЕКРУТЕР"]
profile_board.add(*buttons1)
create_vacancy_board = types.ReplyKeyboardMarkup(resize_keyboard=True)
create_vacancy_board.add("ЗАПОЛНИТЬ ЗАЯВКУ")
pay_level_list = ['LIGHT', 'MEDIUM', 'HARD', 'PRO']
pay_level_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
pay_level_keyboard.add(*pay_level_list)
pay_level_dict = {
    'LIGHT': [[1, 500], 1],
    'MEDIUM': [[501, 5000], 2],
    'HARD': [[5001, 10000], 3],
    'PRO': [[10001, 10000000], 4]
}
keyboard_activate = types.ReplyKeyboardMarkup(resize_keyboard=True)
activate_buttons = ["Запустить подбор", "Сохранить в черновик", "Отменить"]
keyboard_activate.add(*activate_buttons)
level_recruiter_board = types.ReplyKeyboardMarkup(resize_keyboard=True)
level_recruiter_board.add("УРОВЕНЬ LIGHT", "ОТПРАВИТЬ РЕЗЮМЕ")
next_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
next_button.add("ДАЛЕЕ")
star_test_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
star_test_button.add("НАЧАТЬ ТЕСТ")
finish_test_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
finish_test_button.add("ЗАВЕРШИТЬ ТЕСТ")
not_completed_button = types.ReplyKeyboardMarkup(resize_keyboard=True)
not_completed_button.add("Не проводилось")
mark_of_candidate_buttons = types.ReplyKeyboardMarkup(resize_keyboard=False, row_width=1)
mark_of_candidate_list = [
    "Не соответствует, но очень хочет",
    "Есть понимание и способности к обучению",
    "Полностью соответствует, опыт и квалификация согласно заявке"
]
mark_of_candidate_buttons.add(*mark_of_candidate_list)
source_buttons = types.ReplyKeyboardMarkup(resize_keyboard=False, row_width=3)
source_list = [
    "HH", "Superjob", "Avito", "Instagram", "HRtime", "HRspace", "WhatsApp"
]
source_buttons.add(*source_list)
question1 = ["Я буду искать кандидатов",
             [
                 "Telegram",
                 "Соц сети, работные сайты",
                 "На рынке",
                 "Сайты знакомств",
                 "Дам объявление",
                 "Переманю"
             ],
             False]

question2 = ["Прежде, чем отправить кандидата на рассмотрение работодателю, я",
             [
                 "Проведу телефонное интервью",
                 "Созвонюсь по видео связи",
                 "Встречусь вживую при необходимости",
                 "Только пообщаюсь по переписке",

             ],
             False,
             ]

question3 = ["Для того, чтобы начать зарабатывать на закрытии заявок мне нужно",
             [
                 "Быть ИП",
                 "Иметь юр лицо",
                 "Открыть самозанятость",
                 "Быть фрилансером",

             ],
             False,
             ]


def get_vacancy_button(vacancy):
    vacancy_id = vacancy.id
    vacancy_button = types.InlineKeyboardMarkup()
    vacancy_button.add(types.InlineKeyboardButton("Показать вакансию",
                                                callback_data="show_vacancy " + f"{vacancy_id}"))
    return vacancy_button


async def admin_set_level(admin_id, lvl, numb_lvl, recruiter_id):
    recruiter = session.query(Recruiter).filter_by(user_id=recruiter_id).first()
    resume = session.query(Resume).filter_by(recruiter_id=recruiter.id).first()
    if not resume.reviewed:
        resume.reviewed = True
        recruiter.level = lvl
        recruiter.level_numb = numb_lvl
        recruiter.finished_educ = True
        session.commit()
        session.close()
        await bot.send_message(recruiter_id, f"Поздравляем, вам назначен уровень {lvl}!")
        await bot.send_message(admin_id, "Уровень рекрутеру назначен!")
    else:
        await bot.send_message(admin_id, "Резюме рекрутера уже было рассмотрено")


async def set_light_level(user_id):
    await bot.send_message(user_id, "Ваш уровень LIGHT. Давайте пройдём небольшое обучение.", reply_markup=next_button)


async def send_candidate_to_employer(candidate_id):
    sleep(3)
    candidate = session.query(Candidate).get(candidate_id)
    vacancy = candidate.vacancy
    employer = vacancy.employer
    await bot.send_message(employer.user.telegram_id, "На вашу вакансию откликнулись.", reply_markup=get_vacancy_button(vacancy))
    candidate_buttons = types.InlineKeyboardMarkup()
    candidate_buttons.add(
        types.InlineKeyboardButton("Отклонить",
                                   callback_data="cand_ref " + f"{candidate_id}"),
        types.InlineKeyboardButton("Трудоустроить",
                                   callback_data="cand_empl " + f"{candidate_id}"),
        types.InlineKeyboardButton("Собеседовать",
                                   callback_data="cand_inter " + f"{candidate_id}"),
    )
    await bot.send_message(employer.user.telegram_id, f"Кандидат:"
                                                      f"{candidate}", reply_markup=candidate_buttons)
    if candidate.resume_file:
        file = InputFile(f"resume/{candidate.resume_file}")
        await bot.send_message(employer.user.telegram_id, "Файл с резюме:")
        await bot.send_document(employer.user.telegram_id, file)


class SetSource(StatesGroup):
    source = State()


class AdminState(StatesGroup):
    loign = State()


class AdminForUsers(StatesGroup):
    for_all = State()
    for_all_employers = State()
    for_all_recruters = State()
    for_recruters_no_educ = State()
    for_employers_without_vacancy = State()


class FeedbackState(StatesGroup):
    feedback = State()


class EmployerState(StatesGroup):
    category = State()
    company = State()
    website = State()
    city = State()
    name = State()
    duties = State()
    requirements = State()
    conditions = State()
    level = State()
    salary = State()
    activate = State()


class RecruiterRegistry(StatesGroup):
    register = State()
    fio = State()
    years = State()
    specialization = State()
    tools = State()
    difficulties = State()
    invitation = State()
    letter = State()
    refusal = State()
    text1 = State()
    text2 = State()
    text3 = State()
    text4 = State()
    text5 = State()
    test1 = State()
    test2 = State()
    test3 = State()
    finish_test = State()


class CandidateRegister(StatesGroup):
    name = State()
    interview = State()
    video = State()
    meeting = State()
    mark = State()
    resume = State()


class SendContact(StatesGroup):
    send_contact = State()


class SendLink(StatesGroup):
    send_link = State()


@dp.message_handler(commands=['feedback'])
async def become_admin(message: types.Message):
    await FeedbackState.feedback.set()
    await message.answer("Опишите в одном сообщении вашу проблему или предложение")


@dp.message_handler(commands=['get_open_resume'])
async def for_all(message: types.Message):
    if session.query(User).filter_by(telegram_id=message.from_user.id).first().superuser:
        resumes = session.query(Resume).filter_by(reviewed=False).all()

        for resume in resumes:
            user_id = resume.recruiter.user_id
            admin_buttons = types.InlineKeyboardMarkup()
            admin_buttons.add(
                types.InlineKeyboardButton("LIGHT",
                                           callback_data="set_lvl " + "LIGHT " + "1 " + str(user_id)),
                types.InlineKeyboardButton("MEDIUM",
                                           callback_data="set_lvl " + "MEDIUM " + "2 " + str(user_id)),
                types.InlineKeyboardButton("HARD",
                                           callback_data="set_lvl " + "HARD " + "3 " + str(user_id)),
                types.InlineKeyboardButton("PRO", callback_data="set_lvl " + "PRO " + "4 " + str(user_id)),
            )
            await message.answer("Резюме от рекрутера для рассмотрения")
            await message.answer(resume)
            await message.answer("Назначьте уровень рекрутеру", reply_markup=admin_buttons)
    else:
        await message.answer("У вас недостаточно прав для данного действия")


@dp.message_handler(commands=['message_for_all'])
async def for_all(message: types.Message):
    if session.query(User).filter_by(telegram_id=message.from_user.id).first().superuser:
        await AdminForUsers.for_all.set()
        await message.answer("Введите сообщение")
    else:
        await message.answer("У вас недостаточно прав для данного действия")


@dp.message_handler(state=AdminForUsers.for_all)
async def all_message(message: types.Message, state: FSMContext):
    users = session.query(User).all()
    msg = message.text
    for user in users:
        try:
            await bot.send_message(user.telegram_id, msg)
        except Exception as err:
            user.blocked = True
            session.commit()
    session.add(MessageFromAdmin(msg_type="for_all",
                                 msg_text=msg,
                                 from_user=message.from_user.id))
    session.commit()
    session.close()
    await message.answer("Успешно отправлено")
    await state.finish()


@dp.message_handler(commands=['message_for_recruters'])
async def for_all_recruters(message: types.Message):
    if session.query(User).filter_by(telegram_id=message.from_user.id).first().superuser:
        await AdminForUsers.for_all_recruters.set()
        await message.answer("Введите сообщение")
    else:
        await message.answer("У вас недостаточно прав для данного действия")


@dp.message_handler(state=AdminForUsers.for_all_recruters)
async def recruters_message(message: types.Message, state: FSMContext):
    users = session.query(Recruiter).all()
    msg = message.text
    for user in users:
        try:
            await bot.send_message(user.user_id, msg)
        except Exception as err:
            user.blocked = True
            session.commit()
    session.add(MessageFromAdmin(msg_type="for_all_recruters",
                                 msg_text=msg,
                                 from_user=message.from_user.id))
    session.commit()
    session.close()
    await message.answer("Успешно отправлено")
    await state.finish()


@dp.message_handler(commands=['message_for_recruters_no_educ'])
async def recruters_no_educ(message: types.Message):
    if session.query(User).filter_by(telegram_id=message.from_user.id).first().superuser:
        await AdminForUsers.for_recruters_no_educ.set()
        await message.answer("Введите сообщение")
    else:
        await message.answer("У вас недостаточно прав для данного действия")


@dp.message_handler(state=AdminForUsers.for_recruters_no_educ)
async def recruters_no_educ_message(message: types.Message, state: FSMContext):
    users = session.query(Recruiter).filter_by(finished_educ=False).all()
    msg = message.text
    for user in users:
        try:
            await bot.send_message(user.user_id, msg)
        except Exception as err:
            user.blocked = True
            session.commit()
    session.add(MessageFromAdmin(msg_type="for_recruters_no_educ",
                                 msg_text=msg,
                                 from_user=message.from_user.id))
    session.commit()
    session.close()
    await message.answer("Успешно отправлено")
    await state.finish()


@dp.message_handler(commands=['message_for_employers'])
async def for_all_employers(message: types.Message):
    if session.query(User).filter_by(telegram_id=message.from_user.id).first().superuser:
        await AdminForUsers.for_all_employers.set()
        await message.answer("Введите сообщение")
    else:
        await message.answer("У вас недостаточно прав для данного действия")


@dp.message_handler(state=AdminForUsers.for_all_employers)
async def employers_message(message: types.Message, state: FSMContext):
    users = session.query(Employer).all()
    msg = message.text
    for user in users:
        try:
            await bot.send_message(user.user_id, msg)
        except Exception as err:
            user.blocked = True
            session.commit()
    session.add(MessageFromAdmin(msg_type="for_all_employers",
                                 msg_text=msg,
                                 from_user=message.from_user.id))
    session.commit()
    session.close()
    await message.answer("Успешно отправлено")
    await state.finish()


@dp.message_handler(commands=['message_for_employers_without_vacancy'])
async def employers_without_vacancy(message: types.Message):
    if session.query(User).filter_by(telegram_id=message.from_user.id).first().superuser:
        await AdminForUsers.for_employers_without_vacancy.set()
        await message.answer("Введите сообщение")
    else:
        await message.answer("У вас недостаточно прав для данного действия")


@dp.message_handler(state=AdminForUsers.for_employers_without_vacancy)
async def employers_without_vacancy_message(message: types.Message, state: FSMContext):
    vacancy_list = session.query(Vacancy.employer_id).all()
    vacancy_list = list(set(vacancy_list))
    for i in range(len(vacancy_list)):
        vacancy_list[i] = vacancy_list[i][0]
    employer_list = session.query(Employer).filter(Employer.id.not_in(vacancy_list)).all()
    msg = message.text
    for employer in employer_list:
        try:
            await bot.send_message(employer.user_id, msg)
        except Exception as err:
            user = session.query(User).filter_by(telegram_id=employer.user_id)
            user.blocked = True
            session.commit()
    session.add(MessageFromAdmin(msg_type="for_employers_without_vacancy",
                                 msg_text=msg,
                                 from_user=message.from_user.id))
    session.commit()
    session.close()
    await message.answer("Успешно отправлено")
    await state.finish()


@dp.message_handler(commands=['admin'])
async def feedback(message: types.Message):
    await AdminState.loign.set()
    await message.answer("Введите ключ, чтобы получить возможность рассмотрения заявки")


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.answer(
        """Доступные команды:
        /get_vacancies - список вакансий доступных рекрутеру
        /in_work - список вакансий в разработке у рекрутера
        /my_vacancies - список заявок запущенных работодателем
        /drafts - список заявок сохраненных в черновики
        /feedback - отправить отзыв об ошибке или предложение о доработке бота
    """)
    if session.query(User).filter_by(telegram_id=message.from_user.id).first().superuser:
        await message.answer(
            """Команды для администраторов бота:
            /message_for_all - Отправить сообщение всем пользователям
            /message_for_recruters - Отправить сообщение всем рекрутерам
            /message_for_employers - Отправить сообщение всем работодателям
            /message_for_recruters_no_educ - Отправить сообщение всем рекрутерам не прошедшим обучение
            /message_for_employers_without_vacancy - Отправить сообщение всем работодателям без вакансий
            /get_open_resume - не рассмотренные резюме рекрутеров
        """)


@dp.message_handler(commands=['my_vacancies'])
async def my_vacancies(message: types.Message):
    employer = session.query(Employer).filter_by(user_id=message.from_user.id).first()
    employer_vacancies = session.query(Vacancy).filter_by(employer=employer, active=True).all()
    if len(employer_vacancies) > 0:
        for vacancy in employer_vacancies:
            vacancy_buttons = types.InlineKeyboardMarkup()
            vacancy_buttons.add(
                types.InlineKeyboardButton("Удалить вакансию",
                                           callback_data="del_vac " + f"{vacancy.id} " + f"{message.from_user.id}"),
                types.InlineKeyboardButton("Убрать в черновики",
                                           callback_data="draft_vac " + f"{vacancy.id} " + f"{message.from_user.id}"),
            )
            await message.answer(vacancy, reply_markup=vacancy_buttons)
    else:
        await message.answer("""Вы не еще не запустили ни одной заявки""")


@dp.message_handler(commands=['drafts'])
async def drafts(message: types.Message):
    employer = session.query(Employer).filter_by(user_id=message.from_user.id).first()
    drafts_list = session.query(Vacancy).filter(Vacancy.employer == employer, Vacancy.active == False,
                                                Vacancy.category_id is not None).all()
    if len(drafts_list) > 0:
        for draft in drafts_list:
            draft_buttons = types.InlineKeyboardMarkup()
            draft_buttons.add(
                types.InlineKeyboardButton("Удалить черновик",
                                           callback_data="del_vac " + f"{draft.id} " + f"{message.from_user.id}"),
                types.InlineKeyboardButton("Запустить подбор",
                                           callback_data="draft_vac " + f"{draft.id} " + f"{message.from_user.id}"),
            )
            await message.answer(draft, reply_markup=draft_buttons)
    else:
        await message.answer("""Вы не еще не запустили ни одной заявки""")


@dp.message_handler(commands=['get_vacancies'])
async def get_vacancies(message: types.Message):
    if recruiter := session.query(Recruiter).filter_by(user_id=message.from_user.id).first():
        if recruiter.finished_educ:
            vacancy_buttons = types.InlineKeyboardMarkup()
            vacancy_buttons.add(
                types.InlineKeyboardButton("ВСЕ ВАКАНСИИ",
                                           callback_data="vacancies " + f"{recruiter.id} " + "all"),
                types.InlineKeyboardButton("ВЫБРАТЬ КАТЕГОРИЮ",
                                           callback_data="categories " + f"{recruiter.id}")
            )
            await message.answer("Вы хотите ", reply_markup=vacancy_buttons)
        else:
            await message.answer("""Вы ещё не прошли обучение. 
            Чтобы пройти обучение, воспользуйтесь командой /start далее выберите РЕКРУТЕР и следуйте инструкциям.""")
    else:
        await message.answer("""У вас ещё  нет профиля рекрутера. 
        Чтобы создать профиль рекрутера, воспользуйтесь командой /start далее выберите РЕКРУТЕР и следуйте инструкциям.""")


@dp.message_handler(commands=['in_work'])
async def in_work(message: types.Message):
    if recruiter := session.query(Recruiter).filter_by(user_id=message.from_user.id).first():
        if recruiter.finished_educ:
            vacancies_in_work = session.query(InWork).filter(
                InWork.recruiter_id == recruiter.id
            ).all()
            if len(vacancies_in_work) > 0:
                for vacancy_in_work in vacancies_in_work:
                    vacancy = session.query(Vacancy).get(vacancy_in_work.vacancy_id)
                    recruiter_buttons = types.InlineKeyboardMarkup()
                    recruiter_buttons.add(
                        types.InlineKeyboardButton("ПРЕДЛОЖИТЬ КАНДИДАТА",
                                                   callback_data="add_cand " + f"{vacancy.id} " + f"{recruiter.id}"),
                    )
                    await message.answer(vacancy, reply_markup=recruiter_buttons)
            else:
                await message.answer("""Вы еще не взяли ни одной заявки в работу, воспользуйтесь командой 
                /get_vacancies чтобы получить список доступных заявок.""")
        else:
            await message.answer("""Вы ещё не прошли обучение. 
Чтобы пройти обучение, воспользуйтесь командой /start далее выберите РЕКРУТЕР и следуйте инструкциям.""")
    else:
        await message.answer("""У вас ещё  нет профиля рекрутера. 
Чтобы создать профиль рекрутера, воспользуйтесь командой /start далее выберите РЕКРУТЕР и следуйте инструкциям.""")


@dp.message_handler(state=AdminState.loign)
async def login(message: types.Message, state: FSMContext):
    if message.text == ADMIN_KEY:
        user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
        user.superuser = True
        session.commit()
        session.close()
        await message.answer("""Вы получили права модератора. 
Вам будут поступать резюме рекрутеров для рассмотрения уровня""")
    else:
        await message.answer("Неверный пароль")
    await state.finish()


@dp.message_handler(state=FeedbackState.feedback)
async def feedback(message: types.Message, state: FSMContext):
    session.add(Feedback(user_id=message.from_user.id, feedback_message=message.text))
    session.commit()
    session.close()
    for admin in session.query(User).filter_by(superuser=True):
        await bot.send_message(admin.telegram_id, message.text)
    await message.answer("Ваш отзыв будет обязательно рассмотрен")
    await state.finish()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    if not session.query(User).filter_by(telegram_id=message.from_user.id).first():
        session.add(User(telegram_id=message.from_user.id,
                         first_name=message.from_user.first_name,
                         last_name=message.from_user.last_name,
                         username=message.from_user.username))
        session.commit()
        session.close()

    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    if not user.username:
        user.username = message.from_user.username
    if not user.first_name:
        user.first_name = message.from_user.first_name
    if not user.last_name:
        user.last_name = message.from_user.last_name
    if not user.source:
        await SetSource.source.set()
        await message.answer(
            "Пожалуйста, укажите откуда вы узнали о нашем боте. Выберите вариант из предложенных или введите свой.",
            reply_markup=source_buttons)
    else:
        await message.answer("Чтобы посмотреть доступные команды введите /help. Выберите категорию:",
                             reply_markup=profile_board
                             )
    session.commit()
    session.close()


@dp.message_handler(state=SetSource.source)
async def set_sourse(message: types.Message, state: FSMContext):
    user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
    user.source = message.text
    session.commit()
    session.close()
    await state.finish()
    await message.answer("Спасибо за указанную информацию!")
    await message.answer("Чтобы посмотреть доступные команды введите /help. Выберите категорию:",
                         reply_markup=profile_board
                         )


# ОБРАБОТКА ЗАПОЛНЕНИЯ ЗАЯВКИ


@dp.message_handler(Text(equals="РАБОТОДАТЕЛЬ"))
async def employer_start(message: types.Message):
    if not session.query(Employer).filter_by(user_id=message.from_user.id).first():
        user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
        session.add(Employer(user=user))
        session.commit()
        session.close()
    text = """Здравствуйте, {0}. 
Не тратьте время на поиск сотрудников. Делегируйте это мне! 
Со мной работает {1} рекрутеров со всей страны!
Внимательно заполните форму заявки, выберите уровень вознаграждения за подбор и мотивируйте рекрутеров заняться именно вашей заявкой.""".format(
        message.from_user.full_name,
        300
        # len(session.query(Employer).all())
    )
    await message.answer(text, reply_markup=create_vacancy_board)


@dp.message_handler(Text(equals="ЗАПОЛНИТЬ ЗАЯВКУ"))
async def vacancy_start(message: types.Message):
    if employer := session.query(Employer).filter_by(user_id=message.from_user.id).first():
        session.add(Vacancy(employer=employer, finite_state=1))
        session.commit()
        text = "Выберите категорию"
        await message.answer(text)
        categories = session.query(Category).all()
        for category in categories:
            category_buttons = types.InlineKeyboardMarkup()
            category_buttons.add(
                types.InlineKeyboardButton("ВЫБРАТЬ КАТЕГОРИЮ",
                                           callback_data="set_vacancy " + f"{message.from_user.id} " + f"{category.category_id}")
            )
            await bot.send_message(message.from_user.id, category.name, reply_markup=category_buttons)


@dp.message_handler(state=EmployerState.company)
async def set_company(message: types.Message, state: FSMContext):
    employer = session.query(Employer).filter_by(user_id=message.from_user.id).first()
    vacancy = session.query(Vacancy).filter_by(employer=employer, finite_state=2)[-1]
    vacancy.company = message.text
    vacancy.finite_state = 3
    session.commit()
    session.close()
    await EmployerState.next()
    await message.answer("Введите сайт компании")


@dp.message_handler(state=EmployerState.website)
async def set_website(message: types.Message, state: FSMContext):
    employer = session.query(Employer).filter_by(user_id=message.from_user.id).first()
    vacancy = session.query(Vacancy).filter_by(employer=employer, finite_state=3)[-1]
    vacancy.website = message.text
    vacancy.finite_state = 4
    session.commit()
    session.close()
    await EmployerState.next()
    await message.answer("Введите город")


@dp.message_handler(state=EmployerState.city)
async def set_city(message: types.Message, state: FSMContext):
    employer = session.query(Employer).filter_by(user_id=message.from_user.id).first()
    vacancy = session.query(Vacancy).filter_by(employer=employer, finite_state=4)[-1]
    vacancy.city = message.text
    vacancy.finite_state = 5
    session.commit()
    session.close()
    await EmployerState.next()
    await message.answer("Введите наименование вакантной должности")


@dp.message_handler(state=EmployerState.name)
async def set_name(message: types.Message, state: FSMContext):
    employer = session.query(Employer).filter_by(user_id=message.from_user.id).first()
    vacancy = session.query(Vacancy).filter_by(employer=employer, finite_state=5)[-1]
    vacancy.name = message.text
    vacancy.finite_state = 6
    session.commit()
    session.close()
    await EmployerState.next()
    await message.answer("Введите обязанности будущего сотрудника")


@dp.message_handler(state=EmployerState.duties)
async def set_duties(message: types.Message, state: FSMContext):
    employer = session.query(Employer).filter_by(user_id=message.from_user.id).first()
    vacancy = session.query(Vacancy).filter_by(employer=employer, finite_state=6)[-1]
    vacancy.duties = message.text
    vacancy.finite_state = 7
    session.commit()
    session.close()
    await EmployerState.next()
    await message.answer("""Введите требования для будущего сотрудника
- опыт работы:

- образование:

- навыки и умения:

- иное:""")


@dp.message_handler(state=EmployerState.requirements)
async def set_requirements(message: types.Message, state: FSMContext):
    employer = session.query(Employer).filter_by(user_id=message.from_user.id).first()
    vacancy = session.query(Vacancy).filter_by(employer=employer, finite_state=7)[-1]
    vacancy.requirements = message.text
    vacancy.finite_state = 8
    session.commit()
    session.close()
    await EmployerState.next()
    await message.answer("""Какие условия работы вы готовы предложить будущему сотруднику
- график работы:

- заработная плата:

- характер работы:

- иное:""")


@dp.message_handler(state=EmployerState.conditions)
async def set_conditions(message: types.Message, state: FSMContext):
    employer = session.query(Employer).filter_by(user_id=message.from_user.id).first()
    vacancy = session.query(Vacancy).filter_by(employer=employer, finite_state=8)[-1]
    vacancy.conditions = message.text
    vacancy.finite_state = 9
    session.commit()
    session.close()
    await EmployerState.next()
    await message.answer("""Выберите уровень вознаграждения рекрутеру за подбор. От суммы вознаграждения зависит, какого уровня рекрутеры увидят вашу заявку.

LIGHT (заявки до 500 рублей)

MEDIUM (от 501 до 5000 руб.)

HARD (от 5001 до 10000 руб.)

PRO ( выше 10000 руб.)""", reply_markup=pay_level_keyboard)


@dp.message_handler(state=EmployerState.level)
async def set_level(message: types.Message, state: FSMContext):
    employer = session.query(Employer).filter_by(user_id=message.from_user.id).first()
    vacancy = session.query(Vacancy).filter_by(employer=employer, finite_state=9)[-1]
    if message.text in pay_level_list:
        vacancy.pay_level = message.text
        vacancy.numb_level = pay_level_dict[message.text][1]
        vacancy.finite_state = 10
        session.commit()
        session.close()
        await EmployerState.next()
        await message.answer("""Введите сумму вознаграждения рекрутеру""")
    else:
        await message.answer("Выберите один из предложенных вариантов!")


@dp.message_handler(state=EmployerState.salary)
async def set_salary(message: types.Message, state: FSMContext):
    employer = session.query(Employer).filter_by(user_id=message.from_user.id).first()
    vacancy = session.query(Vacancy).filter_by(employer=employer, finite_state=10)[-1]
    try:
        salary = int(message.text)
    except ValueError:
        await message.answer("Введите валидные данные. Одно число без дополнительных знаков")
        return
    pay_level = vacancy.pay_level
    if pay_level_dict[pay_level][0][0] <= salary <= pay_level_dict[pay_level][0][1]:
        vacancy.salary = salary
        vacancy.finite_state = 11
        session.commit()
        recruiter_count = session.query(Recruiter).filter(Recruiter.level_numb >= vacancy.numb_level).count()
        await EmployerState.next()
        await message.answer("""Вами выбран уровень {0}! 
После модерации я покажу ее {1} рекрутерам и они предложат целевых кандидатов, если заявка их заинтересует.
Вам останется только сделать свой выбор. А пока вы можете заняться более важными делами. До связи, {2} {3}!""".format(
            pay_level,
            150,
            message.from_user.first_name,
            message.from_user.last_name,
        ))
        await message.answer(vacancy, reply_markup=keyboard_activate)
        session.close()
    else:
        await message.answer("Введенное значение не удовлетворяет выбранному уровню.")


@dp.message_handler(state=EmployerState.activate)
async def set_activate(message: types.Message, state: FSMContext):
    employer = session.query(Employer).filter_by(user_id=message.from_user.id).first()
    vacancy = session.query(Vacancy).filter_by(employer=employer, finite_state=11)[-1]
    if message.text == "Запустить подбор":
        vacancy.active = True
        vacancy.finite_state = 12
        session.commit()
        session.close()
        await state.finish()
        await message.answer("Заявка добавлена в выдачу, вам придёт сообщение, как только на неё откликнутся!")
    elif message.text == "Сохранить в черновик":
        vacancy.finite_state = 12
        session.commit()
        session.close()
        await state.finish()
        await message.answer("Заявка сохранена в черновик. Выберите команду /drafts чтобы отобразить ваши черновики")
    elif message.text == "Отменить":
        session.delete(vacancy)
        session.commit()
        session.close()
        await state.finish()
        await message.answer("Заявка удалена")
    else:
        await message.answer("Выберите один из предложенных вариантов", reply_markup=keyboard_activate)


@dp.message_handler(Text(equals="РЕКРУТЕР"))
async def recruiter_start(message: types.Message):
    if not session.query(Recruiter).filter_by(user_id=message.from_user.id).first():
        user = session.query(User).filter_by(telegram_id=message.from_user.id).first()
        session.add(Recruiter(user=user))
        session.commit()
        session.close()
        text_hello = """Здравствуйте, {0} {1}. 
    Рад приветствовать тебя!
    Заработай больше на поиске персонала. Закрывай заявки в любое время. Делай то, что тебе нравится!""".format(
            message.from_user.first_name,
            message.from_user.last_name,
        )
        await message.answer(text_hello)
        text_levels = """
    Для рекрутеров доступны 4 уровня профиля: LIGHT, MEDIUM, HARD, PRO. 
    LIGHT - доступны заявки с вознаграждением рекрутеру до 500 рублей. 
    MEDIUM – заявки стоимостью до 5000 руб. Переход при закрытии 3-х  заявок от разных работодателей на уровне LIGHT.
    HARD – заявки стоимостью от 5000 до 10000 руб. Переход при закрытии 7-ми заявок разных работодателей на уровне MEDIUM.
    PRO – заявки стоимостью от 10000 руб. Переход при закрытии 10-ти заявок любых работодателей на уровне HARD.
    """
        await message.answer(text_levels)
        text_question = """
    Вы можете продолжить на уровне LIGHT или отправить резюме, я рассмотрю его и присвою соответствующий уровень.
    """
        await RecruiterRegistry.register.set()
        await message.answer(text_question, reply_markup=level_recruiter_board)
    else:
        if not session.query(Recruiter).filter_by(user_id=message.from_user.id).first().finished_educ:
            text_hello = """Здравствуйте, {0} {1}. 
                Рад приветствовать тебя!
                Заработай больше на поиске персонала. Закрывай заявки в любое время. Делай то, что тебе нравится!""".format(
                message.from_user.first_name,
                message.from_user.last_name,
            )
            await message.answer(text_hello)
            text_levels = """
                Для рекрутеров доступны 4 уровня профиля: LIGHT, MEDIUM, HARD, PRO. 
                LIGHT - доступны заявки с вознаграждением рекрутеру до 500 рублей. 
                MEDIUM – заявки стоимостью до 5000 руб. Переход при закрытии 3-х  заявок от разных работодателей на уровне LIGHT.
                HARD – заявки стоимостью от 5000 до 10000 руб. Переход при закрытии 7-ми заявок разных работодателей на уровне MEDIUM.
                PRO – заявки стоимостью от 10000 руб. Переход при закрытии 10-ти заявок любых работодателей на уровне HARD.
                """
            await message.answer(text_levels)
            text_question = """
                Вы можете продолжить на уровне LIGHT или отправить резюме, я рассмотрю его и присвою соответствующий уровень.
                """
            await RecruiterRegistry.register.set()
            await message.answer(text_question, reply_markup=level_recruiter_board)
        else:
            await message.answer(
                "У вас уже есть профиль рекрутера, выберите команду /get_vacancies чтобы получить заявки")


@dp.message_handler(state=RecruiterRegistry.register)
async def choose_level(message: types.Message, state: FSMContext):
    recruiter = session.query(Recruiter).filter_by(user_id=message.from_user.id).first()
    if message.text == "УРОВЕНЬ LIGHT":
        recruiter.level = "LIGHT"
        recruiter.level_numb = 1
        session.commit()
        session.close()
        await RecruiterRegistry.text1.set()
        await set_light_level(message.from_user.id)
    elif message.text == "ОТПРАВИТЬ РЕЗЮМЕ":
        recruiter.level = "LIGHT"
        recruiter.level_numb = 1
        recruiter.finished_educ = True
        session.add(Resume(recruiter=recruiter))
        session.commit()
        session.close()
        await message.answer("""
Я всегда рад опытным рекрутерам! Отлично, что вы решили работать со мной!
Расскажите мне о себе и в течение 3- х дней я приму решение:
""")
        await message.answer("Заполните форму, чтобы перейти на следующий уровень.")
        await message.answer("Ваше ФИО:")
        await RecruiterRegistry.next()
    else:
        await message.answer("Выберите один из предложенных вариантов!")


@dp.message_handler(state=RecruiterRegistry.fio)
async def set_fio(message: types.Message, state: FSMContext):
    recruiter = session.query(Recruiter).filter_by(user_id=message.from_user.id).first()
    resume = session.query(Resume).filter_by(recruiter_id=recruiter.id).first()
    resume.fio = message.text
    session.commit()
    session.close()
    await message.answer("Сколько лет вы в подборе:")
    await RecruiterRegistry.next()


@dp.message_handler(state=RecruiterRegistry.years)
async def set_years(message: types.Message, state: FSMContext):
    recruiter = session.query(Recruiter).filter_by(user_id=message.from_user.id).first()
    resume = session.query(Resume).filter_by(recruiter_id=recruiter.id).first()
    resume.years = message.text
    session.commit()
    session.close()
    await message.answer("В какой области вы специализируетесь:")
    await RecruiterRegistry.next()


@dp.message_handler(state=RecruiterRegistry.specialization)
async def set_specialization(message: types.Message, state: FSMContext):
    recruiter = session.query(Recruiter).filter_by(user_id=message.from_user.id).first()
    resume = session.query(Resume).filter_by(recruiter_id=recruiter.id).first()
    resume.specialization = message.text
    session.commit()
    session.close()
    await message.answer("Какими инструментами пользуетесь при подборе:")
    await RecruiterRegistry.next()


@dp.message_handler(state=RecruiterRegistry.tools)
async def set_tools(message: types.Message, state: FSMContext):
    recruiter = session.query(Recruiter).filter_by(user_id=message.from_user.id).first()
    resume = session.query(Resume).filter_by(recruiter_id=recruiter.id).first()
    resume.tools = message.text
    session.commit()
    session.close()
    await message.answer("С какими трудностями сталкивались при подборе")
    await RecruiterRegistry.next()


@dp.message_handler(state=RecruiterRegistry.difficulties)
async def set_difficulties(message: types.Message, state: FSMContext):
    recruiter = session.query(Recruiter).filter_by(user_id=message.from_user.id).first()
    resume = session.query(Resume).filter_by(recruiter_id=recruiter.id).first()
    resume.difficulties = message.text
    session.commit()
    session.close()
    await message.answer("Напишите краткое приглашение соискателю на вакансию")
    await RecruiterRegistry.next()


@dp.message_handler(state=RecruiterRegistry.invitation)
async def set_invitation(message: types.Message, state: FSMContext):
    recruiter = session.query(Recruiter).filter_by(user_id=message.from_user.id).first()
    resume = session.query(Resume).filter_by(recruiter_id=recruiter.id).first()
    resume.invitation = message.text
    session.commit()
    session.close()
    await message.answer("""Вы не можете долго закрыть заявку и понимаете, что заработная плата не в рынке. 
Напишите письмо работодателю с предложением откорректировать заявку.""")
    await RecruiterRegistry.next()


@dp.message_handler(state=RecruiterRegistry.letter)
async def set_letter(message: types.Message, state: FSMContext):
    recruiter = session.query(Recruiter).filter_by(user_id=message.from_user.id).first()
    resume = session.query(Resume).filter_by(recruiter_id=recruiter.id).first()
    resume.letter = message.text
    session.commit()
    session.close()
    await message.answer("Не все соискатели подошли. Как вы откажете соискателю?")
    await RecruiterRegistry.next()


@dp.message_handler(state=RecruiterRegistry.refusal)
async def set_refusal(message: types.Message, state: FSMContext):
    recruiter = session.query(Recruiter).filter_by(user_id=message.from_user.id).first()
    resume = session.query(Resume).filter_by(recruiter_id=recruiter.id).first()
    resume.refusal = message.text
    session.commit()
    await message.answer("Ваше резюме:")
    await message.answer(resume)
    await message.answer("""Я рассмотрю ваше резюме в течение 3 дней и вам будет присвоен соответствующий уровень. 
На время рассмотрения вам будет присвоен уровень LIGHT.""")
    await message.answer("""Теперь вы можете закрывать заявки от работодателей. 
Чтобы увидеть доступные заявки воспользуйтесь командой /get_vacancies""")
    await state.finish()
    admins = session.query(User).filter_by(superuser=True).all()
    admin_buttons = types.InlineKeyboardMarkup()
    admin_buttons.add(
        types.InlineKeyboardButton("LIGHT", callback_data="set_lvl " + "LIGHT " + "1 " + str(message.from_user.id)),
        types.InlineKeyboardButton("MEDIUM", callback_data="set_lvl " + "MEDIUM " + "2 " + str(message.from_user.id)),
        types.InlineKeyboardButton("HARD", callback_data="set_lvl " + "HARD " + "3 " + str(message.from_user.id)),
        types.InlineKeyboardButton("PRO", callback_data="set_lvl " + "PRO " + "4 " + str(message.from_user.id)),
    )
    for admin in admins:
        await bot.send_message(admin.telegram_id, "Резюме от рекрутера для рассмотрения")
        await bot.send_message(admin.telegram_id, resume)
        await bot.send_message(admin.telegram_id, "Назначьте уровень рекрутеру", reply_markup=admin_buttons)
    session.close()


@dp.message_handler(state=RecruiterRegistry.text1)
async def first_text(message: types.Message, state: FSMContext):
    if message.text == "ДАЛЕЕ":
        await message.answer("""Мир поделен на две части: тот, кто предлагает работу, и тот, кто эту работу выполняет.
 
Рекрутер относится ко второй категории.

Мы с вами выполняем работу по поиску людей, которые согласны выполнять работу тех, кто ее предоставляет.

Требуется понимать - насколько качественно мы выполним нашу с вами работу и как быстро предоставим нужного человека – от этого зависит наше будущее, как профессионала.
""", reply_markup=next_button)

        await RecruiterRegistry.next()
    else:
        await message.answer("Нажмите ДАЛЕЕ, чтобы продолжить обучение.")


@dp.message_handler(state=RecruiterRegistry.text2)
async def second_text(message: types.Message, state: FSMContext):
    if message.text == "ДАЛЕЕ":
        await message.answer("""Сейчас искать людей гораздо проще, когда мир технологий развит и продолжает развиваться. Использовать можно все возможные ресурсы:
        
- во-первых, telegram. Есть множество сообществ, где общаются специалисты той или иной области. 
Подписываемся на их группы и каналы и общаемся с ними от лица представителя работодателя. Кто-то да откликнется.

- социальные сети. Технология та же – используем тематические группы и форумы и находим тех, кого заинтересуют наши предложения.

- специализированные площадки, сайты по поиску работы. Сейчас их множество, но многие могут быть платными. 
Их можно использовать, но нужно быть готовыми платить за услуги по предоставлению резюме.

- сайты знакомств. Даже такие сайты имеются в инструментах профессионального рекрутера. 
Можно завязывать диалог, а затем плавно переходить к предложению по работе. Если попадете в бан, то ничего страшного. 
Поверьте, многие, обдумав потом предложение, соглашаются на оффер.

- ну и конечно печатные СМИ и объявления на местных досках. 
Сколько бы людей не пользовалось интернетом, иногда выгоднее наклеить объявление на остановке и получить требуемый отклик.

- прямой поиск. Когда мы точно знаем, где находится требуемый специалист, и пытаемся его переманить. 
Обычно это уже уровень PRO, но и новички бывают проворными.
""", reply_markup=next_button)

        await RecruiterRegistry.next()
    else:
        await message.answer("Нажмите ДАЛЕЕ, чтобы продолжить обучение.")


@dp.message_handler(state=RecruiterRegistry.text3)
async def third_text(message: types.Message, state: FSMContext):
    if message.text == "ДАЛЕЕ":
        await message.answer("""Прежде, чем направить кандидата на рассмотрение рекрутер использует три проверенных шага:
        
- первичное интервью. Свяжитесь с кандидатом по аудиосвязи, чтобы задать несколько вопросов в рамках заявки. 
Прежде, выпишите себе вопросы, которые будете задавать.

- проведите видеовстречу. Используйте любую платформу для видеоконференций, например, вы можете воспользоваться видео-звонком в telegram или сейчас очень популярен zoom. 
Оцените для себя кандидата и попробуйте понять понравится ли он будущему работодателю.

- есть возможность встретиться – пригласите в кафе или к себе в офис. Разговор лучше переписки, встреча вживую - лучше общения онлайн.
Поняли, что сами взяли бы такого сотрудника к себе – направляйте работодателю на оценку и дальнейшее решение по трудоустройству.

""", reply_markup=next_button)

        await RecruiterRegistry.next()
    else:
        await message.answer("Нажмите ДАЛЕЕ, чтобы продолжить обучение.")


@dp.message_handler(state=RecruiterRegistry.text4)
async def fourth_text(message: types.Message, state: FSMContext):
    if message.text == "ДАЛЕЕ":
        await message.answer("""Перечислю вам самые популярные инструменты для проведения онлайн встреч:

- Сам телеграм 
- zoom.us 
- meet.google.com 
- telemost.yandex.ru

Используйте любой из перечисленных или иные для быстрых и качественных встреч с соискателями.
""", reply_markup=next_button)

        await RecruiterRegistry.next()
    else:
        await message.answer("Нажмите ДАЛЕЕ, чтобы продолжить обучение.")


@dp.message_handler(state=RecruiterRegistry.text5)
async def fourth_text(message: types.Message, state: FSMContext):
    if message.text == "ДАЛЕЕ":
        await message.answer(""" 
Если ты еще никак не оформил свою деятельность, для уплаты налогов, то для закрытия заявок с получением оплаты по завершнению, тебе нужно открыть самозанятость. 

Это не сложно и не потребует от тебя никаких затрат. Наоборот, позволит работать уверенно. 

Инструкция по открытию самозанятости npd.nalog.ru.

Для подтверждения ИП или самозанятости используйте команду /confirm_docs
И приложите свидетельство о регистрации ИП или справку о самозанятости.
Повышение на следующие уровни производится автоматически.
""", reply_markup=star_test_button)
        await message.answer("""Сейчас я дам вам небольшой тест.""")
        await RecruiterRegistry.next()
    else:
        await message.answer("Нажмите ДАЛЕЕ, чтобы продолжить обучение.")


@dp.message_handler(state=RecruiterRegistry.test1)
async def first_test(message: types.Message, state: FSMContext):
    if message.text == "НАЧАТЬ ТЕСТ":
        answer = session.query(Answer).filter_by(user_id=message.from_user.id).first()
        if answer:
            session.delete(answer)
            session.commit()
        await message.answer("""В тестах может быть несколько вариантов ответов. 
Выберите те, которые считаете правильными, подтвердите ответ, после чего нажмите ДАЛЕЕ""")
        response = await bot.send_poll(
            message.from_user.id,
            *question1,
            allows_multiple_answers=True,
            reply_markup=next_button)
        session.add(Question(poll_id=response.poll.id, question=response.poll.question))
        session.commit()
        session.close()
        await state.finish()
    else:
        await message.answer("Нажмите НАЧАТЬ ТЕСТ, чтобы продолжить обучение.")


@dp.message_handler(state=RecruiterRegistry.test2)
async def second_test(message: types.Message, state: FSMContext):
    if message.text == "ДАЛЕЕ":
        response = await bot.send_poll(
            message.from_user.id,
            *question2,
            allows_multiple_answers=True,
            reply_markup=next_button)
        session.add(Question(poll_id=response.poll.id, question=response.poll.question))
        session.commit()
        session.close()
        await state.finish()
    else:
        await message.answer("Нажмите ДАЛЕЕ, чтобы получить следующий вопрос.")


@dp.message_handler(state=RecruiterRegistry.test3)
async def third_test(message: types.Message, state: FSMContext):
    if message.text == "ДАЛЕЕ":
        response = await bot.send_poll(
            message.from_user.id,
            *question3,
            allows_multiple_answers=True,
            reply_markup=finish_test_button)
        session.add(Question(poll_id=response.poll.id, question=response.poll.question))
        session.commit()
        session.close()
        await state.finish()
    else:
        await message.answer("Нажмите ДАЛЕЕ, чтобы получить следующий вопрос.")


@dp.message_handler(state=RecruiterRegistry.finish_test)
async def finish_test(message: types.Message, state: FSMContext):
    if message.text == "ЗАВЕРШИТЬ ТЕСТ":
        answer = session.query(Answer).filter_by(user_id=message.from_user.id).first()
        if answer.score == 3:
            await message.answer("Поздравляем, вы правильно ответили на все вопросы!")
            await message.answer("""Теперь вы можете закрывать заявки от работодателей. 
Чтобы увидеть доступные заявки воспользуйтесь командой /get_vacancies""")
            await state.finish()
            recruiter = session.query(Recruiter).filter_by(user_id=message.from_user.id).first()
            recruiter.finished_educ = True
            session.commit()
            session.close()
        else:
            session.delete(answer)
            session.commit()
            session.close()
            await message.answer("""К сожалению, вы  ответили не на все вопросы правильно. 
Нажмите НАЧАТЬ ТЕСТ, чтобы пройти тест заново.""", reply_markup=star_test_button)
            await RecruiterRegistry.test1.set()
    else:
        await message.answer("Нажмите ЗАВЕРШИТЬ ТЕСТ, чтобы завершить тест.")


@dp.message_handler(state=CandidateRegister.name)
async def set_candidate_name(message: types.Message, state: FSMContext):
    recruiter = session.query(Recruiter).filter_by(user_id=message.from_user.id).first()
    candidate = session.query(Candidate).filter_by(recruiter_id=recruiter.id, finite_state=0)[-1]
    name = message.text
    candidate.name = name
    candidate.finite_state = 1
    await message.answer("Введите итоги интервью:", reply_markup=not_completed_button)
    await CandidateRegister.next()


@dp.message_handler(state=CandidateRegister.interview)
async def set_candidate_interview(message: types.Message, state: FSMContext):
    recruiter = session.query(Recruiter).filter_by(user_id=message.from_user.id).first()
    candidate = session.query(Candidate).filter_by(recruiter_id=recruiter.id, finite_state=1)[-1]
    interview = message.text
    if message.text == "Не проводилось":
        candidate.interview = "None"
    else:
        candidate.interview = interview
    candidate.finite_state = 2
    await message.answer("Введите итоги видеоконференции:", reply_markup=not_completed_button)
    await CandidateRegister.next()


@dp.message_handler(state=CandidateRegister.video)
async def set_candidate_video(message: types.Message, state: FSMContext):
    recruiter = session.query(Recruiter).filter_by(user_id=message.from_user.id).first()
    candidate = session.query(Candidate).filter_by(recruiter_id=recruiter.id, finite_state=2)[-1]
    video = message.text
    if message.text == "Не проводилось":
        candidate.video = "None"
    else:
        candidate.video = video
    candidate.finite_state = 3
    await message.answer("Введите итоги встречи:", reply_markup=not_completed_button)
    await CandidateRegister.next()


@dp.message_handler(state=CandidateRegister.meeting)
async def set_candidate_meeting(message: types.Message, state: FSMContext):
    recruiter = session.query(Recruiter).filter_by(user_id=message.from_user.id).first()
    candidate = session.query(Candidate).filter_by(recruiter_id=recruiter.id, finite_state=3)[-1]
    meeting = message.text
    if message.text == "Не проводилось":
        candidate.meeting = "None"
    else:
        candidate.meeting = meeting
    candidate.finite_state = 4
    await message.answer("Оценка кандидата на соответствие предлагаемой должности",
                         reply_markup=mark_of_candidate_buttons)
    await CandidateRegister.next()


@dp.message_handler(state=CandidateRegister.mark)
async def set_candidate_mark(message: types.Message, state: FSMContext):
    recruiter = session.query(Recruiter).filter_by(user_id=message.from_user.id).first()
    candidate = session.query(Candidate).filter_by(recruiter_id=recruiter.id, finite_state=4)[-1]
    mark = message.text
    if message.text in mark_of_candidate_list:
        candidate.mark = mark
        candidate.finite_state = 5
        session.commit()
        session.close()
        await CandidateRegister.next()
        await message.answer("Приложите файл с резюме или приложите ссылку на резюме или отправьте его текстом")
    else:
        await message.answer("Выберите один из предложенных вариантов")


@dp.message_handler(state=CandidateRegister.resume, content_types=ContentType.DOCUMENT)
async def set_candidate_resume_with_file(message: types.Message, state: FSMContext):
    recruiter = session.query(Recruiter).filter_by(user_id=message.from_user.id).first()
    candidate = session.query(Candidate).filter_by(recruiter_id=recruiter.id, finite_state=5)[-1]
    file_id = message.document.file_id
    resume_text = message.caption
    try:
        file = await bot.get_file(file_id)
    except FileIsTooBig:
        await message.answer("Файл слишком большой! Попробуйте другой файл или отправьте резюме текстом.")
    else:
        file_path = file.file_path
        file_extension = file_path[file_path.rfind("."):]
        if file_extension in [".txt", ".doc", ".docx", ".pdf"]:
            file_name = file_id + file_extension
            candidate.resume_text = resume_text
            candidate.resume_file = file_name
            candidate.finite_state = 6
            session.commit()
            await bot.download_file(file_path, f"resume/{file_name}")
            await message.answer("Ваш кандидат поступил на рассмотрения работодателя, ожидайте ответа!")
            await send_candidate_to_employer(candidate.id)
            session.close()
            await state.finish()
        else:
            await message.answer(
                "Разрешены файлы с расширениями .txt, .doc, .docx, .pdf. Попробуйте другой файл или отправьте резюме ссылкой или текстом в сообщении.")


@dp.message_handler(state=CandidateRegister.resume)
async def set_candidate_resume_without_file(message: types.Message, state: FSMContext):
    recruiter = session.query(Recruiter).filter_by(user_id=message.from_user.id).first()
    candidate = session.query(Candidate).filter_by(recruiter_id=recruiter.id, finite_state=5)[-1]
    resume_text = message.text
    candidate.resume_text = resume_text
    candidate.finite_state = 6
    session.commit()
    await message.answer("Ваш кандидат поступил на рассмотрения работодателя, ожидайте ответа!")
    await send_candidate_to_employer(candidate.id)
    session.close()
    await state.finish()


@dp.message_handler(state=SendContact.send_contact)
async def set_candidate_contact(message: types.Message, state: FSMContext):
    recruiter = session.query(Recruiter).filter_by(user_id=message.from_user.id).first()
    candidate = session.query(Candidate).filter_by(recruiter_id=recruiter.id, finite_state=7,
                                                   taken_refused=None).first()
    candidate.finite_state = 8
    session.commit()
    await message.answer("Контакты переданы работодателю")
    await bot.send_message(candidate.vacancy.employer.user_id, "Вам переданы контакты для кандидата \n"
                                                               f"{message.text} \n\n"
                                                               f"Кандидат"
                                                               f"{candidate}")
    vacancy = candidate.vacancy
    in_work = session.query(InWork).filter(InWork.recruiter_id.not_in([recruiter.id]), InWork.vacancy == vacancy).all()
    for vac in in_work:
        rec = vac.recruiter.user_id
        session.delete(vac)
        session.commit()
        await bot.send_message(rec, "Вакансия закрыта:\n", reply_markup=get_vacancy_button(vacancy))
    vacancy.active = False
    session.commit()
    await bot.send_message(candidate.vacancy.employer.user_id, reply_markup=get_vacancy_button(vacancy))
    session.close()
    await state.finish()


@dp.message_handler(state=SendLink.send_link)
async def set_candidate_link(message: types.Message, state: FSMContext):
    recruiter = session.query(Recruiter).filter_by(user_id=message.from_user.id).first()
    candidate = session.query(Candidate).filter_by(recruiter_id=recruiter.id, finite_state=6).first()
    await bot.send_message(candidate.vacancy.employer.user_id,
                           "Вам передана ссылка на конференцию для собеседования кандидата \n"
                           f"{message.text} \n\n"
                           f"Кандидат"
                           f"{candidate}")
    vacancy = candidate.vacancy
    await bot.send_message(candidate.vacancy.employer.user_id, reply_markup=get_vacancy_button(vacancy))
    await message.answer("Ссылка отправлена работодателю")
    session.close()
    await state.finish()


@dp.poll_answer_handler()
async def handle_poll_answer(quiz_answer: types.PollAnswer):
    poll_id = quiz_answer.poll_id
    answers = quiz_answer.option_ids
    user_id = quiz_answer.user.id
    question = session.query(Question).get(poll_id).question
    answer_score = get_or_create(session, Answer, user_id=user_id)
    if question == question1[0]:
        await RecruiterRegistry.test2.set()
        if answers == [0, 1, 3, 4, 5]:
            answer_score.score += 1
            session.commit()
            session.close()
        else:
            session.close()
    elif question == question2[0]:
        await RecruiterRegistry.test3.set()
        if answers == [0, 1, 2]:
            answer_score.score += 1
            session.commit()
            session.close()
        else:
            session.close()
    elif question == question3[0]:
        await RecruiterRegistry.finish_test.set()
        if 3 not in answers:
            answer_score.score += 1
            session.commit()
            session.close()
        else:
            session.close()


@dp.callback_query_handler(lambda callback_query: True)
async def handle_callback(callback_query: types.CallbackQuery):
    global vacancies
    callback_list = callback_query.data.split()
    if callback_list[0] == "set_lvl":
        await admin_set_level(callback_query.from_user.id, *callback_list[1:])
    elif callback_list[0] == "set_vacancy":
        employer_id = callback_list[1]
        employer = session.query(Employer).filter_by(user_id=employer_id).first()
        vacancy = session.query(Vacancy).filter_by(employer=employer, finite_state=1).first()
        vacancy.category_id = callback_list[2]
        vacancy.finite_state = 2
        session.commit()
        session.close()
        await bot.send_message(employer_id, "Введите наименование компании")
        await EmployerState.company.set()

    elif callback_list[0] == "categories":
        """коллбэк для кнопки ВЫБРАТЬ КАТЕГОРИЮ"""
        user_id = callback_list[1]
        categories = session.query(Category).all()
        for category in categories:
            category_buttons = types.InlineKeyboardMarkup()
            recruiter = session.query(Recruiter).get(user_id)
            category_buttons.add(
                types.InlineKeyboardButton("ВЫБРАТЬ КАТЕГОРИЮ",
                                           callback_data="vacancies " + f"{recruiter.id} " + f"{category.category_id}")
            )
            await bot.send_message(recruiter.user_id, category.name, reply_markup=category_buttons)

    elif callback_list[0] == "vacancies":
        """коллбэк для кнопки ВСЕ ВАКАНСИИ и ВЫБРАТЬ КАТЕГОРИЮ"""
        recruiter_id = callback_list[1]
        category = callback_list[2]
        recruiter = session.query(Recruiter).get(recruiter_id)
        if category == "all":
            vacancies = session.query(Vacancy).filter(
                Vacancy.numb_level <= recruiter.level_numb,
                Vacancy.active == True
            ).all()
            for vacancy in vacancies:
                in_work = session.query(InWork).filter_by(recruiter_id=recruiter_id, vacancy_id=vacancy.id).first()
                if in_work in vacancy.inwork:
                    vacancies.remove(vacancy)
            await bot.send_message(recruiter.user_id, "Вам доступно %s заявок" % len(vacancies))
        else:
            vacancies = session.query(Vacancy).filter(
                Vacancy.numb_level <= recruiter.level_numb,
                Vacancy.active == True,
                Vacancy.category_id == category
            ).all()
            for vacancy in vacancies:
                in_work = session.query(InWork).filter_by(recruiter_id=recruiter_id, vacancy_id=vacancy.id).first()
                if in_work in vacancy.inwork:
                    vacancies.remove(vacancy)
            category_name = session.query(Category.name).filter(Category.category_id == category).first()[0]
            text = "Выбрана категория %s, в данной категории доступно %s заявок" % (category_name, str(len(vacancies)))
            await bot.send_message(recruiter.user_id, text)
        for vacancy in vacancies:
            recruiter_buttons = types.InlineKeyboardMarkup()
            recruiter_buttons.add(
                types.InlineKeyboardButton("ВЗЯТЬ В РАБОТУ",
                                           callback_data="in_work " + f"{vacancy.id} " + f"{recruiter_id}"),
                types.InlineKeyboardButton("ПРЕДЛОЖИТЬ КАНДИДАТА",
                                           callback_data="add_cand " + f"{vacancy.id} " + f"{recruiter_id}"),
            )
            await bot.send_message(recruiter.user_id, vacancy, reply_markup=recruiter_buttons)

    elif callback_list[0] == "in_work":
        vacancy_id = callback_list[1]
        recruiter_id = callback_list[2]
        vacancy = session.query(Vacancy).get(vacancy_id)
        recruiter = session.query(Recruiter).get(recruiter_id)
        if vacancy and recruiter:
            in_work = get_or_create(session, InWork, vacancy=vacancy, recruiter=recruiter)
            vacancies_in_work = session.query(InWork).filter_by(recruiter_id=recruiter.id).all()
            len_vac = len(vacancies_in_work)
            await bot.send_message(recruiter.user_id, f"""Заявка №{vacancy.id} {vacancy.name} в работе. 

Итого заявок в работе: {len_vac}

Используйте команду /in_work чтобы получить вакансии находящиеся у вас в работе""")

    elif callback_list[0] == "add_cand":
        vacancy_id = callback_list[1]
        recruiter_id = callback_list[2]
        vacancy = session.query(Vacancy).get(vacancy_id)
        recruiter = session.query(Recruiter).get(recruiter_id)
        session.add(Candidate(vacancy=vacancy, recruiter=recruiter))
        session.commit()
        await CandidateRegister.name.set()
        await bot.send_message(recruiter.user_id, "Давайте заполним форму кандидата")
        await bot.send_message(recruiter.user_id, "Введите имя кандидата")
        session.close()


    elif callback_list[0] == "del_vac":
        vacancy_id = callback_list[1]
        vacancy = session.query(Vacancy).filter_by(id=vacancy_id).first()
        in_work = session.query(InWork).filter_by(vacancy_id=vacancy_id).all()
        for work in in_work:
            user_id = session.query(Recruiter).get(work.recruiter_id).user_id
            await bot.send_message(user_id, """Работодатель удалил заявку \n""" + vacancy.__repr__())
            session.delete(work)
            session.commit()
        session.delete(vacancy)
        session.commit()
        session.close()
        await bot.send_message(callback_list[2], """Успешно удалено""")

    elif callback_list[0] == "draft_vac":
        vacancy_id = callback_list[1]
        vacancy = session.query(Vacancy).filter_by(id=vacancy_id).first()
        if vacancy.active:
            vacancy.active = False
            msg = "Заявка перемещена в черновики. Вы можете проверить свои черновики с помощью команды /drafts"
        else:
            vacancy.active = True
            msg = "Заявка добавлена в выдачу. Вы можете проверить свои заявки с помощью команды /my_vacancies"
        session.commit()
        session.close()
        await bot.send_message(callback_list[2], msg)

    elif callback_list[0] == "cand_ref":
        candidate_id = callback_list[1]
        candidate = session.query(Candidate).get(candidate_id)
        if candidate.taken_refused != "refused" and candidate.taken_refused != "taken":
            candidate.taken_refused = "refused"
            vacancy = candidate.vacancy
            recruiter = candidate.recruiter
            await bot.send_message(recruiter.user.telegram_id, "Ваш кандидат отклонен\n"
                                                               f"Кандидат: \n{candidate}",
                                   reply_markup=get_vacancy_button(vacancy))
        else:
            await bot.send_message(callback_query.from_user.id, "Вы уже отклонили/приняли этого кандидата")

    elif callback_list[0] == "cand_inter":
        candidate_id = callback_list[1]
        candidate = session.query(Candidate).get(candidate_id)
        if candidate.taken_refused != "refused" and candidate.taken_refused != "taken":
            send_interview_buttons = types.InlineKeyboardMarkup()
            send_interview_buttons.add(
                types.InlineKeyboardButton("Аудио",
                                           callback_data="interview_audio " + f"{candidate_id}"),
                types.InlineKeyboardButton("Видео",
                                           callback_data="interview_video " + f"{candidate_id}"),
            )
            await bot.send_message(callback_query.from_user.id, "Выберите тип собеседования",
                                   reply_markup=send_interview_buttons)
            session.close()
        else:
            await bot.send_message(callback_query.from_user.id, "Вы уже отклонили/приняли этого кандидата")

    elif callback_list[0] == "cand_empl":
        candidate_id = callback_list[1]
        candidate = session.query(Candidate).get(candidate_id)
        if candidate.taken_refused != "refused" and candidate.taken_refused != "taken":
            candidate.taken_refused = "taken"
            candidate.finite_state = 7
            vacancy = candidate.vacancy
            recruiter = candidate.recruiter
            await bot.send_message(recruiter.user.telegram_id, "Поздравляем! Ваш кандидат соответствует заявке."
                                                               f"Кандидат: \n{candidate}",
                                   reply_markup=get_vacancy_button(vacancy))
            send_contact_buttons = types.InlineKeyboardMarkup()
            send_contact_buttons.add(
                types.InlineKeyboardButton("ОТПРАВИТЬ КОНТАКТЫ",
                                           callback_data="contact " + f"{vacancy.id} " + f"{recruiter.id} " + f"{candidate.id}"),
            )
            await bot.send_message(recruiter.user.telegram_id, "Отправьте контакты кандидата для работодателя",
                                   reply_markup=send_contact_buttons)
            session.commit()
            session.close()
        else:
            await bot.send_message(callback_query.from_user.id, "Вы уже отклонили/приняли этого кандидата")

    elif callback_list[0] == "contact":
        await SendContact.send_contact.set()
        await bot.send_message(callback_query.from_user.id, "Отправьте сообщение с контактами кандидата")

    elif "interview" in callback_list[0]:
        candidate_id = callback_list[1]
        candidate = session.query(Candidate).get(candidate_id)
        vacancy = candidate.vacancy
        recruiter = candidate.recruiter
        interview_type = "аудио"
        if "video" in callback_list[0]:
            interview_type = "видео"
        send_link_buttons = get_vacancy_button(vacancy)
        send_link_buttons.add(
            types.InlineKeyboardButton("ОТПРАВИТЬ ССЫЛКУ",
                                       callback_data="inter_link " + f"{candidate.id}"),
        )
        await bot.send_message(recruiter.user.telegram_id,
                               f"Работодатель хочет провести {interview_type} собеседование с кандидатом. \n"
                               f"Кандидат: \n{candidate}",
                               reply_markup=send_link_buttons)
        session.close()

    elif callback_list[0] == "inter_link":
        await SendLink.send_link.set()
        await bot.send_message(callback_query.from_user.id, "Отправьте сообщение с ссылкой на конференцию")

    elif callback_list[0] == "show_vacancy":
        vacancy_id = callback_list[1]
        vacancy = session.query(Vacancy).get(vacancy_id)
        await bot.send_message(callback_query.from_user.id, "Вакансия: \n"
                               f"{vacancy}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
