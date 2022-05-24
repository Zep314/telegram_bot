import sys
import requests
import json
from jsonparse import JsonParse
#from message import TeleMessage
from settings import Settings
from botIO import MyIO
from time import sleep

class GrigoryTestPythonBot:

    incoming_msgs = []
    offset_msg = 0

    def __init__(self):
        self.settings = Settings()
        self.myIO = MyIO()

    def _send_message(self,chat_id,text,reply_to_message_id = 0):
        url = f"{self.settings.baseUrl}sendMessage?chat_id={chat_id}&text={text}"
        if reply_to_message_id: url += f"&reply_to_message_id={reply_to_message_id}"
        requests.get(url)

    def _getUpdates(self):
        url = f"{self.settings.baseUrl}getUpdates?offset={self.offset_msg}"

        response = requests.get(url)
        data = json.loads(response.text)

        self.incoming_msgs = JsonParse.Parse(JsonParse(data))
                

    #def _check_events(self):
        #print("222")

#        self._send_message(418068635,"Ответ123")
#        sys.exit()

    def _help_action(self,msg):
        help_msg =  'Привет! Я Telegram-бот ГРИША\n'+\
                    ' Я умею показывать погоду по указанному Вами городу'
        self._send_message(msg.chat_id,help_msg,msg.message_id)

    def _start_action(self,msg):
        msg_string =  'Тут надо написать функцию СТАРТ'
        self._send_message(msg.chat_id,msg_string,msg.message_id)

    def _save(self,fmt,msg):
        out = MyIO()

        result = out.SaveLog(msg.user_id, msg.message_id, msg.chat_id,fmt)
        if not result:
            self._send_message(msg.chat_id,'Ошибка отправки файла',msg.message_id)

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
                        case '/savetxt':
                            self._save('TXT',msg)
                        case '/savejson':
                            self._save('JSON',msg)
                        case '/savexml':
                            self._save('XML',msg)
                        case _:
                            self._send_message(msg.chat_id,'Не понимаю, чего Вы от меня хотите...',msg.message_id)
                self.offset_msg = msg.update_id +1
                #print(msg.message_text)
            sleep(1)

            #sys.exit()
