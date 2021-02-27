import telebot
from models import form, Base, workers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from time import sleep
engine = create_engine('sqlite:///forms.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
DBSession.bind = engine
session = DBSession()
#('LIGHT (бесплатно)', 'MEDIUM (до 5000 руб.)', 'HARD (от 5000 до 10000 руб.)', 'PRO (выше 10000 руб.)')
reading, writing = False, False
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
keyboard11 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard11.row('ПРОЙТИ ОБУЧЕНИЕ', 'УЗНАТЬ ОБ ОСТАЛЬНЫХ УРОВНЯХ')
keyboard8 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard8.row('ДАЛЕЕ')
keyboard9 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard9.row('ПРОЙТИ ТЕСТ')
keyboard10 = telebot.types.InlineKeyboardMarkup()

all_answers_dict = {'Telegram':'Telegram' , 'Соцсети, работные сайты':'Соцсети, работные сайты', 'На рынке':'На рынке',
                    'Сайты знакомств':'Сайты знакомств', 'Дам объявление':'Дам объявление', 'Переманю':'Переманю',
'Проведу телефонное интер':'Проведу телефонное интервью',
'Созвонюсь по видео связи':'Созвонюсь по видео связи',
'Встречусь вживую при нео':'Встречусь вживую при необходимости',
'Только пообщаюсь по пере':'Только пообщаюсь по переписке'
                    }

question_list1 = ['Telegram', 'Соцсети, работные сайты', 'На рынке', 'Сайты знакомств', 'Дам объявление', 'Переманю',]
question_list2 = ['Проведу телефонное интер',
'Созвонюсь по видео связи',
'Встречусь вживую при нео',
'Только пообщаюсь по пере']
def get_quiz_table(ques_numb, workernumb):
    global reading
    reading = True
    if not writing:
        worker = session.query(workers).filter_by(user_id= workernumb).first()
        session.close()
        reading = False
        quiz_table = telebot.types.InlineKeyboardMarkup()
        quiz_answer_dict = {}
        if type(worker) != 'NoneType' :
            if ques_numb ==1:
                TrueFalseList = [worker.first_test_1, worker.first_test_2, worker.first_test_3, worker.first_test_4, worker.first_test_5, worker.first_test_6]
                quiz_answer_dict = dict(zip(question_list1, TrueFalseList))
            elif ques_numb == 2:
                TrueFalseList = [worker.second_test_1, worker.second_test_2, worker.second_test_3, worker.second_test_4]
                quiz_answer_dict = dict(zip(question_list2, TrueFalseList))
            for ques, answ in quiz_answer_dict.items():
                if quiz_answer_dict[ques]:
                    quiz_table.add(telebot.types.InlineKeyboardButton(text= ques, callback_data= "answ" + ques), telebot.types.InlineKeyboardButton(text= '✅', callback_data=ques))
                else:
                    quiz_table.add(telebot.types.InlineKeyboardButton(text=ques, callback_data="answ" + ques),
                                   telebot.types.InlineKeyboardButton(text='❌', callback_data=ques))
            quiz_table.add(telebot.types.InlineKeyboardButton(text= 'Далее', callback_data="Accept"))
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
            if ques_numb ==1:
                TrueFalseList = [worker.first_test_1, worker.first_test_2, worker.first_test_3, worker.first_test_4,
                                 worker.first_test_5, worker.first_test_6]
                quiz_answer_dict = dict(zip(question_list1, TrueFalseList))
            elif ques_numb ==2:
                TrueFalseList = [worker.second_test_1, worker.second_test_2, worker.second_test_3, worker.second_test_4]
                quiz_answer_dict = dict(zip(question_list2, TrueFalseList))
        reading = False
        return  quiz_answer_dict
    else:
        return "processing"

def change_true_false(question, workernumb):
    if not reading:
        global writing
        writing = True
        worker = session.query(workers).filter_by(user_id=workernumb).first()
        #sleep(0.5)
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
        writing = False



@bot.message_handler(commands=['start'])
def get_start_message(message):
    worker = session.query(workers).filter_by(user_id = message.from_user.id).first()
    if worker:
        session.delete(worker)
        session.commit()
        session.close()
    form_request = session.query(form).filter_by(user_id=message.from_user.id).first()
    if form_request:
        session.delete(form_request)
        session.commit()
        session.close()

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
        try:
            salary = int(message.text)
            salaryflag = True
        except ValueError:
            salaryflag = False
            bot.send_message(message.from_user.id, 'Введите вознаграждение одним числом без букв')
        if salaryflag:
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

    elif message.text == 'ПРОЙТИ РЕГИСТРАЦИЮ':

        bot.send_message(message.from_user.id,
                         '''Твой уровень LIGHT
Закрой 3 позиции от разных работодателей по заявке уровня LIGHT (без оплаты) и переходи на следующий уровень. 
''',
                         reply_markup=keyboard11)
    elif message.text == 'ПРОЙТИ ОБУЧЕНИЕ':
        session.add(workers(user_id=message.from_user.id))
        worker = session.query(workers).filter_by(user_id = message.from_user.id).first()
        worker.educ_lvl = 1
        session.commit()
        session.close()
        bot.send_message(message.from_user.id,
                         '''Мир поделен на две части: тот, кто предлагает работу, и тот, кто эту работу выполняет. Рекрутер относится ко второй категории. Мы с вами выполняем работу по поиску людей, которые согласны выполнять работу тех, кто ее предоставляет.
Требуется понимать - насколько качественно мы выполним нашу с вами работу и как быстро предоставим нужного человека – от этого зависит наше будущее, как профессионала.
''',
                         reply_markup=keyboard8)
    elif message.text == 'ДАЛЕЕ':
        worker = session.query(workers).filter_by(user_id = message.from_user.id).first()
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
        elif worker.educ_lvl ==2:
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
    #рекрутер
    elif message.text == 'ПРОЙТИ ТЕСТ' and session.query(workers).filter_by(user_id=message.from_user.id).first().educ_lvl == 5:
        worker = session.query(workers).filter_by(user_id=message.from_user.id).first()
        worker.educ_lvl = 6
        worker.test_stage = 1
        worker.first_test_1 = False
        worker.first_test_2 = False
        worker.first_test_3 = False
        worker.first_test_4 = False
        worker.first_test_5 = False
        worker.first_test_6 = False
        session.commit()
        session.close()
        bot.send_message(message.from_user.id, '''Вопрос 1. Чтобы отметить вариант ответа как правильный нажмите на крестик и ждите когда он изменится на галочку. Для подтверждение вариантов ответа нажмите кнопку "Далее" 
        
        
        Я буду искать кандидатов:''',
                             reply_markup=get_quiz_table(1, message.from_user.id))

@bot.callback_query_handler(func=lambda call: True)
def get_callback(call):
    if call.data in question_list1:
        test_dict = get_test_dict(1, call.from_user.id)
        if test_dict !=  "processing":
            for key in test_dict:
                if call.data == key:
                    change_true_false(key, call.from_user.id)
                    bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.message_id,
                                                  reply_markup=get_quiz_table(1, call.from_user.id))
                    break
    elif call.data in question_list2:
        test_dict = get_test_dict(2, call.from_user.id)
        if test_dict != "processing":
            for key in test_dict:
                if call.data == key:
                    change_true_false(key, call.from_user.id)
                    bot.edit_message_reply_markup(call.message.chat.id, message_id=call.message.message_id,
                                                  reply_markup=get_quiz_table(2, call.from_user.id))
                    break

    elif call.data.startswith('answ'):
        button_data = call.data[4:]
        button_full_text = all_answers_dict[button_data]
        bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text=button_full_text)
    elif call.data == 'Accept' and session.query(workers).filter_by(user_id=call.from_user.id).first().test_stage == 1:
        worker = session.query(workers).filter_by(user_id=call.from_user.id).first()
        worker.test_stage = 2
        worker.second_test_1 = False
        worker.second_test_2 = False
        worker.second_test_3 = False
        worker.second_test_4 = False
        session.commit()
        session.close()
        bot.send_message(call.from_user.id, "Ответы учтены")
        bot.send_message(call.from_user.id, '''Вопрос 1. Чтобы отметить вариант ответа как правильный нажмите на крестик и ждите когда он изменится на галочку. Для подтверждение вариантов ответа нажмите кнопку "Далее" 
        
        
        Прежде, чем отправить кандидата на рассмотрение работодателю, я:''', reply_markup=get_quiz_table(2, call.from_user.id))







bot.polling(none_stop=True, interval=0)

#telebot.types.InlineKeyboardButton("Название"), telebot.types.InlineKeyboardButton("Обязанности"), telebot.types.InlineKeyboardButton("Требования"), telebot.types.InlineKeyboardButton("Условия"),telebot.types.InlineKeyboardButton("Уровень оплаты"),telebot.types.InlineKeyboardButton("Сумма"), telebot.types.InlineKeyboardButton("Контакты")
#bot.answer_callback_query(callback_query_id=call.id, show_alert=True,
    #                          text="You Clicked " + valueFromCallBack + " and key is " + keyFromCallBack)