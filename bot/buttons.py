from telebot import types

#menu
markup = types.ReplyKeyboardMarkup()
markup.add(types.KeyboardButton('Играть'))


#play->choose card(inline)
markup_inline = types.InlineKeyboardMarkup(row_width=3)
tmp = []
for i in range(15):
    button = types.InlineKeyboardButton(f'{i+1}',callback_data=i+1)
    tmp.append(button)
markup_inline.add(*tmp)

#начать игру
markup_yes_no = types.ReplyKeyboardMarkup()
yes = types.KeyboardButton('Да')
no = types.KeyboardButton('Нет')
markup_yes_no.add(yes,no)