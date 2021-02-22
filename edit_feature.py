'''elif message.text == 'Исправить':
form_request = session.query(form).filter_by(user_id=message.from_user.id, active=False).first()
form_request.editing = True
session.commit()
session.close()
bot.send_message(message.from_user.id, 'Выберите параметр для исправления', reply_markup=keyboard5)
elif (message.text == 'Название' or message.text == 'Обязанности' or message.text == 'Требования' or message.text == 'Условия' or message.text == 'Уровень оплаты' or message.text == 'Сумма' or message.text == 'Контакты') and len(
    session.query(form).filter_by(user_id=message.from_user.id, active=False).all()) > 0:
if message.text == 'Название':
    current_form = session.query(form).filter_by(user_id=message.from_user.id, editing=True).first()
    current_form.vacancy = 'wait'
    session.commit()
    session.close()
    bot.send_message(message.from_user.id, 'Введите название вакансии')
elif message.text == 'Обязанности':
    current_form = session.query(form).filter_by(user_id=message.from_user.id, editing=True).first()
    current_form.duties = 'wait'
    session.commit()
    session.close()
    bot.send_message(message.from_user.id, 'Введите обязанности работающего')
elif message.text == 'Требования':
    current_form = session.query(form).filter_by(user_id=message.from_user.id, editing=True).first()
    current_form.requirements = 'wait'
    session.commit()
    session.close()
    bot.send_message(message.from_user.id, 'Введите требования для работающего')
elif message.text == 'Условия':
    current_form = session.query(form).filter_by(user_id=message.from_user.id, editing=True).first()
    current_form.conditions = 'wait'
    session.commit()
    session.close()
    bot.send_message(message.from_user.id, 'Введите условия работы')
elif message.text == 'Уровень оплаты':
    current_form = session.query(form).filter_by(user_id=message.from_user.id, editing=True).first()
    current_form.pay_level = 'wait'
    session.commit()
    session.close()
    bot.send_message(message.from_user.id,""" Выберите уровень оплаты.
    LIGHT (бесплатно),
    MEDIUM (до 5000 руб.),
    HARD (от 5000 до 10000 руб.),
    PRO (выше 10000 руб.)
    """, reply_markup=keyboard3)'''

