import time
import telebot
from telebot import types
import sorts
import hard

bot = telebot.TeleBot('8324658293:AAG1J8_Q_uI7JBMG4T5Zs3YfNtBTNmgGqdI')


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(msg: types.Message):
    bot.send_message(msg.chat.id, "Привет! Я бот, который расскажет вам о сортировках.")
    menu(msg)

def menu(msg: types.Message):
    keyboard = types.ReplyKeyboardMarkup(True, True)
    keyboard.row("Справка популярных сортировок")
    keyboard.row("Анализ сложности алгоритма")
    bot.send_message(msg.chat.id, "Выбери действие:", reply_markup=keyboard)
    bot.register_next_step_handler(msg, menu_handler)

def menu_handler(msg: types.Message):
    if msg.text.endswith("сортировок"):
        local_sorts(msg)
    elif msg.text.endswith("алгоритма"):
        bot.send_message(msg.chat.id, "Отправь мне свой алгоритм, "
                                      "а я постараюсь посчитать его сложность по О-нотации.\n"
                                      "Внимание: анализ кода на сложность это сложный аналитический процесс. Результат "
                                      "может быть неверным!")
        bot.register_next_step_handler(msg, analyze_custom_algorithm)


def local_sorts(msg: types.Message):
    keyboard = types.ReplyKeyboardMarkup(True, True)
    for sort in sorts.sort_dict:
        keyboard.row(sort)
    bot.send_message(msg.chat.id, "Выберите вид сортировки из меню ниже:", reply_markup=keyboard)
    bot.register_next_step_handler(msg, handle_sort_choice)


# Обработчик кнопок
def handle_sort_choice(msg: types.Message):
    sort_type = msg.text
    # В зависимости от выбора пользователя, отправьте информацию о соответствующей сортировке
    sort_info = sorts.sort(sort_type)
    bot.send_message(msg.chat.id, sort_info, parse_mode='HTML')
    time.sleep(2)
    menu(msg)

def analyze_custom_algorithm(msg: types.Message):
    a = hard.Analyze(msg.text)
    result = a.start()
    bot.send_message(msg.chat.id, result)
    time.sleep(2)
    menu(msg)


# Запуск бота
bot.infinity_polling()

