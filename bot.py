# Основной класс работы с ботом

import sys
import requests
import json
import signal
import time
import os
from jsonparse import JsonParse
from settings import Settings
from botIO import MyIO
from accuweather import MyAccuWeather
from time import sleep

class GrigoryTestPythonBot:

    def __init__(self):
        self.settings = Settings()
        self.myIO = MyIO()
        self.incoming_msgs = []
        self.users = {}     # Тут храним ID юзеров с активными сессиями
        self.offset_msg = 0

    # Посылание сообщений
    # parse_mode работает только с MarkDown, с HTML - на работает, хотя в доке написано, что все гут (((
    def _send_message(self,chat_id,text,reply_to_message_id = 0, parse_mode = 'Markdown'):
        url = f"{self.settings.baseUrl}sendMessage?chat_id={chat_id}&text={text}&parse_mode={parse_mode}"
        if reply_to_message_id: 
            url += f"&reply_to_message_id={reply_to_message_id}"
        requests.get(url)

    # Обработчик входящих сообщений
    def _getUpdates(self):
        url = f"{self.settings.baseUrl}getUpdates?offset={self.offset_msg}"
        response = requests.get(url)
        data = json.loads(response.text)
        self.incoming_msgs = JsonParse.Parse(JsonParse(data))
                
    # Обрабочтик запроса на прогноз погоды
    def _forecast(self,msg):
        aw = MyAccuWeather() # Тут создаем объект

        # А тут вызываем метод-запрос погоды
        self._send_message(msg.chat_id,
                           aw.GetWeather(msg.message_text.split(' ',maxsplit=1)[1]),
                           msg.message_id,parse_mode = 'Markdown')

    # "Пасхалочка" с котиками
    def _cat(self,msg):
        cat_gif = requests.get(self.settings.cats_api_url) # Тут простой запрос без параметров.
                                                           # Возвращает GIF 
        file_gif = os.path.join(self.settings.data_dir, 'random_cat.gif')
        with open(file_gif, mode = 'wb') as g:
            g.write(cat_gif.content)
        with open(file_gif, mode = 'rb') as g:
            post_data = {
                        'chat_id': msg.chat_id,
                        'caption': 'Котик',
                        'reply_to_message_id': msg.message_id
                        }
            post_file = {
                        'video': g
                        }
            self._send_message(msg.chat_id,'Ура! Вы нашли пасхалочку! )))))\n Вот Вам котик в карму!',msg.message_id)
            requests.post(f'{self.settings.baseUrl}sendVideo', data = post_data, files = post_file)
        if os.path.exists(file_gif):
            os.remove(file_gif)

    # Обработчик запроса хелп мессаги
    def _help_action(self,msg):
        help_msg =  'Привет! Я Telegram-бот ГРИША\n'+\
                    '\t Я умею показывать погоду по указанному Вами городу\n'+\
                    '\t Команда /start запускает работу со мной.'    
        self._send_message(msg.chat_id,help_msg,msg.message_id)

    # Обработка запроса на возврат журнала запроса в чат
    def _get_log(self,msg):
        with open(os.path.join(self.settings.data_dir,f'{msg.user_id}.db'), mode = 'r', encoding="utf-8") as f:
            msg_str = 'Полный журнал сообщений:\n'+''.join(f.readlines())
        while len(msg_str)> 4095:  # В методе sendMessage ограничение на длину текста - в 4096 символов
            self._send_message(msg.chat_id,msg_str[:4095],msg.message_id)
            msg_str = msg_str[4095:]

    # Запуск работы с ботом
    def _start_action(self,msg):
        self.users[msg.user_id] = [time.time(), msg.chat_id]    # Запоминаем user_id и время входа
        msg_string =  'У Вас есть возможность использовать команды:\n'+\
                    '\t /forecast <Название города> - прогноз погоды по указанному городу\n'+\
                    '\t /saveTXT - сохранить журнал запросов в TXT формате\n'+\
                    '\t /saveXML - сохранить журнал запросов в XML формате\n'+\
                    '\t /saveJSON - сохранить журнал запросов в JSON формате\n'+\
                    '\t /log  - показать журнал запросов в чате\n'+\
                    f'\t время сеанса ограничено {self.settings.life_time} секунд'   
        self._send_message(msg.chat_id,msg_string,msg.message_id)

    def _is_started(self,msg): # Определяем, есть ли пользователь среди зареганых
        if msg.user_id in self.users:
            return True
        else:
            return False

    # Отдаем пользователю файл журнала работы в нужном fmt формате
    def _save(self,fmt,msg):
        out = MyIO()
        result = out.SaveLog(msg.user_id, msg.message_id, msg.chat_id,fmt)
        if not result:
            self._send_message(msg.chat_id,'Ошибка отправки файла',msg.message_id)

    # Смотрим, не "протухли" ли у нас пользователи
    def _end_of_life(self):
        user_keys = self.users.keys()        
        for key in user_keys:
            if (time.time() - self.users[key][0]) > self.settings.life_time:
                self._send_message(self.users[key][1],
                                'Время истекло. Ваш сеанс завершен.')
                del self.users[key]    # "Выгоняем" пользователя из активных
                break

    # Обработчик команд от зарегистрированных пользователей
    def _get_command(self,msg):
        self.users[msg.user_id] = [time.time(), msg.chat_id]
        if msg.message_text.lower().find('/savetxt') == 0:
            return 'saveTXT'
        elif msg.message_text.lower().find('/savejson') == 0:
            return 'saveJSON'
        elif msg.message_text.lower().find('/savexml') == 0:
            return 'saveXML'
        elif msg.message_text.lower().find('/log') == 0:
            return 'log'
        elif msg.message_text.lower().find('/forecast') == 0:
            return 'forecast'
        elif msg.message_text.lower().find('/cat') == 0:
            return 'cat'
        else:
            return 'unknown'

    # Основной рабочий цикл бота
    def run_bot(self):
        self.offset_msg = 0;
        print("Press Ctrl+C to exit")
        while True:
            self._getUpdates()
            if len(self.incoming_msgs) > 0:
                for msg in self.incoming_msgs: # О! Сообщение пришло (может быть и не одно!)
                    match msg.message_text.lower(): # Все подряд сообщения проверяем
                        case '/help':
                            self._help_action(msg)
                        case '/start':
                            self._start_action(msg)
                        case _: # Тут и зареганые сообщения и что попало может быть
                            if self._is_started(msg): # Тут уже хорошие пользователи пишут
                                match self._get_command(msg):
                                    case 'saveTXT':
                                        self._save('TXT',msg)
                                    case 'saveJSON':
                                        self._save('JSON',msg)
                                    case 'saveXML':
                                        self._save('XML',msg)
                                    case 'log':
                                        self._get_log(msg)
                                    case 'forecast':
                                        self._forecast(msg)
                                    case 'cat':
                                        self._cat(msg)
                                    case _:
                                        self._send_message(msg.chat_id,'Не понимаю, чего Вы от меня хотите...\n /help - для помощи',msg.message_id)
                            else: # Ругаемся....
                                self._send_message(msg.chat_id,'Не понимаю, чего Вы от меня хотите...\n /help - для помощи',msg.message_id)
                self.offset_msg = msg.update_id +1
            self._end_of_life() # Проверяем "протухших" юзеров
            sleep(1)


# отслеживаем нажатие Ctrl+C, вешаем на это событие свой обработчик
def handler(signum, frame):
    res = input("\nCtrl+c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        sys.exit(1)
# Перехват события, и выполнение именно нашей процедуры        
signal.signal(signal.SIGINT, handler)