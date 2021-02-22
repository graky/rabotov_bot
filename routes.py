import telebot
from models import form, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///forms.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
DBSession.bind = engine
session = DBSession()
#('LIGHT (бесплатно)', 'MEDIUM (до 5000 руб.)', 'HARD (от 5000 до 10000 руб.)', 'PRO (выше 10000 руб.)')

token = '1697476492:AAE6Qt9iQlA_K1H6qk_aG6UHSoz8hM7ve-U'
bot = telebot.TeleBot(token)
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('РАБОТАДАТЕЛЬ', 'РЕКРУТЕР')
keyboard2 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard2.row('ЗАПОЛНИТЬ ЗАЯВКУ')
keyboard3 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard3.row('LIGHT', 'MEDIUM', 'HARD', 'PRO')
keyboard4 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard4.row('Запустить подбор',) #Исправить
#keyboard5 = telebot.types.InlineKeyboardMarkup()
#butn1, butn2, butn3, butn4, bunt5, bunt6, butn7 = telebot.types.InlineKeyboardButton("Название"), telebot.types.InlineKeyboardButton("Обязанности"), telebot.types.InlineKeyboardButton("Требования"), telebot.types.InlineKeyboardButton("Условия"),telebot.types.InlineKeyboardButton("Уровень оплаты"),telebot.types.InlineKeyboardButton("Сумма"), telebot.types.InlineKeyboardButton("Контакты")
#keyboard5.row = (butn1, butn2, butn3, butn4, bunt5, bunt6, butn7)
keyboard6 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard6.row('ЗАКРЫТЬ ЗАЯВКУ',)
keyboard7 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard7.row('ПРОЙТИ РЕГИСТРАЦИЮ',)
@bot.message_handler(commands=['start'])
def get_start_message(message):
    bot.send_message(message.from_user.id, 'Выберите категорию:', reply_markup=keyboard1)

