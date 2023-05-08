import Bot.buttons as buttons
import database.db_functions as db
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_handler_backends import State, StatesGroup
import asyncio

#bot
bot = AsyncTeleBot('5840015646:AAGPGwTBXSZbF_tA5ILcxGbITWjaay0-5Mo')

#states
class WorkStates(StatesGroup):
    play = State()
    waiting = State()


@bot.message_handler(commands='start')
async def ret(msg):
    await bot.send_message(msg.chat.id, 'Добро пожаловать в waifu!', reply_markup=buttons.markup)

@bot.message_handler(content_types=['text'])
async def set_states(msg):
    if msg.text == 'Играть':
        await bot.set_state(msg.from_user.id, WorkStates.play, msg.chat.id)
        await play(msg)
    if msg.text == 'Да':
        await bot.set_state(msg.from_user.id, WorkStates.waiting,msg.chat.id)
        await queue(msg)



@bot.message_handler(state=WorkStates.play)
async def play(msg):
    await bot.send_message(msg.chat.id, 'выберите карту')
    await bot.send_message(msg.chat.id, 'все доступные карточки', reply_markup=buttons.markup_inline)


card_lvl = None
@bot.callback_query_handler(func=lambda call: True)
async def process_callback_button1(call):
    global card_lvl
    card_lvl = call.data
    await bot.answer_callback_query(call.id)
    await bot.send_message(call.from_user.id, f'Вы выбрали {call.data} персонажа, начать игру?', reply_markup=buttons.markup_yes_no)

@bot.message_handler(state=WorkStates.waiting)
async def queue(msg):
    print('asdsdvjn')
    db.add_to_queue(msg.chat.id,card_lvl)
    await bot.send_message(msg.chat.id,'Вы добавлены в очередь!')
    my_id = msg.chat.id
    opponent_id = -1
    opponent_id = await db.find_opponent(my_id)
    while True:
        if opponent_id != -1:
            await start_session(msg,opponent_id[0])
            break
        await asyncio.sleep(1)
async def start_session(msg,opponent_id):
    await bot.send_message(msg.chat.id,f'Оппонент найден! {opponent_id}\n'
                                       f'Его номер карты - {db.get_opponent_clvl(opponent_id)}')
    db.delete_from_queue(msg.chat.id)
    db.create_session(msg.chat.id,opponent_id)


def main():
    asyncio.run(bot.infinity_polling())