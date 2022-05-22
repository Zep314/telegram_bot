import sys
import requests
import json
from jsonparse import JsonParse
from message import TeleMessage
from settings import Settings
from time import sleep

class GrigoryTestPythonBot:

    incoming_msgs = []
    offset_msg = 0

    def __init__(self):
        self.settings = Settings()

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

    def run_bot(self):
        self.offset_msg = 0;
        print("Press Ctrl+C to exit")
        while True:
            #self._check_events()
            self._getUpdates()
            if len(self.incoming_msgs) > 0:
                print(len(self.incoming_msgs))
                for msg in self.incoming_msgs:
                    #message.TeleMessage.Print(msg)
                    TeleMessage.Print(msg)
                    self._send_message(msg.chat_id,msg.message_text,msg.message_id)
                self.offset_msg = msg.update_id +1
                print(msg.message_text)
            sleep(1)
            #sys.exit()
