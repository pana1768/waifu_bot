from telebot import types
from database.db_functions import Database
#menu
markup = types.ReplyKeyboardMarkup()
markup.add(types.KeyboardButton('Играть'))


#play->choose card(inline)
def get_inline_card_buttons(user_id):
    markup_inline = types.InlineKeyboardMarkup(row_width=3)
    cards = Database.get_user_cards(user_id)
    tmp = []
    print(len(cards))
    for i in range(len(cards)):
        button = types.InlineKeyboardButton(f'{i+1}',callback_data=i+1)
        tmp.append(button)
    markup_inline.add(*tmp)
    return markup_inline

#начать игру
markup_yes_no = types.ReplyKeyboardMarkup()
yes = types.KeyboardButton('Да')
no = types.KeyboardButton('Нет')
markup_yes_no.add(yes,no)