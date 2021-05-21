import telebot
import random
import os
from models import form, Base, workers, candidates
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from time import sleep

engine = create_engine(r'sqlite:///forms.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
DBSession.bind = engine
session = DBSession()
'''

user = os.environ.get('SQL_USER')
password = os.environ.get('SQL_PASSWORD')
db_name = os.environ.get('SQL_DATABASE')
db_host = os.environ.get('SQL_HOST')
engine = create_engine('postgresql+psycopg2://%s:%s@%s/%s' % (str(user), str(password), str(db_host), str(db_name)))
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
DBSession.bind = engine
session = DBSession()
'''
# ('LIGHT (бесплатно)', 'MEDIUM (до 5000 руб.)', 'HARD (от 5000 до 10000 руб.)', 'PRO (выше 10000 руб.)')
reading, writing = False, False
#token = os.environ['TOKEN']
token2 = '1750912576:AAHFYIs2DQp46NVxfMCuxvhZ2mrHbXupVi4'
bot = telebot.TeleBot(token2)
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('РАБОТАДАТЕЛЬ', 'РЕКРУТЕР')
keyboard2 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard2.row('ЗАПОЛНИТЬ ЗАЯВКУ')
keyboard3 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard3.row('LIGHT', 'MEDIUM', 'HARD', 'PRO')
keyboard4 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard4.row('Запустить подбор', )  # Исправить
# keyboard5 = telebot.types.InlineKeyboardMarkup()
# butn1, butn2, butn3, butn4, bunt5, bunt6, butn7 = telebot.types.InlineKeyboardButton("Название"), telebot.types.InlineKeyboardButton("Обязанности"), telebot.types.InlineKeyboardButton("Требования"), telebot.types.InlineKeyboardButton("Условия"),telebot.types.InlineKeyboardButton("Уровень оплаты"),telebot.types.InlineKeyboardButton("Сумма"), telebot.types.InlineKeyboardButton("Контакты")
# keyboard5.row = (butn1, butn2, butn3, butn4, bunt5, bunt6, butn7)
keyboard6 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard6.row('ЗАКРЫТЬ ЗАЯВКУ', )
keyboard7 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard7.row('ПРОЙТИ РЕГИСТРАЦИЮ', )
keyboard11 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard11.row('ПРОЙТИ ОБУЧЕНИЕ', 'УЗНАТЬ ОБ ОСТАЛЬНЫХ УРОВНЯХ')
keyboard8 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard8.row('ДАЛЕЕ')
keyboard9 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard9.row('ПРОЙТИ ТЕСТ')
keyboard10 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard10.row('ПОЛУЧИТЬ ВСЕ ЗАЯВКИ',
               'ВЫБРАТЬ КАТЕГОРИЮ')
keyboard12 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard12.row('Не проводилось')
keyboard13 = telebot.types.ReplyKeyboardMarkup()
keyboard13.row('не соответствует, но очень хочет',
               'есть понимание и способности к обучению',
               'полностью соответствует: опыт и квалификация согласно заявке'
               )
keyboard14 = telebot.types.ReplyKeyboardMarkup()
keyboard14.row('ОТКЛОНИТЬ',
               'ТРУДОУСТРОИТЬ',
               'Подтвердить выход'
               )
keyboard15 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard15.row('аудио', 'видео')
all_answers_dict = {'Telegram': 'Telegram', 'Соцсети, работные сайты': 'Соцсети, работные сайты',
                    'На рынке': 'На рынке',
                    'Сайты знакомств': 'Сайты знакомств', 'Дам объявление': 'Дам объявление', 'Переманю': 'Переманю',
                    'Проведу телефонное интер': 'Проведу телефонное интервью',
                    'Созвонюсь по видео связи': 'Созвонюсь по видео связи',
                    'Встречусь вживую при нео': 'Встречусь вживую при необходимости',
                    'Только пообщаюсь по пере': 'Только пообщаюсь по переписке',
                    'Быть ИП': 'Быть ИП',
                    'Иметь юр лицо': 'Иметь юр лицо',
                    'Открыть самозанятость': 'Открыть самозанятость',
                    'Быть фрилансером': 'Быть фрилансером'
                    }

pay_level_list = {'LIGHT': [0, 0], 'MEDIUM': [1, 5000], 'HARD': [5000, 10000], 'PRO': [10000, 100000]}


def get_nickname(numb):
    nick = '@nickname' + str(numb)
    phone = '+79' + str(random.randint(100000000, 999999999))
    return random.choice([nick, phone])


'''for i in range(100):
    key = random.choice(list(pay_level_list.keys()))
    value = random.randint(pay_level_list[key][0], pay_level_list[key][1])
    session.add(form(user_id =i, vacancy = 'Тестовая вакансия {0}'.format(str(i)), duties ='Выполнять работу {0}'.format(str(i)), requirements ='необходимые требования{0}'.format(str(i)), conditions = 'необходимые условия {0}'.format(str(i)),  pay_level =key, salary = value, nickname = get_nickname(i), active = True))
    session.commit()
    session.close()
print('done')'''

question_list1 = ['Telegram', 'Соцсети, работные сайты', 'На рынке', 'Сайты знакомств', 'Дам объявление', 'Переманю', ]
question_list2 = ['Проведу телефонное интер',
                  'Созвонюсь по видео связи',
                  'Встречусь вживую при нео',
                  'Только пообщаюсь по пере']
question_list3 = [
    'Быть ИП',
    'Иметь юр лицо',
    'Открыть самозанятость',
    'Быть фрилансером'
]


def get_quiz_table(ques_numb, workernumb):
    global reading
    reading = True
    if not writing:
        worker = session.query(workers).filter_by(user_id=workernumb).first()
        session.close()
        reading = False
        quiz_table = telebot.types.InlineKeyboardMarkup()
        quiz_answer_dict = {}
        if type(worker) != 'NoneType':
            if ques_numb == 1:
                TrueFalseList = [worker.first_test_1, worker.first_test_2, worker.first_test_3, worker.first_test_4,
                                 worker.first_test_5, worker.first_test_6]
                quiz_answer_dict = dict(zip(question_list1, TrueFalseList))
            elif ques_numb == 2:
                TrueFalseList = [worker.second_test_1, worker.second_test_2, worker.second_test_3, worker.second_test_4]
                quiz_answer_dict = dict(zip(question_list2, TrueFalseList))
            elif ques_numb == 3:
                TrueFalseList = [worker.third_test_1, worker.third_test_2, worker.third_test_3, worker.third_test_4]
                quiz_answer_dict = dict(zip(question_list3, TrueFalseList))
            for ques, answ in quiz_answer_dict.items():
                if quiz_answer_dict[ques]:
                    quiz_table.add(telebot.types.InlineKeyboardButton(text=ques, callback_data="answ" + ques),
                                   telebot.types.InlineKeyboardButton(text='✅', callback_data=ques))
                else:
                    quiz_table.add(telebot.types.InlineKeyboardButton(text=ques, callback_data="answ" + ques),
                                   telebot.types.InlineKeyboardButton(text='❌', callback_data=ques))
            if ques_numb == 3:
                quiz_table.add(telebot.types.InlineKeyboardButton(text='Результат', callback_data="Accept"))
            else:
                quiz_table.add(telebot.types.InlineKeyboardButton(text='Далее', callback_data="Accept"))
        reading = False
        return quiz_table


def get_test_dict(ques_numb, workernumb):
    if not writing:
        global reading
        reading = True
        worker = session.query(workers).filter_by(user_id=workernumb).first()
        session.close()
        quiz_answer_dict = {}
        if type(worker) != 'NoneType':
            if ques_numb == 1:
                TrueFalseList = [worker.first_test_1, worker.first_test_2, worker.first_test_3, worker.first_test_4,
                                 worker.first_test_5, worker.first_test_6]
                quiz_answer_dict = dict(zip(question_list1, TrueFalseList))
            elif ques_numb == 2:
                TrueFalseList = [worker.second_test_1, worker.second_test_2, worker.second_test_3, worker.second_test_4]
                quiz_answer_dict = dict(zip(question_list2, TrueFalseList))
            elif ques_numb == 3:
                TrueFalseList = [worker.third_test_1, worker.third_test_2, worker.third_test_3, worker.third_test_4]
                quiz_answer_dict = dict(zip(question_list3, TrueFalseList))
        reading = False
        return quiz_answer_dict
    else:
        return "processing"


def change_true_false(question, workernumb):
    if not reading:
        global writing
        writing = True
        worker = session.query(workers).filter_by(user_id=workernumb).first()
        if question == 'Telegram':
            worker.first_test_1 = not worker.first_test_1
            session.commit()
            session.close()
        elif question == 'Соцсети, работные сайты':
            worker.first_test_2 = not worker.first_test_2
            session.commit()
            session.close()
        elif question == 'На рынке':
            worker.first_test_3 = not worker.first_test_3
            session.commit()
            session.close()
        elif question == 'Сайты знакомств':
            worker.first_test_4 = not worker.first_test_4
            session.commit()
            session.close()
            sleep(1)
        elif question == 'Дам объявление':
            worker.first_test_5 = not worker.first_test_5
            session.commit()
            session.close()
        elif question == 'Переманю':
            worker.first_test_6 = not worker.first_test_6
            session.commit()
            session.close()
        elif question == 'Проведу телефонное интер':
            worker.second_test_1 = not worker.second_test_1
            session.commit()
            session.close()
        elif question == 'Созвонюсь по видео связи':
            worker.second_test_2 = not worker.second_test_2
            session.commit()
            session.close()
        elif question == 'Встречусь вживую при нео':
            worker.second_test_3 = not worker.second_test_3
            session.commit()
            session.close()
        elif question == 'Только пообщаюсь по пере':
            worker.second_test_4 = not worker.second_test_4
            session.commit()
            session.close()
        elif question == 'Быть ИП':
            worker.third_test_1 = not worker.third_test_1
            session.commit()
            session.close()
        elif question == 'Иметь юр лицо':
            worker.third_test_2 = not worker.third_test_2
            session.commit()
            session.close()
        elif question == 'Открыть самозанятость':
            worker.third_test_3 = not worker.third_test_3
            session.commit()
            session.close()
        elif question == 'Быть фрилансером':
            worker.third_test_4 = not worker.third_test_4
            session.commit()
            session.close()
        writing = False


@bot.message_handler(commands=['start'])
def get_start_message(message):
    work_list = session.query(workers).filter_by(user_id=message.from_user.id, done=False).all()
    if len(work_list) > 0:
        for work in work_list:
            session.delete(work)
            session.commit()
            session.close()
    form_request_list = session.query(form).filter_by(user_id=message.from_user.id, done=False).all()
    if len(form_request_list) > 0:
        for form_request in form_request_list:
            session.delete(form_request)
            session.commit()
            session.close()
    bot.send_message(message.from_user.id, 'Выберите категорию:', reply_markup=keyboard1)


@bot.message_handler(commands=['confirm'])
def confirm(message):
    bot.send_message(message.from_user.id, 'Следующие кандидаты ожидают подтверждения выхода от работодателя:')
    candidates_list = session.query(candidates).filter_by(worker_id=message.from_user.id, exit_proof = False).all()
    for candid in candidates_list:
        if candid.contact != 'wait' and candid.contact != '':
            bot.send_message(message.from_user.id, '''Имя кандидата: {0}'''.format(candid.name))


@bot.message_handler(commands=['myforms'])
def get_start_message(message):
    worker = session.query(workers).filter_by(user_id=message.from_user.id).first()
    bot.send_message(message.from_user.id, 'Вы взяли в работу следующие заявки:')
    for form_id in worker.list_of_forms.split():
        form_s = session.query(form).get(form_id)
        form_button = telebot.types.InlineKeyboardMarkup()
        form_button.add(
            telebot.types.InlineKeyboardButton(text='ПРЕДЛОЖИТЬ КАНДИДАТА',
                                               callback_data='candidate' + ' ' + str(form_s.id)))
        bot.send_message(message.from_user.id, '''Заявка:
                Номер заявки: {0},
                Работодатель:{7},
                Наименование вакансии: {1},
                Категория: {9},
                Обязанности: {2},
                Требования: {3},
                Условия работы: {4},
                Сумма вознаграждения: {6},
                Взято в работу рекрутерами: {8}.
                '''.format(
            str(form_s.id),
            form_s.vacancy,
            form_s.duties,
            form_s.requirements,
            form_s.conditions,
            form_s.pay_level,
            str(form_s.salary),
            form_s.nickname,
            form_s.recruiter_count,
            worker.closed_tasks,
            str(3 - worker.closed_tasks),
            str(form_s.category,),
        ), reply_markup=form_button)


@bot.message_handler(commands=['forms'])
def get_start_message(message):
    forms = session.query(form).filter_by(user_id=message.from_user.id).all()
    bot.send_message(message.from_user.id, 'Ваши созданные вакансии:')
    for form_s in forms:
        form_button = telebot.types.InlineKeyboardMarkup()
        form_button.add(
            telebot.types.InlineKeyboardButton(text='Удалить заявку',
                                               callback_data='delete_from' + ' ' + str(form_s.id)))
        bot.send_message(message.from_user.id, '''Заявка:
                Номер заявки: {0},
                Работодатель:{7},
                Наименование вакансии: {1},
                Категория: {9},
                Обязанности: {2},
                Требования: {3},
                Условия работы: {4},
                Сумма вознаграждения: {6},
                Взято в работу рекрутерами: {8}.
                '''.format(
            str(form_s.id),
            form_s.vacancy,
            form_s.duties,
            form_s.requirements,
            form_s.conditions,
            form_s.pay_level,
            str(form_s.salary),
            form_s.nickname,
            form_s.recruiter_count,
            str(form_s.category, ),
        ), reply_markup=form_button)


@bot.message_handler(content_types=['text'])
def application_form(message):
    if message.text == 'РАБОТАДАТЕЛЬ':
        bot.send_message(message.from_user.id,
                         'Не тратьте время на поиск сотрудников. Делегируйте. Рекрутеры займутся этим вопросом за вас.',
                         reply_markup=keyboard2)
    if message.text == 'ЗАПОЛНИТЬ ЗАЯВКУ':
        session.add(form(user_id=message.from_user.id, category='wait'))
        session.commit()
        session.close()
        bot.send_message(message.from_user.id, 'Введите категорию вакансии')

    elif len(session.query(form).filter_by(user_id=message.from_user.id, category='wait').all()) > 0:  # done
        session.close()
        current_form = session.query(form).filter_by(user_id=message.from_user.id, category='wait').first()
        current_form.category = message.text[0].upper() + message.text[1:len(message.text)].lower()
        current_form.vacancy = 'wait'
        session.commit()
        session.close()
        bot.send_message(message.from_user.id, 'Введите название вакансии')

    elif len(session.query(form).filter_by(user_id=message.from_user.id, vacancy='wait').all()) > 0:  # done
        session.close()
        current_form = session.query(form).filter_by(user_id=message.from_user.id, vacancy='wait').first()
        current_form.vacancy = message.text
        current_form.duties = 'wait'
        session.commit()
        session.close()
        bot.send_message(message.from_user.id, 'Введите обязанности работающего')

    elif len(session.query(form).filter_by(user_id=message.from_user.id, duties='wait').all()) > 0:  # done
        session.close()
        current_form = session.query(form).filter_by(user_id=message.from_user.id, duties='wait').first()
        current_form.duties = message.text
        current_form.requirements = 'wait'
        session.commit()
        session.close()
        bot.send_message(message.from_user.id, 'Введите требования для работающего')

    elif len(session.query(form).filter_by(user_id=message.from_user.id, requirements='wait').all()) > 0:  # done
        session.close()
        current_form = session.query(form).filter_by(user_id=message.from_user.id, requirements='wait').first()
        current_form.requirements = message.text
        current_form.conditions = 'wait'
        session.commit()
        session.close()
        bot.send_message(message.from_user.id, 'Введите условия работы')
    elif len(session.query(form).filter_by(user_id=message.from_user.id, conditions='wait').all()) > 0:  # done
        session.close()
        current_form = session.query(form).filter_by(user_id=message.from_user.id, conditions='wait').first()
        current_form.conditions = message.text
        current_form.pay_level = 'wait'
        session.commit()
        session.close()
        bot.send_message(message.from_user.id, '''Выберите уровень оплаты.
        LIGHT (бесплатно), 
        MEDIUM (до 5000 руб.), 
        HARD (от 5000 до 10000 руб.), 
        PRO (выше 10000 руб.)
        ''', reply_markup=keyboard3)

    elif len(session.query(form).filter_by(user_id=message.from_user.id, pay_level='wait').all()) > 0:  # done
        session.close()
        current_form = session.query(form).filter_by(user_id=message.from_user.id, pay_level='wait').first()
        if message.text == 'LIGHT':
            current_form.pay_level = message.text
            current_form.salary = 0
            current_form.nickname = 'wait'
            session.commit()
            session.close()
            bot.send_message(message.from_user.id,
                             'В соотвествии с выбранным уровнем оплаты, вознаграждения работающему не предусмотрено. Введите ваш никнейм или номер телефон для контакта с работающим')
        else:
            current_form.pay_level = message.text
            current_form.salary = -100000
            session.commit()
            session.close()
            bot.send_message(message.from_user.id, 'Введите сумму вознаграждения')
    elif len(session.query(form).filter_by(user_id=message.from_user.id, salary=-100000).all()) > 0:  # done
        session.close()
        current_form = session.query(form).filter_by(user_id=message.from_user.id, salary='wait').first()
        try:
            salary = int(message.text)
            salaryflag = True
        except ValueError:
            salaryflag = False
            bot.send_message(message.from_user.id, 'Введите вознаграждение одним числом без букв')
        if salaryflag:
            if current_form.pay_level == 'MEDIUM':
                if salary > 5000 or (salary < 1):
                    bot.send_message(message.from_user.id,
                                     'вознаграждение рукретеру уровня MEDIUM от 1 до 5000 руб. Проверьте сумму и повторите отправку.')
                else:
                    current_form.salary = salary
                    current_form.nickname = 'wait'
                    session.commit()
                    session.close()
                    bot.send_message(message.from_user.id,
                                     'Введите ваш никнейм или номер телефон для контакта с работающим')
            elif current_form.pay_level == 'HARD':
                if salary < 5000 or salary > 10000:
                    bot.send_message(message.from_user.id,
                                     'вознаграждение рукретеру уровня HARD от 5000 до 10000 руб. Проверьте сумму и повторите отправку.')
                else:
                    current_form.salary = salary
                    current_form.nickname = 'wait'
                    session.commit()
                    session.close()
                    bot.send_message(message.from_user.id,
                                     'Введите ваш никнейм или номер телефон для контакта с работающим')
            elif current_form.pay_level == 'PRO':
                if salary < 10000:
                    bot.send_message(message.from_user.id,
                                     'вознаграждение рукретеру уровня PRO от 10000 руб. Проверьте сумму и повторите отправку.')
                else:
                    current_form.salary = salary
                    current_form.nickname = 'wait'
                    session.commit()
                    session.close()
                    bot.send_message(message.from_user.id,
                                     'Введите ваш никнейм или номер телефон для контакта с работающим')
    elif len(session.query(form).filter_by(user_id=message.from_user.id, nickname='wait').all()) > 0:
        session.close()
        current_form = session.query(form).filter_by(user_id=message.from_user.id, nickname='wait').first()
        current_form.nickname = message.text
        current_form.just_finished = True
        session.commit()
        session.close()
        form_request = session.query(form).filter_by(user_id=message.from_user.id, just_finished=True).first()
        form_request.just_finished = False
        bot.send_message(message.from_user.id, '''Ваша форма:
Номер вакансии: {0},
Название вакансии: {1},
Категория: {8},
Обязанности: {2},
Требования: {3},
Условия работы: {4},
Уровень оплаты: {5},
Сумма вознаграждения: {6},
Никнейм или номер телефона для связи: {7},
        '''.format(
            str(form_request.id),
            form_request.vacancy,
            form_request.duties,
            form_request.requirements,
            form_request.conditions,
            form_request.pay_level,
            str(form_request.salary),
            form_request.nickname,
            form_request.category,
        ), reply_markup=keyboard4)
        form_request.active = False
        session.commit()
        session.close()

    elif message.text == 'Запустить подбор':

        form_request = session.query(form).filter_by(user_id=message.from_user.id, active=False).first()
        form_request.done = True
        form_request.active = True
        form_button = telebot.types.InlineKeyboardMarkup()
        form_button.add(
            telebot.types.InlineKeyboardButton(text='Удалить заявку',
                                               callback_data='delete_from' + ' ' + str(form_request.id)))
        bot.send_message(message.from_user.id,
                         'заявка №{0} {1} добавлена в выдачу. Введите /start чтобы создать новую вакансию. Чтобы удалить заявку нажмите кнопку <Удалить заявку>. Чтобы просмотреть созданные вами заявки введите /forms'.format(
                             str(form_request.id), form_request.vacancy, ), reply_markup=form_button)
        session.commit()
        session.close()



    elif message.text == 'РЕКРУТЕР':
        if len(session.query(workers).filter_by(user_id=message.from_user.id).all()) == 0:
            bot.send_message(message.from_user.id,
                             'Заработай больше на поиске персонала. Закрывай заявки в любое время. Делай то, что тебе нравится.',
                             reply_markup=keyboard7)
        else:
            bot.send_message(message.from_user.id,
                             'Вы уже зарегистрированы. Для получения вакансий нажмите ПОЛУЧИТЬ ЗАЯВКИ.',
                             reply_markup=keyboard10)
    elif message.text == 'ПРОЙТИ РЕГИСТРАЦИЮ':

        bot.send_message(message.from_user.id,
                         '''Твой уровень LIGHT
Закрой 3 позиции от разных работодателей по заявке уровня LIGHT (без оплаты) и переходи на следующий уровень. 
''',
                         reply_markup=keyboard11)
    elif message.text == 'ПРОЙТИ ОБУЧЕНИЕ':
        if len(session.query(workers).filter_by(user_id=message.from_user.id).all()) == 0:
            session.add(workers(user_id=message.from_user.id))
            worker = session.query(workers).filter_by(user_id=message.from_user.id).first()
            worker.educ_lvl = 1
            session.commit()
            session.close()
            bot.send_message(message.from_user.id,
                             '''Мир поделен на две части: тот, кто предлагает работу, и тот, кто эту работу выполняет. Рекрутер относится ко второй категории. Мы с вами выполняем работу по поиску людей, которые согласны выполнять работу тех, кто ее предоставляет.
    Требуется понимать - насколько качественно мы выполним нашу с вами работу и как быстро предоставим нужного человека – от этого зависит наше будущее, как профессионала.
    ''',
                             reply_markup=keyboard8)
    elif message.text == 'УЗНАТЬ ОБ ОСТАЛЬНЫХ УРОВНЯХ':

        bot.send_message(message.from_user.id,
                         '''MEDIUM – заявки стоимостью до 5000 руб. Переход при закрытии 3-х бесплатных заявок от разных работодателей на уровне LIGHT.
HARD – заявки стоимостью от 5000 до 10000 руб. Переход при закрытии 7-ми заявок разных работодателей на уровне MEDIUM.
PRO – заявки стоимостью от 10000 руб. Переход при закрытии 10-ти заявок любых работодателей на уровне HARD.
''',
                         reply_markup=keyboard11)
    elif message.text == 'ДАЛЕЕ':
        worker = session.query(workers).filter_by(user_id=message.from_user.id).first()
        if worker.educ_lvl == 1:
            worker.educ_lvl = 2
            session.commit()
            session.close()
            bot.send_message(message.from_user.id,
                             '''Сейчас искать людей гораздо проще, когда мир технологий развит и продолжает развиваться. Использовать можно все возможные ресурсы:
- во-первых, telegram. Есть множество сообществ, где общаются специалисты той или иной области. Подписываемся на их группы и каналы и общаемся с ними от лица представителя работодателя. Кто-то да откликнется.
- социальные сети. Технология та же – используем тематические группы и форумы и находим тех, кого заинтересуют наши предложения.
- специализированные площадки, сайты по поиску работы. Сейчас их множество, но многие могут быть платными. Их можно использовать, но нужно быть готовыми платить за услуги по предоставлению резюме.
- сайты знакомств. Даже такие сайты имеются в инструментах профессионального рекрутера. Можно завязывать диалог, а затем плавно переходить к предложению по работе. Если попадете в бан, то ничего страшного. Поверьте, многие, обдумав потом предложение, соглашаются на оффер.
- ну и конечно печатные СМИ и объявления на местных досках. Сколько бы людей не пользовалось интернетом, иногда выгоднее наклеить объявление на остановке и получить требуемый отклик.
- прямой поиск. Когда мы точно знаем, где находится требуемый специалист, и пытаемся его переманить. Обычно это уже уровень PRO, но и новички бывают проворными.
''',
                             reply_markup=keyboard8)
        elif worker.educ_lvl == 2:
            worker.educ_lvl += 1
            session.commit()
            session.close()
            bot.send_message(message.from_user.id,
                             '''Прежде, чем направить кандидата на рассмотрение рекрутер использует три проверенных шага:
- первичное интервью. Свяжитесь с кандидатом по аудиосвязи, чтобы задать несколько вопросов в рамках заявки. Прежде, выпишите себе вопросы, которые будете задавать.
- проведите видеовстречу. Используйте любую платформу для видеоконференций, например, вы можете воспользоваться видео-звонком в telegram или сейчас очень популярен zoom. Оцените для себя кандидата и попробуйте понять понравится ли он будущему работодателю.
- есть возможность встретиться – пригласите в кафе или к себе в офис. Разговор лучше переписки, встреча вживую - лучше общения онлайн.
Поняли, что сами взяли бы такого сотрудника к себе – направляйте работодателю на оценку и дальнейшее решение по трудоустройству.
''',
                             reply_markup=keyboard8)
        elif worker.educ_lvl == 3:
            worker.educ_lvl += 1
            session.commit()
            session.close()
            bot.send_message(message.from_user.id,
                             '''Самый простой и популярный инструмент для проведения онлайн встреч это zoom. Используйте его в работе. Инструкция по работе с zoom (ссылка на видео).''',
                             reply_markup=keyboard8)

        elif worker.educ_lvl == 4:
            worker.educ_lvl = 5
            session.commit()
            session.close()
            bot.send_message(message.from_user.id,
                             '''Если ты еще никак не оформил свою деятельность, для уплаты налогов, то для перехода на второй и последующие уровни, где ты сможешь принимать оплату за закрытие заявки, тебе нужно открыть самозанятость. Это не сложно и не потребует от тебя никаких затрат. Наоборот, позволит работать уверенно. Инструкция по открытию самозанятости (ссылка на видео).
Для перехода на уровень MEDIUM выберите команду: Мой уровень
И приложите фото паспорта, свидетельство о регистрации ИП или справку о самозанятости.
Повышение на следующие уровни производится автоматически.
''',
                             reply_markup=keyboard9)
    # рекрутер
    elif message.text == 'ПРОЙТИ ТЕСТ' and session.query(workers).filter_by(
            user_id=message.from_user.id).first().educ_lvl == 5:
        worker = session.query(workers).filter_by(user_id=message.from_user.id).first()
        worker.educ_lvl = 6
        worker.test_stage = 1
        session.commit()
        session.close()
        bot.send_message(message.from_user.id, '''Вопрос 1. Чтобы отметить вариант ответа как правильный нажмите на крестик и ждите когда он изменится на галочку. Для подтверждение вариантов ответа нажмите кнопку "Далее" 


        Я буду искать кандидатов:''',
                         reply_markup=get_quiz_table(1, message.from_user.id))

    #получение заявок
    elif message.text == 'ПОЛУЧИТЬ ВСЕ ЗАЯВКИ' and session.query(workers).filter_by(
        user_id=message.from_user.id).first().test_stage == 4:
        bot.send_message(message.from_user.id, 'В соответствии с вашим уровнем доступны следующие заявки:')
        worker = session.query(workers).filter_by(user_id=message.from_user.id).first()
        worker_level = worker.level
        for s_form in session.query(form).filter_by(pay_level=worker_level).all():
            form_buttons = telebot.types.InlineKeyboardMarkup()
            form_buttons.add(
                telebot.types.InlineKeyboardButton(text='ВЗЯТЬ В РАБОТУ', callback_data='work' + ' ' + str(s_form.id)),
                telebot.types.InlineKeyboardButton(text='ПРЕДЛОЖИТЬ КАНДИДАТА',
                                                   callback_data='candidate' + ' ' + str(s_form.id)))
            bot.send_message(message.from_user.id, '''Заявка:
            Номер заявки: {0},
            Работодатель:{7},
            Наименование вакансии: {1},
            Категория: {11},
            Обязанности: {2},
            Требования: {3},
            Условия работы: {4},
            Сумма вознаграждения: {6},
            Взято в работу рекрутерами: {8}.
            Ваш уровень: закрытых заявок {9} ({10} заявки до перехода на уровень MEDIUM)
                    '''.format(
                str(s_form.id),
                s_form.vacancy,
                s_form.duties,
                s_form.requirements,
                s_form.conditions,
                s_form.pay_level,
                str(s_form.salary),
                s_form.nickname,
                s_form.recruiter_count,
                worker.closed_tasks,
                str(3 - worker.closed_tasks),
                s_form.category,
            ), reply_markup=form_buttons)
    elif message.text == 'ВЫБРАТЬ КАТЕГОРИЮ' and session.query(workers).filter_by(
        user_id=message.from_user.id).first().test_stage == 4:
        bot.send_message(message.from_user.id, "Доступные на данный момент категории")
        categories = set(session.query(form.category).all())
        for cat in categories:
            cat_button = telebot.types.InlineKeyboardMarkup()
            cat_button.add(
                telebot.types.InlineKeyboardButton(text='ВЫБРАТЬ ДАННУЮ КАТЕГОРИЮ',
                                                   callback_data='category+' + str(cat[0])))
            bot.send_message(message.from_user.id, str(cat[0]), reply_markup=cat_button)





    # Рабочий
    elif len(session.query(candidates).filter_by(worker_id=message.from_user.id, contact='wait').all()) > 0:
        session.close()
        recrut = session.query(candidates).filter_by(contact='wait').first()
        recrut.contact = message.text
        form_id = recrut.id_form
        s_form = session.query(form).filter_by(id=form_id).first()
        s_form.active = False
        session.commit()
        worker_list = session.query(workers).all()
        recruter_buttons = telebot.types.InlineKeyboardMarkup()
        recruter_buttons.add(telebot.types.InlineKeyboardButton(text='Статус заявки',
                                                                callback_data='proof_request' + ' ' + str(
                                                                    recrut.worker_id) + ' ' + str(
                                                                    recrut.id) + ' ' + str(form_id)))
        employee_buttons = telebot.types.InlineKeyboardMarkup()
        employee_buttons.add(telebot.types.InlineKeyboardButton(text='Подтвердить выход',
                                                                callback_data='proof_exit' + ' ' + str(
                                                                    recrut.worker_id) + ' ' + str(
                                                                    recrut.id) + ' ' + str(form_id)))

        for work in worker_list:
            if form_id in work.list_of_forms.split():
                worker_id = work.id
                list_forms = work.list_of_forms.split()
                list_forms.remove(form_id)
                work.list_of_forms = ' '.join(list_forms)
                bot.send_message(int(worker_id), '''Заявка закрыта. Вакансия: 
                Номер заявки: {0},
                Работодатель:{7},
                Наименование вакансии: {1},
                Категория: {8},
                Обязанности: {2},
                Требования: {3},
                Условия работы: {4},
                Сумма вознаграждения: {6},'''.format(
                    str(s_form.id),
                    s_form.vacancy,
                    s_form.duties,
                    s_form.requirements,
                    s_form.conditions,
                    s_form.pay_level,
                    str(s_form.salary),
                    s_form.nickname,
                    s_form.category, ))
                session.commit()
        bot.send_message(s_form.user_id, '''Рекрутер передал вам контакты работника:
{0}
Вакансия: 
Номер заявки: {1},
Категория: {8},
Наименование вакансии: {3},
Обязанности: {4},
Требования: {5},
Условия работы: {6},
Сумма вознаграждения: {7}.
Нажмите <Подтвердить выход> как только работник выйдет на работу. Чтобы посмотреть заявки, ожидающие подтверждения выхода введите /proof
'''.format(message.text, str(s_form.id),
           s_form.vacancy,
           s_form.duties,
           s_form.requirements,
           s_form.conditions,
           s_form.pay_level,
           str(s_form.salary),
           s_form.category,), reply_markup=employee_buttons)
        bot.send_message(message.from_user.id,
                         'Контакты работника переданы работодателю. Чтобы проверить подтвержден ли выход работника нажмите <Статус заявки>. Чтобы посмотреть заявки, ожидающие подтверждения выхода введите /confirm',
                         reply_markup=recruter_buttons)
        session.close()
    elif len(session.query(candidates).filter_by(worker_id=message.from_user.id, name='wait').all()) > 0:
        session.close()
        recrut = session.query(candidates).filter_by(name='wait').first()
        recrut.name = message.text
        recrut.interview = 'wait'
        session.commit()
        session.close()
        bot.send_message(message.from_user.id, 'Опишите итоги интервью', reply_markup=keyboard12)

    elif len(session.query(candidates).filter_by(worker_id=message.from_user.id, interview='wait').all()) > 0:
        session.close()
        recrut = session.query(candidates).filter_by(interview='wait').first()
        recrut.interview = message.text
        recrut.video_review = 'wait'
        session.commit()
        session.close()
        bot.send_message(message.from_user.id, 'Опишите итоги видео конференции', reply_markup=keyboard12)

    elif len(session.query(candidates).filter_by(worker_id=message.from_user.id, video_review='wait').all()) > 0:
        session.close()
        recrut = session.query(candidates).filter_by(video_review='wait').first()
        recrut.video_review = message.text
        recrut.meeting_result = 'wait'
        session.commit()
        session.close()
        bot.send_message(message.from_user.id, 'Опишите итоги встречи', reply_markup=keyboard12)

    elif len(session.query(candidates).filter_by(worker_id=message.from_user.id, link_wait=True).all()) > 0:
        session.close()
        recrut = session.query(candidates).filter_by(worker_id=message.from_user.id, link_wait=True).first()
        recrut.link_wait = False
        s_form = session.query(form).filter_by(id = recrut.id_form).first(
        )
        employee_id = s_form.user_id
        session.commit()
        session.close()
        bot.send_message(employee_id, 'Встреча готова, прошу присоединиться: {0}'.format(message.text))

    elif len(session.query(candidates).filter_by(worker_id=message.from_user.id, meeting_result='wait').all()) > 0:
        session.close()
        recrut = session.query(candidates).filter_by(meeting_result='wait').first()
        recrut.meeting_result = message.text
        recrut.mark = 'wait'
        session.commit()
        session.close()
        bot.send_message(message.from_user.id, 'Оценка кандидата на соответствие предлагаемой должности',
                         reply_markup=keyboard13)

    elif len(session.query(candidates).filter_by(worker_id=message.from_user.id, mark='wait').all()) > 0:
        session.close()
        recrut = session.query(candidates).filter_by(mark='wait').first()
        recrut.mark = message.text
        session.commit()
        if recrut.interview == 'Не проводилось' and recrut.meeting_result == 'Не проводилось' and recrut.video_review == 'Не проводилось':
            bot.send_message(message.from_user.id, ''' Заявка не отправлена. Сначала
 пообщайтесь с кандидатом в любом из форматов и напишите работодателю о результате вашего общения.''')
            session.delete(recrut)
            session.commit()
        else:
            bot.send_message(message.from_user.id, 'Заявка отправлена работадателю')
            employee_id = session.query(form).filter_by(id=recrut.id_form).first().user_id
            form_id = recrut.id_form
            worker_closed_tasks = session.query(workers).filter_by(user_id=recrut.worker_id).first().closed_tasks
            employee_buttons = telebot.types.InlineKeyboardMarkup()
            employee_buttons.add(telebot.types.InlineKeyboardButton(text='СОБЕСЕДОВАТЬ',
                                                                    callback_data='interview' + ' ' + str(
                                                                        employee_id) + ' ' + str(
                                                                        recrut.worker_id) + ' ' + str(
                                                                        recrut.id) + ' ' + str(form_id)),
                                 telebot.types.InlineKeyboardButton(text='КАЛЕНДАРЬ» ',
                                                                    callback_data='calendar' + ' ' + str(
                                                                        employee_id) + ' ' + str(
                                                                        recrut.worker_id) + ' ' + str(
                                                                        recrut.id) + ' ' + str(form_id)))
            employee_buttons.add(telebot.types.InlineKeyboardButton(text='«ОТКЛОНИТЬ»',
                                                                    callback_data='refuse' + ' ' + str(
                                                                        employee_id) + ' ' + str(
                                                                        recrut.worker_id) + ' ' + str(
                                                                        recrut.id) + ' ' + str(form_id)),
                                 telebot.types.InlineKeyboardButton(text='«ТРУДОУСТРОИТЬ»» ',
                                                                    callback_data='take' + ' ' + str(
                                                                        employee_id) + ' ' + str(
                                                                        recrut.worker_id) + ' ' + str(
                                                                        recrut.id) + ' ' + str(form_id)), )

            bot.send_message(employee_id, '''На вашу заявку откликнулись. 
''' + '''Имя кандидата: {0}
Итоги интервью: {1},
Итоги видео конференции: {2},
Итоги встречи: {3},
Оценка кандидата на соответствие предлагаемой должности:  {4}.
Уровень рекрутера: закрытых заявок {5}.
'''.format(recrut.name, recrut.interview, recrut.video_review, recrut.meeting_result, recrut.mark, worker_closed_tasks),
                             reply_markup=employee_buttons)


@bot.callback_query_handler(func=lambda call: True)
def get_callback(call):
    if call.data in question_list1:
        test_dict = get_test_dict(1, call.from_user.id)
        if test_dict != "processing":
            for key in test_dict:
                if call.data == key:
                    change_true_false(key, call.from_user.id)
                    bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.message_id,
                                                  reply_markup=get_quiz_table(1, call.from_user.id))
                    break
    elif call.data.split()[0] == 'proof_exit':
        candidate = session.query(candidates).filter_by(id = call.data.split()[2]).first()
        candidate.exit_proof = True
        s_form = session.query(form).filter_by(id = call.data.split()[3]).first()
        worker = session.query(workers).filter_by(user_id = call.data.split()[1]).first()
        worker.closed_tasks = worker.closed_tasks + 1
        if worker.closed_tasks == 3:
            worker.level = 'MEDIUM'
        elif worker.closed_tasks == 10:
            worker.level = 'HARD'
        elif worker.closed_tasks == 20:
            worker.level = 'PRO'
        session.commit()
        bot.send_message(call.data.split()[1], '''Выход вашего кандидата {0} подтверждён.  Вакансия: 
                Номер заявки: {1},
                Работодатель:{2},
                Категория: {8},
                Наименование вакансии: {3},
                Обязанности: {4},
                Требования: {5},
                Условия работы: {6},
                Сумма вознаграждения: {7},'''.format(
            candidate.name,
            str(s_form.id),
           s_form.vacancy,
           s_form.duties,
           s_form.requirements,
           s_form.conditions,
           s_form.pay_level,
           str(s_form.salary,),
        s_form.category,))

        session.delete(s_form)
        session.commit()
        bot.send_message(call.from_user.id, 'Выход кандидата подтвержден')
        session.close()
    elif call.data.split()[0] == 'interview':
        interview_buttons = telebot.types.InlineKeyboardMarkup()
        interview_buttons.add(telebot.types.InlineKeyboardButton(text='аудио',
                                                                 callback_data='audio' + ' ' + ' '.join(
                                                                     call.data.split()[1:])),
                              telebot.types.InlineKeyboardButton(text='видео» ',
                                                                 callback_data='video' + ' ' + ' '.join(
                                                                     call.data.split()[1:])))
        bot.send_message(call.from_user.id, 'Выберите формат собеседования', reply_markup=interview_buttons)
    elif call.data.split()[0] == 'calendar':
        interview_buttons = telebot.types.InlineKeyboardMarkup()
        interview_buttons.add(telebot.types.InlineKeyboardButton(text='аудио',
                                                                 callback_data='calendar_audio' + ' ' + ' '.join(
                                                                     call.data.split()[1:])),
                              telebot.types.InlineKeyboardButton(text='видео» ',
                                                                 callback_data='calendar_video' + ' ' + ' '.join(
                                                                     call.data.split()[1:])))
        bot.send_message(call.from_user.id, 'Выберите формат собеседования', reply_markup=interview_buttons)
    elif call.data.split()[0] == 'audio':
        s_form = session.query(form).filter_by(id = int(call.data.split()[4])).first()
        interview_buttons = telebot.types.InlineKeyboardMarkup()
        interview_buttons.add(telebot.types.InlineKeyboardButton(text='Собеседовать',
                                                                 callback_data='recrut_accept' + ' ' + ' '.join(
                                                                     call.data.split()[1:])))
        bot.send_message(call.data.split()[2], 'Работодатель вакансии {0} {1} готов к аудио встрече в ближайшее время.'.format(s_form.id, s_form.vacancy), reply_markup=interview_buttons)
    elif call.data.split()[0] == 'video':
        s_form = session.query(form).filter_by(id = int(call.data.split()[4]))
        interview_buttons = telebot.types.InlineKeyboardMarkup()
        interview_buttons.add(telebot.types.InlineKeyboardButton(text='Собеседовать',
                                                                 callback_data='recrut_accept' + ' ' + ' '.join(
                                                                     call.data.split()[1:])))
        bot.send_message(call.data.split()[2], 'Работодатель вакансии {0} {1} готов к видео встрече в ближайшее время.'.format(s_form.id, s_form.vacancy), reply_markup=interview_buttons)


    elif call.data.split()[0] == 'recrut_accept':
        recrut = session.query(candidates).filter_by(worker_id = call.from_user.id).first()
        recrut.link_wait = True
        session.commit()
        session.close()
        bot.send_message(call.from_user.id, 'Введите ссылку на конференцию')

    elif call.data.split()[0] == 'delete_from':
        s_form = session.query(form).filter_by(id=int(call.data.split()[1])).first()
        session.delete(s_form)
        session.commit()
        session.close()
        bot.send_message(call.from_user.id, 'Вакансия удалена')

    elif call.data.split()[0] == 'contact':
        candid = session.query(candidates).filter_by(id=int(call.data.split()[3])).first()
        candid.contact = 'wait'
        session.commit()
        session.close()
        bot.send_message(call.from_user.id, 'Введите контакты работающего')

    elif call.data.split()[0] == 'take':
        if len(session.query(candidates).filter_by(id=int(call.data.split()[3])).all()) > 0:
            contact_buttons = telebot.types.InlineKeyboardMarkup()
            contact_buttons.add(telebot.types.InlineKeyboardButton(text='ПЕРЕДАТЬ КОНТАКТ',
                                                                   callback_data='contact' + ' ' + ' '.join(
                                                                       call.data.split()[1:])))

            candid = session.query(candidates).filter_by(id=int(call.data.split()[3])).first()
            s_form = session.query(form).filter_by(id=int(call.data.split()[4])).first()
            bot.send_message(int(call.data.split()[2]), '''Ваш кандидат соответствует заявке. Просьба передать контакт работодателю. Вакансия: 
                Номер заявки: {0},
                Работодатель:{7},
                Наименование вакансии: {1},
                Категория: {9},
                Обязанности: {2},
                Требования: {3},
                Условия работы: {4},
                Сумма вознаграждения: {6},
                Взято в работу рекрутерами: {8}.'''.format(
                str(s_form.id),
                s_form.vacancy,
                s_form.duties,
                s_form.requirements,
                s_form.conditions,
                s_form.pay_level,
                str(s_form.salary),
                s_form.nickname,
                s_form.recruiter_count,
                s_form.category), reply_markup=contact_buttons)
            bot.send_message(call.from_user.id, 'Вы приняли кандидата', )
            session.commit()
            session.close()
    elif call.data.split()[0] == 'refuse':
        if len(session.query(candidates).filter_by(id=int(call.data.split()[3])).all()) > 0:
            candid = session.query(candidates).filter_by(id=int(call.data.split()[3])).first()
            s_form = session.query(form).filter_by(id=int(call.data.split()[4])).first()
            bot.send_message(int(call.data.split()[2]), '''Ваш кандидат отклонен. Вакансия: 
                Номер заявки: {0},
                Работодатель:{7},
                Наименование вакансии: {1},
                Категория: {9},
                Обязанности: {2},
                Требования: {3},
                Условия работы: {4},
                Сумма вознаграждения: {6},
                Взято в работу рекрутерами: {8}.'''.format(
                str(s_form.id),
                s_form.vacancy,
                s_form.duties,
                s_form.requirements,
                s_form.conditions,
                s_form.pay_level,
                str(s_form.salary),
                s_form.nickname,
                s_form.recruiter_count,
                s_form.category))
            session.delete(candid)
            bot.send_message(call.from_user.id, 'Вы отклонили кандидата', )
            session.close()
    elif call.data in question_list2:
        test_dict = get_test_dict(2, call.from_user.id)
        if test_dict != "processing":
            for key in test_dict:
                if call.data == key:
                    change_true_false(key, call.from_user.id)
                    bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.message_id,
                                                  reply_markup=get_quiz_table(2, call.from_user.id))
                    break
    elif call.data in question_list3:
        test_dict = get_test_dict(3, call.from_user.id)
        if test_dict != "processing":
            for key in test_dict:
                if call.data == key:
                    change_true_false(key, call.from_user.id)
                    bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.message_id,
                                                  reply_markup=get_quiz_table(3, call.from_user.id))
                    break

    elif call.data.split()[0] == 'work':
        form_id = call.data.split()[1]
        form_s = session.query(form).get(form_id)
        vacancy_name = form_s.vacancy
        worker = session.query(workers).filter_by(user_id=call.from_user.id).first()
        set_of_forms = set(worker.list_of_forms.split())
        set_of_forms.add(str(form_id))
        str_of_forms = ' '.join(list(set_of_forms))
        worker.list_of_forms = str_of_forms
        active_forms_len = str(len(worker.list_of_forms.split()))
        session.commit()
        session.close()
        bot.send_message(call.from_user.id,
                         "Заявка №{0} {1} принята в работу. Всего заявок  работе {2}. Введите /myforms чтобы просмотреть взятые вами заявки в работу".format(
                             int(form_id), vacancy_name, active_forms_len))

    elif call.data.split()[0] == 'candidate':
        form_id = call.data.split()[1]
        session.add(candidates(id_form=form_id, worker_id=call.from_user.id, name='wait'))
        session.commit()
        session.close()
        bot.send_message(call.from_user.id, 'Заполните форму кандидата')
        bot.send_message(call.from_user.id, 'Введите имя кандидата')

    elif call.data.split('+')[0] == 'category':
        bot.send_message(call.from_user.id, 'В выбранной категории вам доступны следующие заявки:')
        chosen_category = call.data.split('+')[1]
        worker = session.query(workers).filter_by(user_id=call.from_user.id).first()
        worker_level = worker.level
        for s_form in session.query(form).filter_by(pay_level=worker_level, category=chosen_category).all():
            form_buttons = telebot.types.InlineKeyboardMarkup()
            form_buttons.add(
                telebot.types.InlineKeyboardButton(text='ВЗЯТЬ В РАБОТУ', callback_data='work' + ' ' + str(s_form.id)),
                telebot.types.InlineKeyboardButton(text='ПРЕДЛОЖИТЬ КАНДИДАТА',
                                                   callback_data='candidate' + ' ' + str(s_form.id)))
            bot.send_message(call.from_user.id, '''Заявка:
                    Номер заявки: {0},
                    Работодатель:{7},
                    Наименование вакансии: {1},
                    Категория: {11},
                    Обязанности: {2},
                    Требования: {3},
                    Условия работы: {4},
                    Сумма вознаграждения: {6},
                    Взято в работу рекрутерами: {8}.
                    Ваш уровень: закрытых заявок {9} ({10} заявки до перехода на уровень MEDIUM)
                            '''.format(
                str(s_form.id),
                s_form.vacancy,
                s_form.duties,
                s_form.requirements,
                s_form.conditions,
                s_form.pay_level,
                str(s_form.salary),
                s_form.nickname,
                s_form.recruiter_count,
                worker.closed_tasks,
                str(3 - worker.closed_tasks),
                s_form.category,
            ), reply_markup=form_buttons)


    elif call.data.startswith('answ'):
        button_data = call.data[4:]
        button_full_text = all_answers_dict[button_data]
        bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text=button_full_text)
    elif call.data == 'Accept' and session.query(workers).filter_by(user_id=call.from_user.id).first().test_stage == 1:
        worker = session.query(workers).filter_by(user_id=call.from_user.id).first()
        worker.test_stage = 2
        session.commit()
        session.close()
        bot.send_message(call.from_user.id, "Ответы учтены")
        bot.send_message(call.from_user.id, '''Вопрос 2. Чтобы отметить вариант ответа как правильный нажмите на крестик и ждите когда он изменится на галочку. Для подтверждение вариантов ответа нажмите кнопку "Далее" 
Прежде, чем отправить кандидата на рассмотрение работодателю, я:''', reply_markup=get_quiz_table(2, call.from_user.id))
    elif call.data == 'Accept' and session.query(workers).filter_by(user_id=call.from_user.id).first().test_stage == 2:
        worker = session.query(workers).filter_by(user_id=call.from_user.id).first()
        worker.test_stage = 3
        session.commit()
        session.close()
        bot.send_message(call.from_user.id, "Ответы учтены")
        bot.send_message(call.from_user.id,
                         '''Вопрос 3. Для того, чтобы начать зарабатывать на закрытии заявок мне нужно:''',
                         reply_markup=get_quiz_table(3, call.from_user.id))

    elif call.data == 'Accept' and session.query(workers).filter_by(user_id=call.from_user.id).first().test_stage == 3:
        worker = session.query(workers).filter_by(user_id=call.from_user.id).first()
        worker.test_stage = 4
        result = 0
        result1 = 0
        result2 = 0
        result3 = 0
        ans_list1 = [
            worker.first_test_1,
            worker.first_test_2,
            worker.first_test_3,
            worker.first_test_4,
            worker.first_test_5,
            worker.first_test_6]
        ans_list2 = [
            worker.second_test_1,
            worker.second_test_2,
            worker.second_test_3,
            worker.second_test_4]
        ans_list3 = [
            worker.third_test_1,
            worker.third_test_2,
            worker.third_test_3,
            worker.third_test_4,
        ]
        point_list1 = [1, 1, -1, 1, 1, 1]
        point_list2 = [1, 1, 1, -1]
        point_list3 = [1, 1, 1, -3]

        ans_point_list1 = [[ans_list1[i], point_list1[i]] for i in range(6)]
        ans_point_list2 = [[ans_list2[i], point_list2[i]] for i in range(4)]
        ans_point_list3 = [[ans_list3[i], point_list3[i]] for i in range(4)]
        for lst1 in ans_point_list1:
            if lst1[0]:
                result1 += lst1[1]
        for lst2 in ans_point_list2:
            if lst2[0]:
                result2 += lst2[1]
        for lst3 in ans_point_list3:
            if lst3[0]:
                result3 += lst3[1]
        if result1 == 5:
            result += 5
        if result2 == 3:
            result += 3
        if result3 >= 1:
            result += 1
        bot.send_message(call.from_user.id, "Ответы учтены")
        if result == 9:
            worker.done = True
            bot.send_message(call.from_user.id, "Поздравляем, вы в команде!", reply_markup=keyboard10)
        else:
            session.delete(worker)
            session.commit()
            session.close()
            bot.send_message(call.from_user.id, "Вы что-то упустили!", reply_markup=keyboard11)


bot.polling(none_stop=True, interval=0)

# telebot.types.InlineKeyboardButton("Название"), telebot.types.InlineKeyboardButton("Обязанности"), telebot.types.InlineKeyboardButton("Требования"), telebot.types.InlineKeyboardButton("Условия"),telebot.types.InlineKeyboardButton("Уровень оплаты"),telebot.types.InlineKeyboardButton("Сумма"), telebot.types.InlineKeyboardButton("Контакты")
# bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
#                          text="You Clicked " + valueFromCallBack + " and key is " + keyFromCallBack)