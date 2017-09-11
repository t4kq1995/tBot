# -*- coding: utf-8 -*-
import config
import telebot
import logging
import datetime
import time

bot = telebot.TeleBot(config.token)


def __get_task_list():
    # Here will be some request to API server to get task list
    return [
        {
            'name': 'Владислав Небеснюк',
            'birthday': '24.07.1995',
            'group': 'Семья'
        },
        {
            'name': 'Владислав Компаниец',
            'birthday': '01.02.1996',
            'group': 'Друзья'
        },
        {
            'name': 'Тест',
            'birthday': '14.09.1994',
            'group': 'Тест'
        },
        {
            'name': 'Тест',
            'birthday': '11.09.1994',
            'group': 'Тест'
        }
    ]


def __get_message_template(task):
    return 'Имя и фамилия: {0}\n' \
           'Группа: {1}\n' \
           'Дата рождения: {2}\n'.format(task['name'], task['group'], task['birthday'])


def __check_date_task(task):
    date_three_days = datetime.datetime.now() + datetime.timedelta(days=3)

    task_date = (
        int(task['birthday'].split('.')[0]),
        int(task['birthday'].split('.')[1])
    )
    date_now = (datetime.datetime.now().day, datetime.datetime.now().month)
    date_now_three = (date_three_days.day, date_three_days.month)

    if (task_date[0] == date_now[0] and task_date[1] == date_now[1]) or (task_date[0] == date_now_three[0] and task_date[1] == date_now_three[1]):
        return True

    return False


def find_task_with_birthday_today():
    # Get list of tasks
    task_list = __get_task_list()

    # Check every task
    for _el in task_list:
        if __check_date_task(_el):
            logging.info('[App] Found birthday task to send')
            send_message_to_bot(__get_message_template(_el))


@bot.message_handler(content_types=["text"])
def send_message_to_bot(message):
    user_access = [
        (397003777, 't4kq2407'),
        (398683260, 'Nastia_Danilenko')
    ]
    for user in user_access:
        bot.send_message(user[0], message)


if __name__ == '__main__':
    # Init logger
    logging.getLogger('iRemember').setLevel(logging.DEBUG)
    logging.basicConfig(
        format=
        '[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - %(message)s',
        level=logging.INFO,
        filename='bot_log.log', datefmt='%d.%m.%Y %H:%M:%S')

    while True:
        # Pause for certain time
        date_and_time = datetime.datetime.now()
        print date_and_time.second
        if date_and_time.hour == config.hour_time\
                and date_and_time.minute == config.minute_time \
                and date_and_time.second == 0:
            find_task_with_birthday_today()
            time.sleep(1)
