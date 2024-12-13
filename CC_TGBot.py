"""Телеграм-бот технической поддержки контакт-центра"""

import telebot
from telebot import types
from config import *

bot = telebot.TeleBot(token())
chat = chat_id()


@bot.message_handler(commands=['start'])
def welcome(message):
    """Приветствие. Кнопочное меню."""
    global chat
    member = bot.get_chat_member(chat_id=chat, user_id=message.from_user.id)
    statuses = ('creator', 'administrator', 'member')
    if message.chat.type == 'private':
        if member.status in statuses:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton('ПК 🖥️')
            button2 = types.KeyboardButton('Citrix 🌀')
            button3 = types.KeyboardButton('Связь 🎧')
            button4 = types.KeyboardButton('Почта 📧')
            button5 = types.KeyboardButton('Браузер 🌐')
            button6 = types.KeyboardButton('Пароли 🔓')
            button7 = types.KeyboardButton('Доступы 📄')
            button8 = types.KeyboardButton('Принтер 🖨️')
            markup.add(button1, button2, button3, button4, button5, button6,
                       button7, button8)
            bot.send_message(message.chat.id, 'Привет, {0.first_name}! Я бот для сотрудников нашего КЦ, '
                                              'который постарается тебе помочь! Воспользуйся кнопками меню.'
                             .format(message.from_user, bot.get_me()), parse_mode='html',
                             reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Ты не в списке избранных 😎 \nПо крайней мере пока')


@bot.message_handler(commands=['info'])
def info(message):
    """Обратная связь"""
    global chat
    member = bot.get_chat_member(chat_id=chat, user_id=message.from_user.id)
    statuses = ('creator', 'administrator', 'member')
    if message.chat.type == 'private':
        if member.status in statuses:
            contacts = open('contacts.txt', encoding='UTF-8').read()
            bot.send_message(message.chat.id, f'Чтобы помочь нам улучшить бота, пишите письма/сообщения с '
                                              f'предложениями и замечаниями: {contacts}', parse_mode='html')
        else:
            bot.send_message(message.chat.id, 'Ты не в списке избранных 😎 \nПо крайней мере пока')


@bot.message_handler(content_types=['text'])
def dialog(message):
    """Работа с текстовыми сообщениями"""
    global chat
    member = bot.get_chat_member(chat_id=chat, user_id=message.from_user.id)
    statuses = ('creator', 'administrator', 'member')
    if message.chat.type == 'private':
        if member.status in statuses:
            if message.text == 'Citrix 🌀':
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton('Установка Цитрикс на личный ПК', callback_data='citrix_setup'))
                markup.add(types.InlineKeyboardButton('Цитрикс просит адрес сервера', callback_data='citrix_address'))
                markup.add(types.InlineKeyboardButton('Зависает Цитрикс, лагает связь', callback_data='citrix_lags'))
                markup.add(types.InlineKeyboardButton('Обновление Цитрикса', callback_data='citrix_update'))
                bot.send_message(message.chat.id, 'Выбери из списка:', reply_markup=markup)
            if message.text == 'Связь 🎧':
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton('Пропал звук', callback_data='lose_sound'))
                markup.add(types.InlineKeyboardButton('Не меняется статус', callback_data='softphone_statuses'))
                bot.send_message(message.chat.id, 'Выбери из списка:', reply_markup=markup)
            if message.text == 'Outlook 📧':
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton('Переполнена почта, архив', callback_data='full_mail'))
                bot.send_message(message.chat.id, 'Выбери из списка:', reply_markup=markup)
            if message.text == 'ПК 🖥️':
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton('Ошибка при входе в ПК', callback_data='pc_not_in_domain'))
                markup.add(types.InlineKeyboardButton('Изображение на 2 монитора', callback_data='two_monitors'))
                bot.send_message(message.chat.id, 'Выбери из списка:', reply_markup=markup)
            if message.text == 'Пароль 🔓':
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton('Как сменить пароль от системы',
                                                      callback_data='domain_pass_change'))
                markup.add(types.InlineKeyboardButton('Пароль от второй УЗ',
                                                      callback_data='another_password'))
                bot.send_message(message.chat.id, 'Выбери из списка:', reply_markup=markup)
            if message.text == 'Браузер 🌐':
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton('Браузер по умолчанию', callback_data='default_browser'))
                markup.add(types.InlineKeyboardButton('Как сохранить закладки', callback_data='bookmarks'))
                markup.add(types.InlineKeyboardButton('Очистка кэша', callback_data='clean_cache'))
                bot.send_message(message.chat.id, 'Выбери из списка:', reply_markup=markup)
            if message.text == 'Принтер 🖨️':
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton('Печать на принтере', callback_data='print_on_printer'))
                bot.send_message(message.chat.id, 'Выбери из списка:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_instructions(call):
    """Обработка диалога через инлайновые кнопки"""
    global chat
    member = bot.get_chat_member(chat_id=chat, user_id=call.from_user.id)
    statuses = ('creator', 'administrator', 'member')
    if member.status in statuses:
        if call.message:
            if call.data == 'citrix_setup':
                ctx_home_part_1 = open('ctx_home_part_1.txt', encoding='UTF-8').read()
                ctx_home_1 = open('ctx_home_1.png', 'rb')
                ctx_home_2 = open('ctx_home_2.png', 'rb')
                bot.send_message(call.message.chat.id, text=ctx_home_part_1)
                bot.send_photo(call.message.chat.id, ctx_home_1)
                bot.send_photo(call.message.chat.id, ctx_home_2)
                ctx_home_part_2 = open('ctx_home_part_2.txt', encoding='UTF-8').read()
                ctx_home_3 = open('ctx_home_3.png', 'rb')
                bot.send_message(call.message.chat.id, text=ctx_home_part_2)
                bot.send_photo(call.message.chat.id, ctx_home_3)
                ctx_home_part_3_1 = open('ctx_home_part_3_1.txt', encoding='UTF-8').read()
                ctx_home_4 = open('ctx_home_4.png', 'rb')
                bot.send_message(call.message.chat.id, text=ctx_home_part_3_1)
                bot.send_photo(call.message.chat.id, ctx_home_4)
                ctx_home_part_3_2 = open('ctx_home_part_3_2.txt', encoding='UTF-8').read()
                ctx_home_5 = open('ctx_home_5.png', 'rb')
                bot.send_message(call.message.chat.id, text=ctx_home_part_3_2)
                bot.send_photo(call.message.chat.id, ctx_home_5)
                ctx_home_part_4 = open('ctx_home_part_4.txt', encoding='UTF-8').read()
                ctx_home_6 = open('ctx_home_6.png', 'rb')
                bot.send_message(call.message.chat.id, text=ctx_home_part_4)
                bot.send_photo(call.message.chat.id, ctx_home_6)
                ctx_home_part_5 = open('ctx_home_part_5.txt', encoding='UTF-8').read()
                ctx_home_7 = open('ctx_home_7.png', 'rb')
                bot.send_message(call.message.chat.id, text=ctx_home_part_5)
                bot.send_photo(call.message.chat.id, ctx_home_7)
                ctx_home_part_6 = open('ctx_home_part_6.txt', encoding='UTF-8').read()
                bot.send_message(call.message.chat.id, text=ctx_home_part_6)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Установка Цитрикс на личный ПК:', reply_markup=None)
            if call.data == 'citrix_address':
                ctx_server = open('ctx_server.txt', encoding='UTF-8').read()
                ctx_server_pic = open('ctx_server_pic.png', 'rb')
                bot.send_message(call.message.chat.id, text=ctx_server)
                bot.send_photo(call.message.chat.id, ctx_server_pic)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Цитрикс просит адрес сервера:', reply_markup=None)
            if call.data == 'citrix_lags':
                ctx_network_trouble = open('ctx_network_trouble.txt', encoding='UTF-8').read()
                ctx_network_trouble_1_1 = open('ctx_network_trouble_1_1.txt', encoding='UTF-8').read()
                ctx_network_trouble_1_2 = open('ctx_network_trouble_1_2.txt', encoding='UTF-8').read()
                ctx_network_trouble_2 = open('ctx_network_trouble_2.txt', encoding='UTF-8').read()
                ctx_network_trouble_3 = open('ctx_network_trouble_3.txt', encoding='UTF-8').read()
                ctx_network = open('ctx_network.png', 'rb')
                ctx_network_1 = open('ctx_network_1.png', 'rb')
                ctx_network_2 = open('ctx_network_2.png', 'rb')
                ctx_network_3 = open('ctx_network_3.png', 'rb')
                bot.send_message(call.message.chat.id, text=ctx_network_trouble)
                bot.send_photo(call.message.chat.id, ctx_network)
                bot.send_message(call.message.chat.id, text=ctx_network_trouble_1_1)
                bot.send_photo(call.message.chat.id, ctx_network_1)
                bot.send_message(call.message.chat.id, text=ctx_network_trouble_1_2)
                bot.send_message(call.message.chat.id, text=ctx_network_trouble_2)
                bot.send_photo(call.message.chat.id, ctx_network_2)
                bot.send_message(call.message.chat.id, text=ctx_network_trouble_3)
                bot.send_photo(call.message.chat.id, ctx_network_3)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Зависает Цитрикс, лагает связь:', reply_markup=None)
            if call.data == 'citrix_update':
                ctx_update_1 = open('ctx_update_1.txt', encoding='UTF-8').read()
                ctx_update_2 = open('ctx_update_2.txt', encoding='UTF-8').read()
                ctx_update_3 = open('ctx_update_3.txt', encoding='UTF-8').read()
                ctx_update_4 = open('ctx_update_4.txt', encoding='UTF-8').read()
                ctx_update_del = open('ctx_update_del.png', 'rb')
                ctx_home_4 = open('ctx_home_4.png', 'rb')
                ctx_home_5 = open('ctx_home_5.png', 'rb')
                ctx_home_6 = open('ctx_home_6.png', 'rb')
                bot.send_message(call.message.chat.id, text=ctx_update_1)
                bot.send_photo(call.message.chat.id, ctx_update_del)
                bot.send_message(call.message.chat.id, text=ctx_update_2)
                bot.send_photo(call.message.chat.id, ctx_home_4)
                bot.send_photo(call.message.chat.id, ctx_home_5)
                bot.send_message(call.message.chat.id, text=ctx_update_3)
                bot.send_photo(call.message.chat.id, ctx_home_6)
                bot.send_message(call.message.chat.id, text=ctx_update_4)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Обновление Цитрикса:', reply_markup=None)
            if call.data == 'lose_sound':
                softphone_sound_1 = open('softphone_sound_1.txt', encoding='UTF-8').read()
                softphone_sound_2 = open('softphone_sound_2.txt', encoding='UTF-8').read()
                softphone_sound_3_0 = open('softphone_sound_3_0.txt', encoding='UTF-8').read()
                softphone_sound_3_1 = open('softphone_sound_3_1.txt', encoding='UTF-8').read()
                softphone_sound_3_2 = open('softphone_sound_3_2.txt', encoding='UTF-8').read()
                softphone_sound_3_3 = open('softphone_sound_3_3.txt', encoding='UTF-8').read()
                softphone_sound_3_4 = open('softphone_sound_3_4.txt', encoding='UTF-8').read()
                softphone_sound_3_5 = open('softphone_sound_3_5.txt', encoding='UTF-8').read()
                softphone_sound_3 = open('softphone_sound_3.txt', encoding='UTF-8').read()
                softphone_sound_4 = open('softphone_sound_4.txt', encoding='UTF-8').read()
                softphone_sound_pic1 = open('softphone_sound_pic1.png', 'rb')
                softphone_sound_pic2 = open('softphone_sound_pic2.png', 'rb')
                softphone_sound_pic3_2 = open('softphone_sound_pic3_2.png', 'rb')
                softphone_sound_pic4 = open('softphone_sound_pic4.png', 'rb')
                softphone_sound_pic5 = open('softphone_sound_pic5.png', 'rb')
                softphone_sound_pic6 = open('softphone_sound_pic6.png', 'rb')
                softphone_sound_pic6_2 = open('softphone_sound_pic6_2.png', 'rb')
                softphone_sound_pic7 = open('softphone_sound_pic7.png', 'rb')
                softphone_sound_pic8 = open('softphone_sound_pic8.png', 'rb')
                bot.send_message(call.message.chat.id, text=softphone_sound_1)
                bot.send_photo(call.message.chat.id, softphone_sound_pic1)
                bot.send_message(call.message.chat.id, text=softphone_sound_2)
                bot.send_photo(call.message.chat.id, softphone_sound_pic2)
                bot.send_message(call.message.chat.id, text=softphone_sound_3)
                bot.send_message(call.message.chat.id, text=softphone_sound_3_0)
                bot.send_message(call.message.chat.id, text=softphone_sound_3_1)
                bot.send_photo(call.message.chat.id, softphone_sound_pic3_2)
                bot.send_message(call.message.chat.id, text=softphone_sound_3_2)
                bot.send_photo(call.message.chat.id, softphone_sound_pic4)
                bot.send_message(call.message.chat.id, text=softphone_sound_3_3)
                bot.send_photo(call.message.chat.id, softphone_sound_pic5)
                bot.send_message(call.message.chat.id, text=softphone_sound_3_4)
                bot.send_photo(call.message.chat.id, softphone_sound_pic6)
                bot.send_message(call.message.chat.id, text=softphone_sound_3_5)
                bot.send_photo(call.message.chat.id, softphone_sound_pic6_2)
                bot.send_message(call.message.chat.id, text=softphone_sound_4)
                bot.send_photo(call.message.chat.id, softphone_sound_pic7)
                bot.send_photo(call.message.chat.id, softphone_sound_pic8)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Пропал звук:', reply_markup=None)
            if call.data == 'softphone_statuses':
                softphone_status = open('softphone_status.txt', encoding='UTF-8').read()
                softphone_status_pic = open('softphone_status_pic.png', 'rb')
                bot.send_message(call.message.chat.id, text=softphone_status)
                bot.send_photo(call.message.chat.id, softphone_status_pic)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Не меняется статус:', reply_markup=None)
            if call.data == 'full_mail':
                outlook_ar = open('outlook_ar.txt', encoding='UTF-8').read()
                outlook_ar_pic1 = open('outlook_ar_pic1.png', 'rb')
                outlook_ar_pic2 = open('outlook_ar_pic2.png', 'rb')
                bot.send_message(call.message.chat.id, text=outlook_ar)
                bot.send_photo(call.message.chat.id, outlook_ar_pic1)
                bot.send_photo(call.message.chat.id, outlook_ar_pic2)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Переполнена почта, архив:', reply_markup=None)
            if call.data == 'pc_not_in_domain':
                pc_not_domian = open('pc_not_domian.txt', encoding='UTF-8').read()
                pc_not_domian_pic = open('pc_not_domian_pic.png', 'rb')
                bot.send_message(call.message.chat.id, text=pc_not_domian)
                bot.send_photo(call.message.chat.id, pc_not_domian_pic)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Ошибка при входе в ПК:', reply_markup=None)
            if call.data == 'two_monitors':
                pc_ctx_monitor_1 = open('pc_ctx_monitor_1.txt', encoding='UTF-8').read()
                pc_ctx_monitor_pic1 = open('pc_ctx_monitor_pic1.png', 'rb')
                pc_ctx_monitor_2 = open('pc_ctx_monitor_2.txt', encoding='UTF-8').read()
                pc_ctx_monitor_pic2 = open('pc_ctx_monitor_pic2.png', 'rb')
                bot.send_message(call.message.chat.id, text=pc_ctx_monitor_1)
                bot.send_photo(call.message.chat.id, pc_ctx_monitor_pic1)
                bot.send_message(call.message.chat.id, text=pc_ctx_monitor_2)
                bot.send_photo(call.message.chat.id, pc_ctx_monitor_pic2)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Изображение на 2 монитора:', reply_markup=None)
            if call.data == 'default_browser':
                ctx_server = open('ctx_default_program.txt', encoding='UTF-8').read()
                ctx_default_1 = open('ctx_default_1.png', 'rb')
                ctx_default_2 = open('ctx_default_2.png', 'rb')
                ctx_default_3 = open('ctx_default_3.png', 'rb')
                bot.send_message(call.message.chat.id, text=ctx_server)
                bot.send_photo(call.message.chat.id, ctx_default_1)
                bot.send_photo(call.message.chat.id, ctx_default_2)
                bot.send_photo(call.message.chat.id, ctx_default_3)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Браузер по умолчанию:', reply_markup=None)
            if call.data == 'bookmarks':
                browser_bookmarks = open('browser_bookmarks.txt', encoding='UTF-8').read()
                browser_bookmarks_pic1 = open('browser_bookmarks_pic1.png', 'rb')
                browser_bookmarks_pic2 = open('browser_bookmarks_pic2.png', 'rb')
                bot.send_message(call.message.chat.id, text=browser_bookmarks)
                bot.send_photo(call.message.chat.id, browser_bookmarks_pic1)
                bot.send_photo(call.message.chat.id, browser_bookmarks_pic2)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Как сохранить закладки:', reply_markup=None)
            if call.data == 'clean_cache':
                browser_cache_1 = open('browser_cache_1.txt', encoding='UTF-8').read()
                browser_cache_2 = open('browser_cache_2.txt', encoding='UTF-8').read()
                browser_cache_3 = open('browser_cache_3.txt', encoding='UTF-8').read()
                browser_cache_pic1 = open('browser_cache_pic1.png', 'rb')
                browser_cache_pic2 = open('browser_cache_pic2.png', 'rb')
                bot.send_message(call.message.chat.id, text=browser_cache_1)
                bot.send_photo(call.message.chat.id, browser_cache_pic1)
                bot.send_message(call.message.chat.id, text=browser_cache_2)
                bot.send_photo(call.message.chat.id, browser_cache_pic2)
                bot.send_message(call.message.chat.id, text=browser_cache_3)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Очистка кэша:', reply_markup=None)
            if call.data == 'domain_pass_change':
                pass_domain = open('pass_domain.txt', encoding='UTF-8').read()
                bot.send_message(call.message.chat.id, text=pass_domain)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Как сменить пароль от системы:', reply_markup=None)
            if call.data == 'another_password':
                tickets_another_account = open('tickets_another_account.txt', encoding='UTF-8').read()
                tickets_another_account_pic = open('tickets_another_account_pic.png', 'rb')
                bot.send_message(call.message.chat.id, text=tickets_another_account)
                bot.send_photo(call.message.chat.id, tickets_another_account_pic)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Пароль от второй УЗ:', reply_markup=None)
            if call.data == 'print_on_printer':
                printer = open('printer.txt', encoding='UTF-8').read()
                bot.send_message(call.message.chat.id, text=printer)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text='Печать на принтере:', reply_markup=None)


if __name__ == '__main__':
    bot.polling(none_stop=True)
