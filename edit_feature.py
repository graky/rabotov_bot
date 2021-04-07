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
    """, reply_markup=keyboard3)

pay_level_list = {'LIGHT':[0, 0], 'MEDIUM':[1, 5000], 'HARD':[5000,10000], 'PRO':[10000, 100000]}

for i in range(100):
    key = random.choice(list(pay_level_list.keys()))
    value = random.randint(pay_level_list[key][0], pay_level_list[key][1])
    session.add(form(user_id =i, vacancy = 'говночист {0}'.format(str(i)), duties ='чистить говно {0}'.format(str(i)), requirements ='умелые руки {0}'.format(str(i)), conditions = 'барак {0}'.format(str(i)),  pay_level =key, salary = value, nickname = str(228*i), active = True))
print('done')'''
#1697476492:AAFqdRTjz-LOKIIKjKQqjT4BOS3PpBUS3G0 tok1
#1570308085:AAFC4rvv6aQGb8SZt_sc4mWtmn-l27c6D8k tok2
#employee_buttons = telebot.types.InlineKeyboardMarkup()
           # employee_buttons.add(telebot.types.InlineKeyboardButton(text='СОБЕСЕДОВАТЬ', callback_data=''),
            #                     telebot.types.InlineKeyboardButton(text='СОБЕСЕДОВАТЬ', callback_data=''),

             #                    )