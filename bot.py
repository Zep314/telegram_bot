import sys
import requests
import json
import signal
import time
import os
from jsonparse import JsonParse
#from message import TeleMessage
from settings import Settings
from botIO import MyIO
from accuweather import MyAccuWeather
from time import sleep

class GrigoryTestPythonBot:


    def __init__(self):
        self.settings = Settings()
        self.myIO = MyIO()
        self.incoming_msgs = []
        self.users = {}
        self.offset_msg = 0

    def _send_message(self,chat_id,text,reply_to_message_id = 0, parse_mode = 'Markdown'):
        url = f"{self.settings.baseUrl}sendMessage?chat_id={chat_id}&text={text}&parse_mode={parse_mode}"
        if reply_to_message_id: 
            url += f"&reply_to_message_id={reply_to_message_id}"
        requests.get(url)

    def _getUpdates(self):
        url = f"{self.settings.baseUrl}getUpdates?offset={self.offset_msg}"

        response = requests.get(url)
        data = json.loads(response.text)

        self.incoming_msgs = JsonParse.Parse(JsonParse(data))
                
    def _forecast(self,msg):
        aw = MyAccuWeather()
        self._send_message(msg.chat_id,
                           aw.GetWeather(msg.message_text.split(' ',maxsplit=1)[1]),
                           msg.message_id,parse_mode = 'Markdown')

    def _cat(self,msg):
        cat_gif = requests.get(self.settings.cats_api_url)
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

    def _help_action(self,msg):
        help_msg =  'Привет! Я Telegram-бот ГРИША\n'+\
                    '\t Я умею показывать погоду по указанному Вами городу\n'+\
                    '\t Команда /start запускает работу со мной.'    
        self._send_message(msg.chat_id,help_msg,msg.message_id)

    def _start_action(self,msg):
        self.users[msg.user_id] = [time.time(), msg.chat_id]
        
        msg_string =  'У Вас есть возможность использовать команды:\n'+\
                    '\t /forecast <Название города> - прогноз погоды по указанному городу\n'+\
                    '\t /saveTXT - сохранить журнал запросов в TXT формате\n'+\
                    '\t /saveXML - сохранить журнал запросов в XML формате\n'+\
                    '\t /saveJSON - сохранить журнал запросов в JSON формате\n'+\
                    f'\t время сеанса ограничено {self.settings.life_time} секунд'   
        self._send_message(msg.chat_id,msg_string,msg.message_id)

    def _is_started(self,msg):
        if msg.user_id in self.users:
            return True
        else:
            return False

    def _save(self,fmt,msg):
        out = MyIO()
        result = out.SaveLog(msg.user_id, msg.message_id, msg.chat_id,fmt)
        if not result:
            self._send_message(msg.chat_id,'Ошибка отправки файла',msg.message_id)

    def _end_of_life(self):
        user_keys = self.users.keys()        
        for key in user_keys:
            if (time.time() - self.users[key][0]) > self.settings.life_time:
                self._send_message(self.users[key][1],
                                'Время истекло. Ваш сеанс завершен.')
                del self.users[key]
                break

    def _get_command(self,command_str):
        if command_str.lower().find('/savetxt') == 0:
            return 'saveTXT'
        elif command_str.lower().find('/savejson') == 0:
            return 'saveJSON'
        elif command_str.lower().find('/savexml') == 0:
            return 'saveXML'
        elif command_str.lower().find('/forecast') == 0:
            return 'forecast'
        elif command_str.lower().find('/cat') == 0:
            return 'cat'
        else:
            return 'unknown'

    def run_bot(self):
        self.offset_msg = 0;
        print("Press Ctrl+C to exit")
        while True:
            self._getUpdates()
            if len(self.incoming_msgs) > 0:

                for msg in self.incoming_msgs:
                    match msg.message_text.lower():
                        case '/help':
                            self._help_action(msg)
                        case '/start':
                            self._start_action(msg)
                        case _:
                            if self._is_started(msg):
                                match self._get_command(msg.message_text):
                                    case 'saveTXT':
                                        self._save('TXT',msg)
                                    case 'saveJSON':
                                        self._save('JSON',msg)
                                    case 'saveXML':
                                        self._save('XML',msg)
                                    case 'forecast':
                                        self._forecast(msg)
                                    case 'cat':
                                        self._cat(msg)
                                    case _:
                                        self._send_message(msg.chat_id,'Не понимаю, чего Вы от меня хотите...\n /help - для помощи',msg.message_id)
                            else:
                                self._send_message(msg.chat_id,'Не понимаю, чего Вы от меня хотите...\n /help - для помощи',msg.message_id)
                self.offset_msg = msg.update_id +1
            self._end_of_life()
            sleep(1)



def handler(signum, frame):
    res = input("\nCtrl+c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        sys.exit(1)
        
signal.signal(signal.SIGINT, handler)