@bot.message_handler(content_types= ['text'])
def application_form(message):
    if message.text == 'РАБОТАДАТЕЛЬ':
        bot.send_message(message.from_user.id, 'Не тратьте время на поиск сотрудников. Делегируйте. Рекрутеры займутся этим вопросом за вас.',
                         reply_markup=keyboard2)
    if message.text == 'ЗАПОЛНИТЬ ЗАЯВКУ':
        session.add(form(user_id=message.from_user.id, vacancy= 'wait'))
        session.commit()
        session.close()
        bot.send_message(message.from_user.id, 'Введите название вакансии')
    
    elif len(session.query(form).filter_by(user_id = message.from_user.id, vacancy = 'wait').all()) > 0:  #done
        session.close()
        current_form = session.query(form).filter_by(user_id = message.from_user.id, vacancy = 'wait').first()
        current_form.vacancy = message.text
        current_form.duties = 'wait'
        session.commit()
        session.close()
        bot.send_message(message.from_user.id, 'Введите обязанности работающего')

    elif len(session.query(form).filter_by(user_id = message.from_user.id, duties = 'wait').all()) >0: #done
        session.close()
        current_form = session.query(form).filter_by(user_id = message.from_user.id, duties = 'wait').first()
        current_form.duties = message.text
        current_form.requirements = 'wait'
        session.commit()
        session.close()
        bot.send_message(message.from_user.id, 'Введите требования для работающего')

    elif len(session.query(form).filter_by(user_id = message.from_user.id, requirements = 'wait').all()) > 0: #done
        session.close()
        current_form = session.query(form).filter_by(user_id = message.from_user.id, requirements = 'wait').first()
        current_form.requirements = message.text
        current_form.conditions = 'wait'
        session.commit()
        session.close()
        bot.send_message(message.from_user.id, 'Введите условия работы')
    elif len(session.query(form).filter_by(user_id = message.from_user.id, conditions = 'wait').all()) > 0: #done
        session.close()
        current_form = session.query(form).filter_by(user_id = message.from_user.id, conditions = 'wait').first()
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

    elif len(session.query(form).filter_by(user_id = message.from_user.id, pay_level = 'wait').all()) > 0: #done
        session.close()
        current_form = session.query(form).filter_by(user_id = message.from_user.id, pay_level = 'wait').first()
        if message.text == 'LIGHT':
            current_form.pay_level = message.text
            current_form.salary = 0
            current_form.nickname = 'wait'
            session.commit()
            session.close()
            bot.send_message(message.from_user.id, 'В соотвествии с выбранным уровнем оплаты, вознаграждения работающему не предусмотрено. Введите ваш никнейм или номер телефон для контакта с работающим')
        else:
            current_form.pay_level = message.text
            current_form.salary = 'wait'
            session.commit()
            session.close()
            bot.send_message(message.from_user.id, 'Введите сумму вознаграждения')
    elif len(session.query(form).filter_by(user_id = message.from_user.id, salary = 'wait').all()) > 0: #done
        session.close()
        current_form = session.query(form).filter_by(user_id = message.from_user.id, salary = 'wait').first()
        salary = int(message.text)
        if current_form.pay_level == 'MEDIUM':
            if salary > 5000:
                bot.send_message(message.from_user.id, 'вознаграждение рукретеру уровня MEDIUM от 1 до 5000 руб. Проверьте сумму и повторите отправку.')
            else:
                current_form.salary = salary
                current_form.nickname = 'wait'
                session.commit()
                session.close()
                bot.send_message(message.from_user.id, 'Введите ваш никнейм или номер телефон для контакта с работающим')
        elif current_form.pay_level == 'HARD':
            if salary < 5000 or salary >10000:
                bot.send_message(message.from_user.id, 'вознаграждение рукретеру уровня HARD от 5000 до 10000 руб. Проверьте сумму и повторите отправку.')
            else:
                current_form.salary = salary
                current_form.nickname = 'wait'
                session.commit()
                session.close()
                bot.send_message(message.from_user.id, 'Введите ваш никнейм или номер телефон для контакта с работающим')
        elif current_form.pay_level == 'PRO':
            if salary <10000:
                bot.send_message(message.from_user.id, 'вознаграждение рукретеру уровня PRO от 10000 руб. Проверьте сумму и повторите отправку.')
            else:
                current_form.salary = salary
                current_form.nickname = 'wait'
                session.commit()
                session.close()
                bot.send_message(message.from_user.id, 'Введите ваш никнейм или номер телефон для контакта с работающим')
    elif len(session.query(form).filter_by(user_id = message.from_user.id, nickname = 'wait').all()) > 0:
        session.close()
        current_form = session.query(form).filter_by(user_id = message.from_user.id, nickname = 'wait').first()
        current_form.nickname = message.text
        current_form.just_finished = True
        session.commit()
        session.close()
        form_request = session.query(form).filter_by(user_id = message.from_user.id, just_finished = True).first()
        form_request.just_finished = False
        bot.send_message(message.from_user.id, '''Ваша форма:
Номер вакансии: {0},
Название вакансии: {1},
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
        ), reply_markup=keyboard4)
        form_request.active = False
        session.commit()
        session.close()

    elif message.text == 'Запустить подбор':
        form_request = session.query(form).filter_by(user_id=message.from_user.id, active=False).first()
        form_request.active = True
        bot.send_message(message.from_user.id, 'заявка №{0} {1} добавлена в выдачу. Чтобы удалить заявку введите ЗАКРЫТЬ ЗАЯВКУ'.format(str(form_request.id),form_request.vacancy, ), reply_markup= keyboard6)
        session.commit()
        session.close()
    elif message.text == 'ЗАКРЫТЬ ЗАЯВКУ':
        form_request = session.query(form).filter_by(user_id=message.from_user.id).first()
        session.delete(form_request)
        bot.send_message(message.from_user.id, 'заявка №{0} {1} закрыта. Чтобы добавить новую заявку введите /start'.format(str(form_request.id),form_request.vacancy, ), reply_markup= keyboard6)
        session.commit()
        session.close()
    elif message.text == 'РЕКРУТЕР':
        bot.send_message(message.from_user.id,
                         'Заработай больше на поиске персонала. Закрывай заявки в любое время. Делай то, что тебе нравится.',
                         reply_markup=keyboard7)


    #рекрутер


bot.polling(none_stop=True, interval=0)

#telebot.types.InlineKeyboardButton("Название"), telebot.types.InlineKeyboardButton("Обязанности"), telebot.types.InlineKeyboardButton("Требования"), telebot.types.InlineKeyboardButton("Условия"),telebot.types.InlineKeyboardButton("Уровень оплаты"),telebot.types.InlineKeyboardButton("Сумма"), telebot.types.InlineKeyboardButton("Контакты")